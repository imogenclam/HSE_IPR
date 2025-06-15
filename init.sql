CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    priority VARCHAR(50) DEFAULT 'medium',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_task_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_task_priority ON tasks(priority);


INSERT INTO tasks (title, description, status, priority)
VALUES 
    ('Первая задача', 'Пример описания', 'pending', 'medium'),
    ('Вторая задача', 'Еще одно описание', 'completed', 'high')
ON CONFLICT DO NOTHING;