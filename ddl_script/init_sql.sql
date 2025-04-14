CREATE DATABASE IF NOT EXISTS companydb;

USE companydb;

CREATE TABLE IF NOT EXISTS department (
    department_id INT COMMENT 'Id of the department',
    department_name VARCHAR(100) COMMENT 'Name of the department',
    creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Row creation timestamp',
    PRIMARY KEY (department_id)
);

CREATE TABLE IF NOT EXISTS job (
    job_id INT COMMENT 'Id of the job',
    job_name VARCHAR(100) COMMENT 'Name of the job',
    creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Row creation timestamp',
    PRIMARY KEY (job_id)
);

CREATE TABLE IF NOT EXISTS hired_employee (
    employee_id INT NOT NULL COMMENT 'Id of the employee',
    employee_name VARCHAR(200) NOT NULL COMMENT 'Name and surname of the employee',
    hiring_datetime VARCHAR(20) NOT NULL COMMENT 'Hiring datetime in ISO format',
    department_id INT NOT NULL COMMENT 'Id of the department which the employee was hired for',
    job_id INT NOT NULL COMMENT 'Id of the job which the employee was hired for',
    creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Row creation timestamp',
    PRIMARY KEY (employee_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);

GRANT ALL PRIVILEGES ON *.* TO 'jechu'@'%';