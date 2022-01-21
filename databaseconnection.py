############ Nidhi_Shah: TitanEnrollAPP - Database...setup and queries.
####################################################################
""" This file have all queries to run on database TITANENROLLDB"""
""" All functions will be called and run the query"""

# pyodbc is the module to connect to sql server
import pyodbc as connector
#connection string with needed information
""" The server name will be differ for all partners"""
connection_string=(r"Driver={SQL Server};"
               r"Server=DESKTOP-DNU7FUC;" # please change this to your server--> run 'select @@SERVERNAME' in sql studio to find your server
               r"Database=TITANENROLLDB;"
               r"Trusted_Connection=yes;")

#connect to the server and database under that server
conn= connector.connect(connection_string)

#create a cursor to work on the database
cur=conn.cursor()

###################################################################
#################### get the list of available courses
def getlistofavailablecourses(username):
   
   """ This function will find the classes avaiable to enroll for the logged in student based on enrolled program and department."""
   studentid=""
   programid=""
   
   # query to get the studentid and program details of logged in user
   cur.execute("""SELECT Student.StudentID,Student.ProgramID from Student 
                     where Student.username=?""", username)
   for i in cur:
      studentid=i[0]
      programid=i[1]
  
  # query will get all available courses but will exclude those classes in which user already have enrolled
   cur.execute(f"""SELECT Courses.CourseID,Classes.ClassID,Courses.CoursesName,Professor.firstname+Professor.lastname,Classes.Semester+Classes.SemesterYear,Classes.days,Classes.startdate,Classes.enddate,Classes.starttime,Classes.endtime,Classes.classCapacity,Classes.RemainingSeats,Courses.Unit FROM Courses 
                  INNER JOIN Classes
                     ON Courses.CourseID = Classes.CourseID 
	 	            INNER JOIN Professor
	 				      ON Classes.ProfessorID = Professor.ProfessorID
		            where  Courses.ProgramID={programid} and not Exists (select classStudentList.classID from classStudentList where classStudentList.studentID={studentid} and classStudentList.classID=Classes.ClassID)""")
   
   availabledata=[]             
   for i in cur:
      availabledata.append(i)
   return availabledata

###################################################################
############################# get the list of registered courses by a student
def getlistofregisteredcourses(username):
   """ This function will find the classes avaiable to enroll for the logged in student based on enrolled program and department."""
   studentid=""
   programid=""
   
   # query to get the studentid and program details of logged in user
   cur.execute("""SELECT Student.StudentID,Student.ProgramID from Student 
                     where Student.username=?""", username)
   for i in cur:
      studentid=i[0]
      programid=i[1]
   
  # query will get all available courses but will exclude those classes in which user already have enrolled
   cur.execute(f"""SELECT Courses.CourseID,Classes.ClassID,Courses.CoursesName,Professor.firstname+Professor.lastname,Classes.Semester+Classes.SemesterYear,Classes.days,Classes.startdate,Classes.enddate,Classes.starttime,Classes.endtime,Courses.Unit FROM Classes 
        INNER JOIN Courses 
                      ON Courses.CourseID = Classes.CourseID 
	 	INNER JOIN Professor
	 				 ON Classes.ProfessorID = Professor.ProfessorID
		
		where  Courses.ProgramID={programid} and Exists (select classStudentList.classID from classStudentList where classStudentList.studentID={studentid} and classStudentList.classID=Classes.ClassID)""")
  
   
   registeredclasses=[]             
   for i in cur:
      registeredclasses.append(i)
   return registeredclasses

############################################ FOR COURSE CATALOG PAGE
# get list of courses by dept and prgm
def getlistofcourses(department,program):
   
  # query will get all courses on selected department and program
   cur.execute(f"""SELECT Courses.CourseID,Courses.CoursesName,Courses.CourseDescription,Courses.Unit FROM Courses 
                  JOIN Program 
                     ON Courses.ProgramID = Program.ProgramID 
                  JOIN Department
                  ON Program.DepartmentID = Department.DepartmentID
                  Where Department.DepartmentName='{department}' AND Program.Programname='{program}'""")


 # print the list of query result
   courselist=[]
   for i in cur:
      course=[]
      for j in i:
         course.append(j)
      courselist.append(course)
   
   return courselist
###################################################### For LOgin authentication
### To authenticate user credentials
def authenticateUser(username,password):
      if username=="" or password=="":
         return False
      else:
         cur.execute(f"""SELECT Student.StudentID FROM Student WHERE username='{username}' AND upassword='{password}'""")
         
         
         for i in cur:
            return i[0]
         

##########################################################################
### function for class registration (enrollment) #################
   # This function will take input of classid and and studentid
   # First: It will check the class have available seats or not. 
   # If there is available seat, then it will update with one addition of enrollment.
   # After fixing that, It will update the classstudentlist with studentid and classid

#enroll into a class based on selection and throw the error, if any
def classenrollment(studentid,classid):
   
   capacity=0
   remaining=0
   enrolled=0
   state=""
   # query to get current remaining seats with class capacity
   cur.execute(f"""SELECT Classes.classCapacity,Classes.RemainingSeats,Classes.Enrolled,Classes.Status FROM Classes Where Classes.ClassID={classid}""")

   # getting the remaining and class capacity data into variable
   for data in cur:
      capacity=data[0]
      #print('capacity',capacity)
      remaining=data[1]
      #print('remaining',remaining)
      enrolled=data[2]
      #print('enrolled',enrolled)
      state=data[3]
      #print('state',state)
   
   # If the remaining seats are less than classcapasity, then enroll student and update the database
   #else send a message that class is fully enrolled, cannot enroll in this class.
   if (remaining <= capacity) and (state=="Available"):
     # print("HAPPENING")
      remaining = remaining - 1
     # print('new remaining',remaining)
      enrolled= enrolled + 1
     # print('new enrolled',enrolled)
      #Before doing update - check the enrolled and capacity is equal or not to change class status
      if enrolled == capacity:
         state="Close"
     
      try:
       
         # Query to insert student record with enrolled class.
         cur.execute(f""" INSERT INTO classStudentList VALUES ({classid},{studentid})""")
         conn.commit()
         # Query to update that class information that neeeded for enrollment functionality
         cur.execute(f"""UPDATE Classes SET Classes.RemainingSeats={remaining}, Classes.Enrolled={enrolled},Classes.Status='{state}' Where Classes.ClassID={classid} """)
         cur.commit()
         return {'success':f"Successfully Enrolled"}
      except Exception as e:
         
         #if the exception is the duplciate entry in classStudentList - means student is trying to enroll in class which is already enrolled by that student
         if(e.args[0]== '23000'):
            return f' You are trying to enroll the class in which you are already enrolled.'
     
     
   elif (enrolled==capacity) and (state=="Close"):
      return {'error':f"You cannot enroll this class because it is already Fully Enrolled."}