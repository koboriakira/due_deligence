CREATE DATABASE due_deligence DEFAULT CHARACTER SET utf8mb4;
CREATE USER admin@localhost IDENTIFIED BY 'admin';
GRANT ALL ON due_deligence.* TO admin@localhost;
commit;
