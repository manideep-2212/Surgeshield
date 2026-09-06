require("dotenv").config();
const { Worker } = require("bullmq");
const { connection } = require("./queue");
const { pool } = require("./db");
const redis = require("./redis");

const worker = new Worker("notifications", async job => {
  const { outboxId, registrationId } = job.data;
  
  if (outboxId) {
    await pool.query(
      `UPDATE notification_outbox SET status='PROCESSING', attempts=attempts+1 WHERE id=$1`,
      [outboxId]
    );
  }

  // Realistic async processing delay so the QUEUED -> PROCESSING -> SENT transition is visible
  await new Promise(resolve => setTimeout(resolve, 800));

  if (outboxId) {
    await pool.query(
      `UPDATE notification_outbox
       SET status='SENT', sent_at=now(), last_error=NULL
       WHERE id=$1`,
      [outboxId]
    );
    console.log(JSON.stringify({ worker: "notification-worker", jobId: job.id, outboxId, registrationId, status: "SENT" }));
  } else {
    console.log(JSON.stringify({ worker: "notification-worker", jobId: job.id, type: "surge-simulation", status: "COMPLETED" }));
  }
}, { connection, concurrency: 5 });

worker.on("failed", (job, err) => {
  if (job) {
    if (job.data?.outboxId) {
      pool.query(`UPDATE notification_outbox SET status='FAILED', last_error=$2 WHERE id=$1`, [job.data.outboxId, err.message]).catch(() => {});
    }
    console.error(JSON.stringify({ worker: "notification-worker", jobId: job.id, status: "FAILED", error: err.message }));
  }
});

worker.on("ready", () => {
  console.log("Notification worker ready");
  redis.set("worker:heartbeat", "online", "EX", 4).catch(() => {});
});

// Periodic heartbeat so the health endpoint and UI can detect worker status in real time
setInterval(() => {
  redis.set("worker:heartbeat", "online", "EX", 4).catch(() => {});
}, 2000);

