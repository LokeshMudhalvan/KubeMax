CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE clusters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    api_server TEXT NOT NULL,
    kubeconfig TEXT, 
    created_by INT REFERENCES users(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE namespaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cluster_id INT REFERENCES clusters(id) ON DELETE CASCADE,
    last_synced_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (name, cluster_id)
);

CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    kind VARCHAR(50) NOT NULL,
    namespace_id INT REFERENCES namespaces(id) ON DELETE CASCADE,
    cluster_id INT REFERENCES clusters(id) ON DELETE CASCADE,
    labels JSONB,
    spec JSONB,
    status JSONB,
    last_synced_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (name, kind, namespace_id, cluster_id)
);

CREATE TABLE yaml_edits (
    id SERIAL PRIMARY KEY,
    resource_id INT REFERENCES resources(id) ON DELETE CASCADE,
    edited_by INT REFERENCES users(id) ON DELETE SET NULL,
    old_yaml TEXT,
    new_yaml TEXT,
    applied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE metrics_cache (
    id SERIAL PRIMARY KEY,
    resource_id INT REFERENCES resources(id) ON DELETE CASCADE,
    metric_name VARCHAR(255) NOT NULL,
    metric_value DOUBLE PRECISION,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE dashboard_settings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    layout JSONB,
    filters JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
