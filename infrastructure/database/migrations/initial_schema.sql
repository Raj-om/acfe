CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE sensors (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    location_lat FLOAT NOT NULL,
    location_lon FLOAT NOT NULL,
    reliability_score FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fusion_results (
    id VARCHAR PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    fused_confidence FLOAT NOT NULL,
    uncertainty FLOAT NOT NULL,
    conflict_level FLOAT NOT NULL,
    method_used VARCHAR NOT NULL,
    sources JSONB,
    weights JSONB,
    explanation JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT create_hypertable('fusion_results', 'created_at');
CREATE INDEX idx_fusion_results_time ON fusion_results USING BRIN (created_at);

CREATE TABLE alerts (
    id VARCHAR PRIMARY KEY,
    severity VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    location geometry(Point, 4326),
    confidence FLOAT NOT NULL,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_alerts_geom ON alerts USING GIST (location);

CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    action VARCHAR NOT NULL,
    resource VARCHAR NOT NULL,
    details JSONB,
    ip_address VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
