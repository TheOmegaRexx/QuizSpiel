CREATE DATABASE IF NOT EXISTS quizdb;
USE quizdb;
CREATE TABLE IF NOT EXISTS quizfragen (
                            id INT NOT NULL AUTO_INCREMENT,
                            frage TEXT NOT NULL,
                            antworten TEXT NOT NULL,
                            richtige_antwort CHAR(1) NOT NULL,
                            PRIMARY KEY (id))