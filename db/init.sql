CREATE DATABASE mybooks;
use mybooks;

CREATE TABLE mybook (
  id INT NOT NULL AUTO_INCREMENT,
  author VARCHAR(50),
  title VARCHAR(50),
  isbn INT,
  PRIMARY KEY (id)
);

INSERT INTO mybook
  (author, title, isbn)
VALUES
  ('RANDRIA', 'Python', 1345674),
  ('RAKOTO', 'Devops', 156433);