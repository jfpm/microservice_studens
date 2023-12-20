GRANT ALL PRIVILEGES ON . TO 'adminroot'@'%' IDENTIFIED BY 'rootroot1' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS userdb;
USE userdb;


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    perfil INTEGER NULL
    token VARCHAR(255) NULL
);