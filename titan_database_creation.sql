---------------------------------------------------------------
--------------CPSC-544-TEAM-1-PROJECT-TITANENROLL--------------
---------------------------------------------------------------
-----------------INITIAL DATABASE CREATION--------------------

---------------CREATE DATABASE - TITANENROLLDB------------
IF NOT EXISTS(SELECT name FROM sys.databases WHERE name='TITANENROLLDB')
     BEGIN
	   CREATE DATABASE TITANENROLLDB
	 END
GO
  USE TITANENROLLDB
GO

---------------------------------------------------------------
------------------ CREATE TABLES ---------------------------
---------------------------------------------------------------
---------------- Table 1. Department----------------------------
----------DEPARTMENT NUMBER: start:100 -------------------------------
IF OBJECT_ID('Department', 'U') IS NOT NULL
   BEGIN
		PRINT ' Department TABLE  ALREADY EXISTS'
   END
ELSE
   BEGIN
		CREATE TABLE Department(
		  DepartmentID Integer IDENTITY(100,1) NOT NULL PRIMARY KEY,
		  DepartmentName varchar(200) NOT NULL UNIQUE,
		  BuildingNumber Integer NOT NULL,
		  Email varchar(100) NOT NULL,
		  DepartmentContact Integer NOT NULL
		  )
   END

---------------------------------------------------------------------
----------------- 2. Program -----------------------------------
IF OBJECT_ID('Program', 'U') IS NOT NULL
   BEGIN
		PRINT 'Program TABLE  ALREADY EXISTS'
   END
ELSE
   BEGIN
		CREATE TABLE Program(
		  ProgramID Integer IDENTITY(1,1) NOT NULL PRIMARY KEY,
		  DepartmentID Integer NOT NULL FOREIGN KEY REFERENCES Department(DepartmentID),
		  Programname varchar(200) NOT NULL 
		  )
   END
--------------------------------------------------------------------------------
-------------------------- 3. Professor ------------------------------
----------------Professor ID Start: 2000 ---------------------------
IF OBJECT_ID('Professor', 'U') IS NOT NULL
   BEGIN
		PRINT 'Professor TABLE  ALREADY EXISTS'
   END
ELSE
   BEGIN
		CREATE TABLE Professor(
		  ProfessorID Integer IDENTITY(2000,1) NOT NULL PRIMARY KEY,
		  firstname varchar(50) NOT NULL,
		  lastname varchar(50) NOT NULL,
		  Email varchar(100) NOT NULL UNIQUE, 
		  DepartmentID Integer NOT NULL FOREIGN KEY REFERENCES Department(DepartmentID)
		  )
   END

--------------------------------------------------------------------------------
----------------------- 4. Student -------------------------------------------
----------------Stundet ID Start: 80000000 ---------------------------
IF OBJECT_ID('Student', 'U') IS NOT NULL
   BEGIN
		PRINT 'Student TABLE  ALREADY EXISTS'
   END
ELSE
   BEGIN
		CREATE TABLE Student(
		  StudentID Integer IDENTITY(80000000,1) NOT NULL PRIMARY KEY,
		  firstname varchar(50) NOT NULL,
		  lastname varchar(50) NOT NULL,
		  Email varchar(100) NOT NULL UNIQUE, 
		  username varchar(40) NOT NULL UNIQUE,
		  upassword varchar(10) NOT NULL CHECK(len(upassword)<=10),
		  admittedYear Integer NOT NULL CHECK(len(admittedYear)=4),
		  admittedSemester varchar(10) NOT NULL CHECK(admittedSemester in ('Fall', 'Winter','Spring','Summer')),
		  phonenumner VARCHAR(100) NOT NULL,
		  DepartmentID Integer NOT NULL FOREIGN KEY REFERENCES Department(DepartmentID),
		  ProgramID Integer NOT NULL FOREIGN KEY REFERENCES Program(ProgramID)
		  )
   END

--------------------------------------------------------------------------------
-------------------- 5. Courses -----------------------------------------------
IF OBJECT_ID('Courses', 'U') IS NOT NULL
   BEGIN
		PRINT ' Courses TABLE  ALREADY EXISTS'
   END
ELSE
   BEGIN
		CREATE TABLE Courses(
		  CourseID varchar(10) NOT NULL PRIMARY KEY,
		  CoursesName varchar(200) NOT NULL UNIQUE,
		  CourseDescription text NOT NULL,
		  Subject varchar(200) NOT NULL,
		  Unit Integer NOT NULL,
		  ProgramID Integer NOT NULL FOREIGN KEY REFERENCES Program(ProgramID)
		  )
   END
------------------------------------------------------------------------------
------------------------- 6. Classes ----------------------------------------
------------------- classID start at 57000-----------------------------------
IF OBJECT_ID('Classes', 'U') IS NOT NULL
   BEGIN
		PRINT ' Classes TABLE  ALREADY EXISTS'
   END
ELSE
   BEGIN
		CREATE TABLE Classes(
		  ClassID Integer IDENTITY(57000,1) NOT NULL PRIMARY KEY,
		  Location varchar(50) NOT NULL,
		  Semester varchar(50) NOT NULL CHECK(Semester in ('Fall','Winter','Spring','Summner')),
		  SemesterYear varchar(4) NOT NULL,
		  startdate Date NOT NULL,
		  enddate Date NOT NULL,
		  days varchar(30) NOT NULL,
		  starttime varchar(50) NOT NULL,
		  endtime varchar(50) NOT NULL,
		  classCapacity Integer NOT NULL,
		  Enrolled Integer NULL,
		  RemainingSeats Integer NULL,
		  Status varchar(20) NOT NULL,
		  CourseID varchar(10) NOT NULL FOREIGN KEY REFERENCES Courses(CourseID),
		  ProfessorID Integer NOT NULL FOREIGN KEY REFERENCES Professor(ProfessorID)
		  )
   END
-----------------------------------------------------------------------------------------
--------------------------- 7. classStudentList ---------------------------------------
IF OBJECT_ID('classStudentList', 'U') IS NOT NULL
   BEGIN
		PRINT 'classStudentList TABLE  ALREADY EXISTS'
   END
ELSE
   BEGIN
		CREATE TABLE classStudentList(
		  classID Integer NOT NULL FOREIGN KEY REFERENCES Classes(ClassID),
		  studentID Integer NOT NULL FOREIGN KEY REFERENCES Student(StudentID),
		  PRIMARY KEY (classID,studentID),

		  )
   END
-----------------------------------------------------------------------------------
-----------------------------------------------------------------------------------