-- init.sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(150) NOT NULL UNIQUE,
  password TEXT NOT NULL,
  mfa TEXT,
  gendate BIGINT,
  expired BOOLEAN DEFAULT FALSE
);
