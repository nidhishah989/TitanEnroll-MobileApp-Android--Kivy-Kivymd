---------------------------------------------------------------
--------------CPSC-544-TEAM-1-PROJECT-TITANENROLL--------------
---------------------------------------------------------------
------- INSERTION OPERATION TO PREPARE DATABASE FOR APP--------
---------------------------------------------------------------
IF EXISTS(SELECT name FROM sys.databases WHERE name='TITANENROLLDB')
     BEGIN
		   USE TITANENROLLDB
		   --------------------------------------------------------------
		   --------------- INSERT DATA IN Department-------------------
		   IF OBJECT_ID('Department', 'U') IS NULL
			 BEGIN
				PRINT ' Department TABLE DOES NOT EXISTS'
			END
		   ELSE
			 BEGIN
				INSERT INTO Department
				VALUES('Computer Science',522,'computersciencecsuf@gmail.com',949)
			 END
		   --------------------------------------------------------------
		   --------------- INSERT DATA IN Program------------------------
		   IF OBJECT_ID('Program', 'U') IS NULL
			 BEGIN
				PRINT ' Program TABLE DOES NOT EXISTS'
			END
		   ELSE
			 BEGIN
				INSERT INTO Program(Programname, DepartmentID)
				VALUES('Bachelor in Computer Science',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science')),
				      ('Master in Computer Science',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'))
			 END
		   --------------------------------------------------------------
		   --------------- INSERT DATA IN Courses ------------------------
		   IF OBJECT_ID('Courses', 'U') IS NULL
			 BEGIN
				PRINT ' Courses TABLE DOES NOT EXISTS'
			END
		   ELSE
			 BEGIN
				INSERT INTO Courses
				VALUES('CPSC120','Introduction to Programming','Introduction to the concepts underlying all computer programming:design and execution of programs; sequential nature of programs; use of assignment, control and input/output statements to accomplish desired tasks; design and use of functions. Structured and object-oriented methodologies. (1.5 hours lecture, 3 hours laboratory) Corequisite: MATH 125.','Computer Science',3,(SELECT ProgramID FROM Program WHERE Programname='Bachelor in Computer Science')),
				      ('CPSC121','Object-oriented programming','The object-oriented programming paradigm: classes, member functions, interfaces, inheritance, polymorphism, and exceptions. Design practices including encapsulation, decoupling, and documentation. Pointers/references and memory management. Recursion. (2 hours lecture, 2 hours activity) Prerequisite: CPSC 120 or passing score on Computer Science Placement Exam.','Computer Science',3,(SELECT ProgramID FROM Program WHERE Programname='Bachelor in Computer Science')),
					  ('CPSC531','Advanced Database Management','Implementation techniques for query analysis, data allocation, concurrency control, data structures and distributed databases. New database models and recent developments in database technology. Student projects directed to specific design problems. CPSC 431 recommended.','Computer Science',3,(SELECT ProgramID FROM Program WHERE Programname='Master in Computer Science')),
					  ('CPSC544','Advanced Software Process','Advanced guidance for defining and improving the software development process. Concepts of software maturity framework, principles of process improvement and software process assessment. Current topics such as CMMI and SCAMPI. CPSC 362 recommended.','Computer Science',3,(SELECT ProgramID FROM Program WHERE Programname='Master in Computer Science'))
			 END
		 --------------------------------------------------------------
		   --------------- INSERT DATA IN student------------------------
		   IF OBJECT_ID('Student', 'U') IS NULL
			 BEGIN
				PRINT ' Student TABLE DOES NOT EXISTS'
			END
		   ELSE
			 BEGIN
				INSERT INTO Student
				VALUES('nidhi','shah','nidhishahtrial@gmail.com','nidhi12','1234',2019,'Fall','949-342-1121',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'),(SELECT ProgramID FROM Program WHERE Programname='Master in Computer Science')),
				      ('kavita','shah','kavtrial@gmail.com','kav12','1234',2019,'Winter','949-312-1121',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'),(SELECT ProgramID FROM Program WHERE Programname='Bachelor in Computer Science')),
					  ('dolly','shah','dolly@gmail.com','doll12','1234',2019,'Winter','949-312-1121',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'),(SELECT ProgramID FROM Program WHERE Programname='Bachelor in Computer Science')),
					  ('kushal','shah','kush@gmail.com','kush12','1234',2019,'Winter','949-312-1121',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'),(SELECT ProgramID FROM Program WHERE Programname='Bachelor in Computer Science')),
					  ('nisarg','shah','nisarg@gmail.com','nis12','1234',2019,'Fall','949-342-1121',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'),(SELECT ProgramID FROM Program WHERE Programname='Master in Computer Science')),
					  ('rakesh','shah','rakesh@gmail.com','rb12','1234',2019,'Fall','949-342-1121',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'),(SELECT ProgramID FROM Program WHERE Programname='Master in Computer Science'))
					  
			 END
		--------------------------------------------------------------
		   --------------- INSERT DATA IN Professor------------------------
		   IF OBJECT_ID('Professor', 'U') IS NULL
			 BEGIN
				PRINT ' Professor TABLE DOES NOT EXISTS'
			END
		   ELSE
			 BEGIN
				INSERT INTO Professor
				VALUES('Doina','Bein','doinabein@gmail.com',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science')),
				      ('Suchi','Pati','Spati@gmail.com',(SELECT DepartmentID FROM DEPARTMENT WHERE DepartmentName='Computer Science'))
			 END
		 --------------------------------------------------------------
		   --------------- INSERT DATA IN Program------------------------
		   IF OBJECT_ID('Classes', 'U') IS NULL
			 BEGIN
				PRINT ' Classes TABLE DOES NOT EXISTS'
			END
		   ELSE
			 BEGIN
				INSERT INTO Classes
				VALUES('CS-201','Spring','2022','1/21/2022','5/18/2022','MW','8:30AM','10:00AM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC120'),(SELECT ProfessorID FROM Professor WHERE firstname='Doina' and lastname='Bein')),
				      ('CS-201','Spring','2022','1/21/2022','5/18/2022','TTH','8:30AM','10:00AM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC121'),(SELECT ProfessorID FROM Professor WHERE firstname='Doina' and lastname='Bein')),
					  ('CS-401','Spring','2022','1/21/2022','5/18/2022','MW','8:30AM','10:00AM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC120'),(SELECT ProfessorID FROM Professor WHERE firstname='Suchi' and lastname='Pati')),
					  ('CS-201','Spring','2022','1/21/2022','5/18/2022','TTH','10:30AM','12:15PM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC531'),(SELECT ProfessorID FROM Professor WHERE firstname='Suchi' and lastname='Pati')),
					  ('CS-301','Spring','2022','1/21/2022','5/18/2022','MW','10:30AM','12:15PM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC544'),(SELECT ProfessorID FROM Professor WHERE firstname='Doina' and lastname='Bein')),
					  ('CS-301','Spring','2022','1/21/2022','5/18/2022','MW','1:30PM','3:00PM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC544'),(SELECT ProfessorID FROM Professor WHERE firstname='Doina' and lastname='Bein')),
					  ('CS-301','Spring','2022','1/21/2022','5/18/2022','MW','1:30PM','3:15PM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC121'),(SELECT ProfessorID FROM Professor WHERE firstname='Suchi' and lastname='Pati')),
					  ('CS-301','Spring','2022','1/21/2022','5/18/2022','MW','1:30PM','3:00PM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC544'),(SELECT ProfessorID FROM Professor WHERE firstname='Doina' and lastname='Bein')),
					  ('CS-301','Spring','2022','1/21/2022','5/18/2022','MW','8:30AM','10:00AM',30,0,30,'Available',(SELECT CourseID FROM Courses WHERE CourseID='CPSC121'),(SELECT ProfessorID FROM Professor WHERE firstname='Suchi' and lastname='Pati'))

			 END
	 END
ELSE 
   PRINT 'THE TITANENROLLDB DATABASE NOT FOUND'



  