CREATE TABLE IF NOT EXISTS users (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'ATTENDEE' CHECK(role IN ('ATTENDEE','ORGANIZER')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  venue TEXT NOT NULL,
  starts_at TIMESTAMPTZ NOT NULL,
  total_seats INTEGER NOT NULL CHECK(total_seats > 0),
  available_seats INTEGER NOT NULL CHECK(available_seats >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT seats_valid CHECK(available_seats <= total_seats)
);

CREATE TABLE IF NOT EXISTS registrations (
  id BIGSERIAL PRIMARY KEY,
  event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
  idempotency_key TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'CONFIRMED',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(event_id,idempotency_key)
);

CREATE TABLE IF NOT EXISTS notification_outbox (
  id BIGSERIAL PRIMARY KEY,
  registration_id BIGINT NOT NULL REFERENCES registrations(id) ON DELETE CASCADE,
  type TEXT NOT NULL DEFAULT 'REGISTRATION_CONFIRMED',
  status TEXT NOT NULL DEFAULT 'PENDING',
  attempts INTEGER NOT NULL DEFAULT 0,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  sent_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_reg_event ON registrations(event_id);
CREATE INDEX IF NOT EXISTS idx_reg_user ON registrations(user_id);
CREATE INDEX IF NOT EXISTS idx_outbox_status ON notification_outbox(status);

INSERT INTO events(name,venue,starts_at,total_seats,available_seats)
SELECT 'High Traffic Tech Conference','Main Auditorium',now()+interval '30 days',100,100
WHERE NOT EXISTS (SELECT 1 FROM events WHERE name='High Traffic Tech Conference');

INSERT INTO events(name,venue,starts_at,total_seats,available_seats)
SELECT 'Virtual Engineering Meetup','Online',now()+interval '14 days',1000,1000
WHERE NOT EXISTS (SELECT 1 FROM events WHERE name='Virtual Engineering Meetup');

INSERT INTO events(name,venue,starts_at,total_seats,available_seats)
SELECT 'Concurrency Stress Test [5 Seats]','Demo Sandbox',now()+interval '7 days',5,5
WHERE NOT EXISTS (SELECT 1 FROM events WHERE name='Concurrency Stress Test [5 Seats]');
