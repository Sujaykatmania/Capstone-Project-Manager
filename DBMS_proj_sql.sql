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
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID),
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
