# TitanEnrollApp
### Project: TITANENROLLAPP- MOBILEAPP- ANDROID APP(KIVY)

--------------------------------------------------------
#### GOAL (PURPOSE)
* Developing a mobile app and practicing the Agile Scrum software development process are integral parts of this project. 
* This app allows for two core functions, the first is showing a course catalog and the second is allowing enrollment in classes.
 -----------------------------------------------------------
#### DEMO:


https://github.com/nidhishah989/TitanEnroll-MobileApp-Android--Kivy-Kivymd/assets/69876607/729adc0d-ae88-4f07-93ee-454a4769fed7


------------------------------------------------
#### Project Detail
The goal of this project is to apply Agile-Scrum to software process. It's about a mobile application for students of the CSUF collage that lets them access information about the classes they are taking in future and allows them to enroll. This is a mobile application made with Kivy and Kivymd. The database (locally stored) is MSSQL. There are five UI pages - MainPage, SelectionPage, CourseCatalogPage, LoginPage, EnrollmentPage.

--------------------------------------------------------
#### PROJECT REQUIRE MODULES/libraries 

* kivy
* kivymd
* pyodbc
* datetime

-----------------------------------------------------
#### project Structure
```bash
 TITANENROLL-KIVYMOBILEAPP
 |-- main.py
 |-- databaseconnection.py
 |-- pagescreen.kv
 |-- titan_database_creation.sql
 |-- titan_DataInsertion.sql
 |-- Images/  
 |-- README.md
 ```

--------------------------------------------------------------------
#### Project details - Course Catalog Service
 The students can view lists of courses and the details of each course, such as unit number, description, etc.
 
-----------------------------------------------------------------
#### Project details - Enrollment Service
1. The Enrollment page is only accessible to authorized students.
2. Students can login before accessing the Enrollment page.
3. The Enrollment page displays the student's registered classes.

4. On the enrollment page, students can also see the available courses they can enroll in. 
5. When student selects a class to enroll in, it will be added to his/her cart. 

6. When the student clicks Enroll, the program will check if the time clashes with another already enrolled class and see if the class is still available to enroll and if the student has already enrolled in the same course.
7. The last step is to show the student the message for all classes in the cart - either error or success Enrollment.

--------------------------------------------------------------------
#### Note:
The RecycleGridLayout is downloaded from latest version of kivy from github

