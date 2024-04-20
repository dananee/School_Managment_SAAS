CREATE TABLE Notification (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(2) DEFAULT 'SF' CHECK (role IN ('OW', 'SF', 'TE', 'ST', 'PT')),
    message VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author VARCHAR(100),
    status VARCHAR(2) DEFAULT 'IM' CHECK (status IN ('WR', 'IM', 'EV')),
    read BOOL DEFAULT FALSE,
    sender_id BIGINT,
    FOREIGN KEY (sender_id) REFERENCES SchoolMembers(id) ON DELETE CASCADE
);