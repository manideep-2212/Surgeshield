require("dotenv").config();
const express=require("express");
const helmet=require("helmet");
const cors=require("cors");
const rateLimit=require("express-rate-limit");
const jwt=require("jsonwebtoken");
const bcrypt=require("bcryptjs");
const crypto=require("crypto");
const client=require("prom-client");
const {pool}=require("./db");
const redis=require("./redis");
const {notificationQueue}=require("./queue");

const app=express();
const PORT=Number(process.env.PORT||3000);
const INSTANCE=process.env.INSTANCE_NAME||"app";
const SECRET=process.env.JWT_SECRET||"local-change-me";

app.use(helmet({contentSecurityPolicy:false}));
app.use(cors());
app.use(express.json({limit:"100kb"}));
app.use(rateLimit({windowMs:60*1000,max:300,standardHeaders:true,legacyHeaders:false}));

const registry=new client.Registry();
client.collectDefaultMetrics({registery:registry,registers:[registry]});
const reqCounter=new client.Counter({name:"http_requests_total",help:"HTTP requests",labelNames:["method","route","status","instance"],registers:[registry]});
const regCounter=new client.Counter({name:"registrations_total",help:"Registration attempts",labelNames:["result","instance"],registers:[registry]});

app.use((req,res,next)=>{
  req.requestId=req.get("x-request-id")||crypto.randomUUID();
  res.setHeader("x-request-id",req.requestId);
  res.setHeader("x-served-by",INSTANCE);
  const start=Date.now();
  res.on("finish",()=>reqCounter.inc({method:req.method,route:req.path,status:res.statusCode,instance:INSTANCE}));
  req.startedAt=start; next();
});

async function runMigrations(){
  try{
    await pool.query(`ALTER TABLE registrations ADD COLUMN IF NOT EXISTS quantity INTEGER NOT NULL DEFAULT 1;`);
    await pool.query(`
      DO $$
      BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'registrations_quantity_check') THEN
          ALTER TABLE registrations ADD CONSTRAINT registrations_quantity_check CHECK (quantity > 0);
        END IF;
      END $$;
    `);
    await pool.query(`ALTER TABLE registrations DROP CONSTRAINT IF EXISTS registrations_event_id_user_id_key;`);
    await pool.query(`
      INSERT INTO events(name,venue,starts_at,total_seats,available_seats)
      SELECT 'Concurrency Stress Test [5 Seats]','Demo Sandbox',now()+interval '7 days',5,5
      WHERE NOT EXISTS (SELECT 1 FROM events WHERE name='Concurrency Stress Test [5 Seats]');
    `);
    console.log(`[${INSTANCE}] Migrations & demo seeds applied safely`);
  }catch(e){
    console.error(`[${INSTANCE}] Migration warning:`, e.message);
  }
}

async function seedDemoUsers(){
  const passwordHash=await bcrypt.hash("Password@123",10);
  for(const u of [
    ["Demo Attendee","attendee@surgeshield.local","ATTENDEE"],
    ["Demo Organizer","organizer@surgeshield.local","ORGANIZER"]
  ]){
    await pool.query(`
      INSERT INTO users(name,email,password_hash,role)
      VALUES($1,$2,$3,$4)
      ON CONFLICT(email) DO UPDATE SET password_hash=EXCLUDED.password_hash,role=EXCLUDED.role
    `,[u[0],u[1],passwordHash,u[2]]);
  }
}

function tokenFor(user){return jwt.sign({id:String(user.id),name:user.name,email:user.email,role:user.role},SECRET,{expiresIn:"8h"});}
function auth(req,res,next){
  const h=req.get("authorization")||"";
  if(!h.startsWith("Bearer "))return res.status(401).json({message:"Authentication required",servedBy:INSTANCE});
  try{req.user=jwt.verify(h.slice(7),SECRET);next();}catch{return res.status(401).json({message:"Invalid or expired token",servedBy:INSTANCE});}
}
function organizer(req,res,next){if(req.user.role!=="ORGANIZER")return res.status(403).json({message:"Organizer access required",servedBy:INSTANCE});next();}
async function clearEventsCache(){await redis.del("events:list");}

app.get("/health",async(req,res)=>{
  try{
    await pool.query("SELECT 1");
    await redis.ping();
    const workerHeartbeat = await redis.get("worker:heartbeat");
    res.json({status:"ok",instance:INSTANCE,database:"ok",redis:"ok",worker:workerHeartbeat?"active":"offline",servedBy:INSTANCE});
  }catch(e){res.status(503).json({status:"degraded",instance:INSTANCE,error:e.message,servedBy:INSTANCE});}
});
app.get("/ready",async(req,res)=>{try{await pool.query("SELECT 1");res.json({ready:true,instance:INSTANCE,servedBy:INSTANCE});}catch{res.status(503).json({ready:false,servedBy:INSTANCE});}});
app.get("/metrics",async(req,res)=>{res.set("Content-Type",registry.contentType);res.end(await registry.metrics());});

// Dedicated rate limiting demo endpoint (2 requests per instance per 10 seconds)
const demoLimiter=rateLimit({
  windowMs:10*1000,
  max:2,
  standardHeaders:true,
  legacyHeaders:false,
  message:{message:"Rate limit exceeded (HTTP 429). Cluster rate limit triggered.",servedBy:INSTANCE}
});
app.get("/api/demo/rate-limit-test",demoLimiter,(req,res)=>{
  res.json({message:"Rate limit check passed",status:"OK",servedBy:INSTANCE,timestamp:new Date().toISOString()});
});

app.post("/api/auth/register",async(req,res,next)=>{
 try{
  const {name,email,password,role="ATTENDEE"}=req.body;
  if(!name||!email||!password)return res.status(400).json({message:"Name, email and password are required",servedBy:INSTANCE});
  if(password.length<8)return res.status(400).json({message:"Password must be at least 8 characters",servedBy:INSTANCE});
  if(!["ATTENDEE","ORGANIZER"].includes(role))return res.status(400).json({message:"Invalid role",servedBy:INSTANCE});
  const hash=await bcrypt.hash(password,12);
  const {rows}=await pool.query(`INSERT INTO users(name,email,password_hash,role) VALUES($1,$2,$3,$4) RETURNING id,name,email,role`,
    [name.trim(),email.trim().toLowerCase(),hash,role]);
  res.status(201).json({user:rows[0],token:tokenFor(rows[0]),servedBy:INSTANCE});
 }catch(e){if(e.code==="23505")return res.status(409).json({message:"Email already registered",servedBy:INSTANCE});next(e);}
});

app.post("/api/auth/login",async(req,res,next)=>{
 try{
  const {rows}=await pool.query("SELECT * FROM users WHERE email=$1",[String(req.body.email||"").trim().toLowerCase()]);
  if(!rows[0]||!(await bcrypt.compare(String(req.body.password||""),rows[0].password_hash)))return res.status(401).json({message:"Invalid email or password",servedBy:INSTANCE});
  const user={id:rows[0].id,name:rows[0].name,email:rows[0].email,role:rows[0].role};
  res.json({user,token:tokenFor(user),servedBy:INSTANCE});
 }catch(e){next(e);}
});
app.get("/api/auth/me",auth,(req,res)=>res.json({user:req.user,servedBy:INSTANCE}));

app.get("/api/events",async(req,res,next)=>{
 try{
  const cached=await redis.get("events:list");
  if(cached)return res.json({events:JSON.parse(cached),servedBy:INSTANCE,cache:"HIT"});
  const {rows}=await pool.query(`SELECT id,name,venue,starts_at,total_seats,available_seats,
    ROUND((100.0*(total_seats-available_seats)/NULLIF(total_seats,0))::numeric,1) fill_percent
    FROM events ORDER BY id`);
  await redis.set("events:list",JSON.stringify(rows),"EX",5);
  res.json({events:rows,servedBy:INSTANCE,cache:"MISS"});
 }catch(e){next(e);}
});

app.get("/api/events/:id",async(req,res,next)=>{
 try{const {rows}=await pool.query(`SELECT id,name,venue,starts_at,total_seats,available_seats,
  ROUND((100.0*(total_seats-available_seats)/NULLIF(total_seats,0))::numeric,1) fill_percent FROM events WHERE id=$1`,[Number(req.params.id)]);
  if(!rows[0])return res.status(404).json({message:"Event not found",servedBy:INSTANCE});res.json({event:rows[0],servedBy:INSTANCE});
 }catch(e){next(e);}
});

app.post("/api/events/:id/register",auth,async(req,res,next)=>{
 const eventId=Number(req.params.id),userId=Number(req.user.id);
 const key=String(req.get("Idempotency-Key")||"").trim();
 if(!key)return res.status(400).json({message:"Idempotency-Key is required",servedBy:INSTANCE});

 const rawQty=req.body?.quantity!==undefined?req.body.quantity:1;
 const quantity=Number(rawQty);
 if(!Number.isInteger(quantity)||quantity<1){
   return res.status(400).json({message:"Ticket quantity must be a positive whole number (>= 1)",servedBy:INSTANCE});
 }

 const db=await pool.connect();
 try{
  await db.query("BEGIN");
  // 1. Idempotency protection check
  const idem=await db.query(`SELECT r.id,r.quantity,r.status,r.created_at,e.name FROM registrations r JOIN events e ON e.id=r.event_id WHERE r.event_id=$1 AND r.idempotency_key=$2`,[eventId,key]);
  if(idem.rows[0]){
    await db.query("COMMIT");
    regCounter.inc({result:"idempotent-replay",instance:INSTANCE});
    return res.json({message:"Already processed",registration:idem.rows[0],replayed:true,servedBy:INSTANCE});
  }

  // 2. Strict concurrency control using SELECT ... FOR UPDATE
  const locked=await db.query("SELECT id,name,available_seats,total_seats FROM events WHERE id=$1 FOR UPDATE",[eventId]);
  if(!locked.rows[0]){
    await db.query("ROLLBACK");
    return res.status(404).json({message:"Event not found",servedBy:INSTANCE});
  }
  const available=Number(locked.rows[0].available_seats);
  if(available<quantity){
    await db.query("ROLLBACK");
    regCounter.inc({result:"insufficient-seats",instance:INSTANCE});
    return res.status(409).json({
      message: available===0 ? "Sold out" : `Not enough seats available (requested: ${quantity}, remaining: ${available})`,
      availableSeats: available,
      requested: quantity,
      servedBy: INSTANCE
    });
  }

  // 3. Atomically decrement seats & insert registration (allows legitimate repeated bookings)
  await db.query("UPDATE events SET available_seats=available_seats-$1 WHERE id=$2",[quantity,eventId]);
  const inserted=await db.query(
    `INSERT INTO registrations(event_id,user_id,idempotency_key,quantity) VALUES($1,$2,$3,$4) RETURNING id,event_id,user_id,quantity,status,created_at`,
    [eventId,userId,key,quantity]
  );
  const outbox=await db.query("INSERT INTO notification_outbox(registration_id) VALUES($1) RETURNING id",[inserted.rows[0].id]);
  await db.query("COMMIT");

  // 4. Dispatch async confirmation job to BullMQ
  await notificationQueue.add(
    "registration-confirmation",
    {registrationId:inserted.rows[0].id,outboxId:outbox.rows[0].id,userId,eventId,quantity},
    {attempts:5,backoff:{type:"exponential",delay:1000},removeOnComplete:1000,removeOnFail:5000}
  );
  await clearEventsCache();
  regCounter.inc({result:"confirmed",instance:INSTANCE});
  res.status(201).json({
    message:"Registration confirmed",
    registration:inserted.rows[0],
    notification:"queued",
    remainingSeats:available-quantity,
    servedBy:INSTANCE
  });
 }catch(e){
  try{await db.query("ROLLBACK");}catch{}
  if(e.code==="23505")return res.status(409).json({message:"Duplicate registration request (idempotency conflict)",servedBy:INSTANCE});
  next(e);
 }
 finally{db.release();}
});

app.get("/api/my-registrations",auth,async(req,res,next)=>{
 try{
   const {rows}=await pool.query(`
     SELECT r.id,r.quantity,r.status,r.created_at,e.id event_id,e.name,e.venue,e.starts_at,
            COALESCE(no.status, 'QUEUED') AS notification_status,
            no.sent_at
     FROM registrations r
     JOIN events e ON e.id=r.event_id
     LEFT JOIN notification_outbox no ON no.registration_id=r.id
     WHERE r.user_id=$1
     ORDER BY r.created_at DESC
   `,[Number(req.user.id)]);
   res.json({registrations:rows,servedBy:INSTANCE});
 }catch(e){next(e);}
});

app.post("/api/events",auth,organizer,async(req,res,next)=>{
 try{const {name,venue,startsAt,totalSeats}=req.body;const seats=Number(totalSeats);
  if(!name||!venue||!startsAt||!Number.isInteger(seats)||seats<1)return res.status(400).json({message:"Valid event fields are required",servedBy:INSTANCE});
  const {rows}=await pool.query(`INSERT INTO events(name,venue,starts_at,total_seats,available_seats) VALUES($1,$2,$3,$4,$4) RETURNING *`,[name.trim(),venue.trim(),startsAt,seats]);
  await clearEventsCache();res.status(201).json({event:rows[0],servedBy:INSTANCE});
 }catch(e){next(e);}
});

// Demo Helpers: Reset Concurrency Test Event
app.post("/api/demo/reset-concurrency-event",async(req,res,next)=>{
  try{
    const {rows}=await pool.query(`
      UPDATE events 
      SET available_seats=5, total_seats=5 
      WHERE name='Concurrency Stress Test [5 Seats]'
      RETURNING id,name,total_seats,available_seats
    `);
    await clearEventsCache();
    res.json({message:"Concurrency test event reset to 5 seats",event:rows[0],servedBy:INSTANCE});
  }catch(e){next(e);}
});

// Reset single event capacity back to full starting total_seats
app.post("/api/events/:id/reset-capacity",auth,organizer,async(req,res,next)=>{
  try{
    const eventId=Number(req.params.id);
    const {rows}=await pool.query(
      `UPDATE events SET available_seats=total_seats WHERE id=$1 RETURNING id,name,total_seats,available_seats`,
      [eventId]
    );
    if(!rows[0]) return res.status(404).json({message:"Event not found",servedBy:INSTANCE});
    await clearEventsCache();
    res.json({message:`Event "${rows[0].name}" reset to starting capacity (${rows[0].total_seats} seats)`,event:rows[0],servedBy:INSTANCE});
  }catch(e){next(e);}
});

// Reset all events capacity back to starting total_seats
app.post("/api/events/reset-all-capacity",auth,organizer,async(req,res,next)=>{
  try{
    const {rows}=await pool.query(
      `UPDATE events SET available_seats=total_seats RETURNING id,name,total_seats,available_seats`
    );
    await clearEventsCache();
    res.json({message:"All events reset to starting capacity",events:rows,servedBy:INSTANCE});
  }catch(e){next(e);}
});

// Full System Reset: clears registrations, outbox, flushes cache/queue, resets all event seats to initial capacity
app.post("/api/admin/reset-system",auth,organizer,async(req,res,next)=>{
  try{
    await pool.query("TRUNCATE TABLE registrations CASCADE;");
    await pool.query("TRUNCATE TABLE notification_outbox CASCADE;");
    await pool.query("UPDATE events SET available_seats = total_seats;");
    await redis.del("events:list");
    await notificationQueue.drain().catch(()=>{});
    try { regCounter.reset(); } catch(e){}
    res.json({message:"System completely reset: registrations cleared, seats restored, queue drained",servedBy:INSTANCE});
  }catch(e){next(e);}
});

// Demo Helpers: Auto-scaling simulation surge
app.post("/api/demo/simulate-surge",async(req,res,next)=>{
  try{
    const count=Math.min(Number(req.body.count)||25,50);
    const jobs=[];
    for(let i=0;i<count;i++){
      jobs.push(notificationQueue.add("surge-job",{surgeId:crypto.randomUUID(),index:i+1},{removeOnComplete:500,removeOnFail:1000}));
    }
    await Promise.all(jobs);
    res.json({message:`Surge triggered: ${count} jobs queued in BullMQ`,enqueued:count,servedBy:INSTANCE});
  }catch(e){next(e);}
});

app.get("/api/admin/dashboard",auth,organizer,async(req,res,next)=>{
 try{
  const [stats,events,recent,outbox,queueCounts,workerHeartbeat]=await Promise.all([
   pool.query(`SELECT count(*)::int registrations,count(*) FILTER(WHERE status='CONFIRMED')::int confirmed FROM registrations`),
   pool.query(`SELECT id,name,total_seats,available_seats,total_seats-available_seats registered,
    ROUND((100.0*(total_seats-available_seats)/NULLIF(total_seats,0))::numeric,1) fill_percent FROM events ORDER BY id`),
   pool.query(`SELECT r.id,r.quantity,r.status,r.created_at,e.name,u.email,COALESCE(no.status,'QUEUED') notification_status FROM registrations r JOIN events e ON e.id=r.event_id JOIN users u ON u.id=r.user_id LEFT JOIN notification_outbox no ON no.registration_id=r.id ORDER BY r.created_at DESC LIMIT 10`),
   pool.query(`SELECT count(*)::int pending,count(*) FILTER(WHERE status='PROCESSING')::int processing,count(*) FILTER(WHERE status='SENT')::int sent,count(*) FILTER(WHERE status='FAILED')::int failed FROM notification_outbox`),
   notificationQueue.getJobCounts("waiting","active","completed","failed","delayed").catch(()=>({waiting:0,active:0,completed:0,failed:0,delayed:0})),
   redis.get("worker:heartbeat").catch(()=>null)
  ]);
  const soldOut=events.rows.filter(e=>Number(e.available_seats)===0).length;
  
  const queueDepth=(queueCounts.waiting||0)+(queueCounts.active||0);
  const baseWorkers=2;
  const simulatedWorkers=Math.min(10,Math.max(baseWorkers,baseWorkers+Math.ceil(queueDepth/3)));
  const autoscalingStatus=queueDepth>0?(simulatedWorkers>2?"SCALING_UP":"DRAINING_QUEUE"):"IDLE_BASELINE";
  const isWorkerActive=!!workerHeartbeat;

  res.json({
   generatedAt:new Date().toISOString(),
   instance:INSTANCE,
   servedBy:INSTANCE,
   services:{
     nginx:"Healthy",
     api:"Healthy",
     postgresql:"Healthy",
     redis:"Healthy",
     bullmq:queueCounts.failed>5?"Degraded":"Healthy",
     worker:isWorkerActive?"Active (Heartbeat OK)":"Stopped / Offline (Jobs Queued in Redis)"
   },
   summary:{
     registrations:stats.rows[0].registrations,
     confirmed:stats.rows[0].confirmed,
     soldOutEvents:soldOut,
     apiInstances:3
   },
   queue:{
     outboxPending:outbox.rows[0].pending,
     outboxProcessing:outbox.rows[0].processing,
     outboxSent:outbox.rows[0].sent,
     outboxFailed:outbox.rows[0].failed,
     bullmqWaiting:queueCounts.waiting||0,
     bullmqActive:queueCounts.active||0,
     bullmqCompleted:queueCounts.completed||0,
     bullmqFailed:queueCounts.failed||0,
     depth:queueDepth
   },
   autoscaling:{
     mode:"Simulated",
     baseWorkers:2,
     maxWorkers:10,
     currentWorkers:simulatedWorkers,
     queueDepth,
     status:autoscalingStatus,
     description:"Simulated worker auto-scaler adjusts virtual pool size (2 to 10) dynamically based on BullMQ backlog"
   },
   workerStatus:isWorkerActive?"RUNNING":"STOPPED",
   events:events.rows,
   recent:recent.rows
  });
 }catch(e){next(e);}
});

app.use((err,req,res,next)=>{
  console.error(JSON.stringify({requestId:req.requestId,error:err.message,instance:INSTANCE}));
  res.status(500).json({message:"Internal server error",requestId:req.requestId,servedBy:INSTANCE});
});

(async()=>{
  await pool.query("SELECT 1");
  await runMigrations();
  await seedDemoUsers();
  app.listen(PORT,()=>console.log(`API ${INSTANCE} listening on ${PORT}`));
})().catch(e=>{console.error(e);process.exit(1);});
