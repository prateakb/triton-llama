CREATE TABLE IF NOT EXISTS inference_logs (
    id SERIAL PRIMARY KEY,
    input_text TEXT,
    output_text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
