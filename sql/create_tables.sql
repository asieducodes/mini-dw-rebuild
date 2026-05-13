DROP TABLE IF EXISTS fact_records;
DROP TABLE IF EXISTS dim_branches;
DROP TABLE IF EXISTS dim_categories;
DROP TABLE IF EXISTS dim_sources;

CREATE TABLE dim_branches (
    branch_id VARCHAR(20) PRIMARY KEY,
    branch_name VARCHAR(100),
    region VARCHAR(100),
    is_active VARCHAR(10)
);

CREATE TABLE dim_categories (
    category_id VARCHAR(20) PRIMARY KEY,
    category_name VARCHAR(100),
    category_group VARCHAR(100),
    description TEXT,
    normal_sign NUMERIC,
    is_active VARCHAR(10)
);

CREATE TABLE dim_sources (
    source_id VARCHAR(20) PRIMARY KEY,
    source_name VARCHAR(100),
    source_type VARCHAR(50),
    owner VARCHAR(100),
    is_active VARCHAR(10)
);

CREATE TABLE fact_records (
    record_id VARCHAR(30),
    record_date DATE,
    branch_id VARCHAR(20),
    region VARCHAR(100),
    category_id VARCHAR(20),
    category_name VARCHAR(100),
    source_id VARCHAR(20),
    raw_value NUMERIC(12, 2),
    normal_sign NUMERIC,
    signed_value NUMERIC(12, 2),
    description TEXT
);