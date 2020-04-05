CREATE DATABASE db DEFAULT CHARACTER SET utf8mb4;
CREATE USER admin@localhost IDENTIFIED BY 'admin';
GRANT ALL ON db.* TO admin@localhost;
commit;
