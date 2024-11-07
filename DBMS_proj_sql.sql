CREATE DATABASE dbms_project;
USE dbms_project;
-- 1. Create Team table (as other tables reference it)
CREATE TABLE Team (
    Team_ID INT PRIMARY KEY AUTO_INCREMENT,
    Team_Name VARCHAR(100)
);

-- 2. Create Mentor table (as Project references Mentor)
CREATE TABLE Mentor (
    Mentor_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Password VARCHAR(100),
    Department VARCHAR(100)
);
ALTER TABLE Mentor
ADD CONSTRAINT email_format CHECK (Email REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
ALTER TABLE Team ADD Mentor_ID INT;

-- 3. Create Project table (as Feedback and Evaluation reference Project)
CREATE TABLE Project (
    Project_ID INT PRIMARY KEY AUTO_INCREMENT,
    Project_Name VARCHAR(100),
    Initial_Draft VARCHAR(255),
    Final_Submission VARCHAR(255),
    Status ENUM('Not Started', 'In Progress', 'Completed'),
    Submission_Date DATE,
    Team_ID INT,
    Mentor_ID INT,
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Mentor_ID) REFERENCES Mentor(Mentor_ID)
);

-- 4. Create Student table (now it can reference Team)
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Password VARCHAR(100),
    Team_ID INT,
    Role ENUM('Student', 'Mentor'),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);

-- 5. Create Feedback table (after Project and Mentor are created)
CREATE TABLE Feedback (
    Feedback_ID INT PRIMARY KEY AUTO_INCREMENT,
    Project_ID INT,
    Mentor_ID INT,
    Comments TEXT,
    Date_Provided DATE,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID),
    FOREIGN KEY (Mentor_ID) REFERENCES Mentor(Mentor_ID)
);

-- 6. Create Panel table (before Evaluation references Panel)
CREATE TABLE Panel (
    Panel_ID INT PRIMARY KEY AUTO_INCREMENT,
    Panel_Name VARCHAR(100)
);

-- 7. Create Evaluation table (after Project and Panel are created)
CREATE TABLE Evaluation (
    Evaluation_ID INT PRIMARY KEY AUTO_INCREMENT,
    Project_ID INT,
    Panel_ID INT,
    Grade DECIMAL(3, 2),
    Comments TEXT,
    Evaluation_Date DATE,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID),  -- Now Project_ID can appear multiple times
    FOREIGN KEY (Panel_ID) REFERENCES Panel(Panel_ID)
);
show databases;
show table status;

-- Stored Procedures
-- Add Stud
DELIMITER //
CREATE PROCEDURE AddStudent(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100),
    IN p_team_id INT,
    IN p_role ENUM('Student', 'Mentor')
)
BEGIN
    INSERT INTO Student(Name, Email, Password, Team_ID, Role)
    VALUES (p_name, p_email, p_password, p_team_id, p_role);
END //
DELIMITER ;

-- Add Mentor
DELIMITER //
CREATE PROCEDURE AddMentor(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100),
    IN p_department VARCHAR(100)
)
BEGIN
    INSERT INTO Mentor(Name, Email, Password, Department)
    VALUES (p_name, p_email, p_password, p_department);
END //
DELIMITER ;

-- Add Project
DELIMITER //
CREATE PROCEDURE AddProject(
    IN p_name VARCHAR(100),
    IN p_team_id INT,
    IN p_mentor_id INT,
    IN p_status ENUM('Not Started', 'In Progress', 'Completed')
)
BEGIN
    INSERT INTO Project(Project_Name, Status, Team_ID, Mentor_ID)
    VALUES (p_name, p_status, p_team_id, p_mentor_id);
END //
DELIMITER ;

-- Get Team Info
DELIMITER $$
CREATE PROCEDURE get_team_info(IN student_id INT)
BEGIN
    SELECT 
        T.Team_Name,
        M.Name AS Mentor_Name,
        GROUP_CONCAT(S.Name SEPARATOR ', ') AS Team_Members,
        GROUP_CONCAT(E.Comments SEPARATOR '; ') AS Review
    FROM Team T
    JOIN Student S ON T.Team_ID = S.Team_ID
    JOIN Mentor M ON T.Mentor_ID = M.Mentor_ID
    LEFT JOIN Project P ON T.Team_ID = P.Team_ID  -- If projects relate to teams
    LEFT JOIN Evaluation E ON P.Project_ID = E.Project_ID  -- Assuming evaluations are linked to projects
    WHERE S.Student_ID = student_id
    GROUP BY T.Team_ID;
END$$
DELIMITER ;
drop procedure get_team_info;
USE dbms_project;

-- Get Student Info
DELIMITER //
CREATE PROCEDURE get_student_info(IN student_id INT)
BEGIN
    SELECT 
        T.Team_Name,
        M.Name AS Mentor_Name,
        (SELECT GROUP_CONCAT(S.Name SEPARATOR ', ') 
         FROM Student S WHERE S.Team_ID = T.Team_ID) AS Team_Members,
        F.Comments AS Review
    FROM Team T
    JOIN Student S ON T.Team_ID = S.Team_ID
    JOIN Mentor M ON T.Mentor_ID = M.Mentor_ID
    LEFT JOIN Feedback F ON T.Team_ID = F.Project_ID
    WHERE S.Student_ID = student_id;
END //
DELIMITER ;


-- Triggers
-- Trigger to log feedback when inserted
DELIMITER //
CREATE TRIGGER before_feedback_insert
BEFORE INSERT ON Feedback
FOR EACH ROW
BEGIN
    SET NEW.Date_Provided = CURDATE();
END //
DELIMITER ;

-- Trigger to update Project Status
DELIMITER //
CREATE TRIGGER after_project_update
AFTER UPDATE ON Project
FOR EACH ROW
BEGIN
    IF NEW.Final_Submission IS NOT NULL THEN
        UPDATE Project
        SET Status = 'Completed'
        WHERE Project_ID = NEW.Project_ID;
    END IF;
END //
DELIMITER ;

  
-- Additional Stored Procedures
-- Assign Team to a Project
DELIMITER //
CREATE PROCEDURE AssignTeamToProject(
    IN p_project_id INT,
    IN p_team_id INT
)
BEGIN
    UPDATE Project
    SET Team_ID = p_team_id
    WHERE Project_ID = p_project_id;
END //
DELIMITER ;

-- Stored Procedure For Evaluate 
DELIMITER //
CREATE PROCEDURE EvaluateProject(
    IN p_project_id INT,
    IN p_panel_id INT,
    IN p_grade DECIMAL(3, 2),
    IN p_comments TEXT
)
BEGIN
    INSERT INTO Evaluation(Project_ID, Panel_ID, Grade, Comments, Evaluation_Date)
    VALUES (p_project_id, p_panel_id, p_grade, p_comments, CURDATE());
END //
DELIMITER ;



-- Start Inserting Values 
INSERT INTO Mentor (Name, Email, Password, Department) VALUES 
('Prof NVP', 'nvp@gmail.com', 'password123', 'Computer Science'),
('Dr. Jayashree R', 'jayashree@gmail.com', 'password123', 'AIML'),
('Dr. Jawahar', 'jawahar@gmail.com', 'password123', 'Data Science'),
('Prof BJD', 'bjd@gmail.com', 'password123', 'AIML');

INSERT INTO Team (Team_Name, Mentor_ID) VALUES 
('Team Alpha',1),
('Team Beta',2),
('Team Gamma',4);

INSERT INTO Project (Project_Name, Initial_Draft, Final_Submission, Status, Submission_Date, Team_ID, Mentor_ID) VALUES 
('AI-Powered System', 'draft_v1.docx', 'final_v1.docx', 'In Progress', '2024-10-20', 1, 1),  -- Assigned to Team Alpha, Mentor Prof NVP
('ZKP-Blockchain Research', 'draft_v2.docx', 'final_v2.docx', 'Not Started', NULL, 2, 2);        -- Assigned to Team Beta, Mentor Dr. Jayashree R

INSERT INTO Student (Name, Email, Password, Team_ID, Role) VALUES 
('Adityanath Yogi', 'adityanath@gmail.com', 'yogi', 1, 'Student'),
('Narendra Modi', 'narendra@gmail.com', 'modi', 1, 'Student'),
('Amit Shah', 'amit@gmail.com', 'amit', 1, 'Student'),
('S Jayashankar', 'jayashankar@gmail.com', 'jayshankar', 1, 'Student');

INSERT INTO Student (Name, Email, Password, Team_ID, Role) VALUES 
('Kharge Mallikarjun', 'kharge@gmail.com', 'kharge', 2, 'Student'),
('Rahul Gandhi', 'rahul@gmail.com', 'rahul', 2, 'Student'),
('Priyanka Gandhi', 'priyanka@gmail.com', 'priyanka', 2, 'Student'),
('Manmohan Singh', 'manmohan@gmail.com', 'manmohan', 2, 'Student');

INSERT INTO Panel (Panel_Name) VALUES 
('ISA Panel'),
('ESA Panel');

SELECT * FROM student;