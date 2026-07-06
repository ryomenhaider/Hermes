-- Initial Hermes database migration.
-- Apply this migration against the database configured by DATABASE_URL.

CREATE TABLE IF NOT EXISTS fred_metadata (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    frequency VARCHAR NOT NULL,
    units VARCHAR NOT NULL,
    source VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS fred_obs (
    id SERIAL PRIMARY KEY,
    series_id VARCHAR NOT NULL,
    period DATE NOT NULL,
    value DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_fred_obs_series_id ON fred_obs(series_id);
CREATE INDEX IF NOT EXISTS ix_fred_obs_period ON fred_obs(period);



