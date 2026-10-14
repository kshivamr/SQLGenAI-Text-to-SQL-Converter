CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL
);

INSERT INTO employees (name, department, salary)
VALUES
('Rahul Sharma', 'IT', 75000),
('Aman Verma', 'HR', 55000),
('Priya Singh', 'IT', 82000),
('Rohit Kumar', 'Finance', 68000),
('Neha Gupta', 'Marketing', 60000),
('Arjun Mehta', 'IT', 95000),
('Sneha Patel', 'HR', 58000),
('Vikas Yadav', 'Finance', 72000),
('Anjali Sharma', 'Marketing', 65000),
('Karan Singh', 'IT', 88000);