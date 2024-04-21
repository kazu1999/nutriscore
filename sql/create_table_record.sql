CREATE TABLE nutriscore.record (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    indivi_id INT NOT NULL,
    calories FLOAT NOT NULL,
    fat FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    carbohydrates FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);