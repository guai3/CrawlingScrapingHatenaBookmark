CREATE TABLE comment(
id BIGINT(7) NOT NULL AUTO_INCREMENT,
bookmarkid BIGINT(7),
user VARCHAR(30),
content VARCHAR(300),
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(id));

ALTER TABLE comment CHANGE content content VARCHAR(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
