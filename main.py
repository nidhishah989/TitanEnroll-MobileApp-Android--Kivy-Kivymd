############ Nidhi_Shah: TitanEnrollAPP - Main file... App startup..
####################################################################
# from typing import Text
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from databaseconnection import getlistofcourses
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.expansionpanel import MDExpansionPanel,MDExpansionPanelTwoLine
from kivymd.uix.list import TwoLineListItem,OneLineListItem
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from databaseconnection import getlistofavailablecourses
from databaseconnection import getlistofregisteredcourses
from kivymd.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDIconButton
from kivymd.uix.toolbar import MDToolbar
from databaseconnection import authenticateUser
from databaseconnection import classenrollment
from datetime import datetime
#from kivy.clock import Clock

# store student id for enrollment page
studentID = ''

############################# HOme page #######################################
class HomePage(MDScreen):
    pass
################################ LOGIN Page ######################################
class LoginPage(MDScreen):
    # variables from pagescreen and other declaration
    dialog = None
    user=ObjectProperty(None)
    password=ObjectProperty(None)
    # on_pre_Enter function will be run before the page comes on screen
    def on_pre_enter(self, *args):
        # clearing the usernmae and password text for nee screen
        self.manager.get_screen('loginpage').user.text=""
        self.manager.get_screen('loginpage').password.text=""
    
    # function when there is error in login.. show user a message for that
    def ShowLoginErrorMessage(self,mesage):
        msg=mesage
        # if not self.dialog:
        self.dialog = MDDialog(
            title= "Login Error!!",
            text = f" {msg} ",
            padding=120,
            buttons=[
                    MDFlatButton(
                        text="Try Again", text_color=self.specific_secondary_text_color,
                        on_press= self.close_dialog,
                    ),
                ],
        )
        self.dialog.open()  
    
    #closing the dialog message box
    def close_dialog(self,object):
        self.dialog.dismiss()

    # when user press login button, this function will work, get the username and password that
    # user have enter, call database function for authentication checking. show the message if authentication is not approved.
    def Login(self,username,password):
        global studentID
        # error - nothing has given
        if(len(username)==0 and len(password)==0):
            self.ShowLoginErrorMessage("Username and Password both required to LOGIN.")
        else:
            # call the authentication database function and get studentid
            self.studentiD = authenticateUser(username,password)
            # call enrollmentpage for that student information
            if self.studentiD:
                studentID = self.studentiD
                self.manager.current = "enrollmentpage"
            else:
                self.ShowLoginErrorMessage("Invalid username/password.")                    
    
############################## ENROLLMENT PAGE ##############################################
#enrollment page data and functions
class EnrollmentPage(MDScreen):
    dialog = None #dialog to show when enrollment is completed
    registeredcourseslist =ObjectProperty(None)
    availablecourseslist=ObjectProperty(None) #id to track
    loginfo=ObjectProperty(None)
    cart =[]
    row=[]
    regcls=[]
    msgs=""
    ################################### on_ente Event #############################
    def on_enter(self, *args):
        """ Function for: On_enter Enrollment page creation.. with data.
            1. FInd the already registred classes of student who is signed in.
            2. Find the available classes according to student's enrolled department and program.
            3. Allow student to enroll in the class with adding and removing class from the cart.
            4. Enroll Button to Enroll in class with class comflict and time comflict validation check"""
        
        self.cart=[]
        self.row=[]
        self.regcls=[]
        self.msgs=""
        ################################ Change toolbar value #################
        username = self.manager.get_screen('loginpage').user.text
        self.manager.get_screen('enrollmentpage').loginfo.title=f'Welcome      {username}'
        ####################################################################
        layout = GridLayout(rows=5,row_default_height=24) # create a layout
        layout1 = GridLayout(rows=5,row_default_height=24) # create a layout
        self.manager.get_screen('enrollmentpage').availablecourseslist.clear_widgets() #clear widgets
        self.manager.get_screen('enrollmentpage').registeredcourseslist.clear_widgets()
        #get the available classes to register for user...
        dbList = getlistofavailablecourses(username)
       
        #get the classes that user have already registered..
        registeredcourses = getlistofregisteredcourses(username) # student ID
        
        # student is not registred, so show that text in label instead of mdtable
        if not registeredcourses:
            self.manager.get_screen('enrollmentpage').registeredcourseslist.add_widget(MDLabel(text="You are not yet registered into any course for this semester.",halign= "center",theme_text_color= "Custom",text_color= (1, 1, 1, 1),font_style="H5"))
       
        # student have registered classes, so show them in mdtable.
        else:
            self.regcls = registeredcourses
            registeredtable = MDDataTable(
                size_hint=(1, None),						#size
                height= 200,
                #define column data
                column_data=[
                    ("CourseID", dp(27)),
                    ("ClassID", dp(15)),
                    ("Course Name", dp(30)),
                    ("Prefessor Name", dp(30)),
                    ("Semester",dp(22)),
                    ("Days",dp(10)),
                    ("Start Date",dp(20)),
                    ("End Date",dp(20)),
                    ("Start At", dp(15)),
                    ("End At",dp(15)),
                    ("Units",dp(10)),
                ],
                #define row data
                row_data=registeredcourses
            )  
            layout1.add_widget(registeredtable)
            self.manager.get_screen('enrollmentpage').registeredcourseslist.add_widget(layout1) 

        # if there are no available classes to enroll, show this message.
        if not dbList:
            self.manager.get_screen('enrollmentpage').availablecourseslist.add_widget(MDLabel(text="Currently there are no available courses for this semester.",halign= "center",theme_text_color= "Custom",text_color= (1, 1, 1, 1),font_style="H5"))
        
        # there are some classes to enroll, show them in mdtable
        else:    
            
            availtable= MDDataTable(
                size_hint=(1, None),						#size
                height= 200,
                check=True,
                #define column data
                column_data=[
                    ("CourseID", dp(27)),
                    ("ClassID", dp(15)),
                    ("Course Name", dp(30)),
                    ("Prefessor Name", dp(30)),
                    ("Semester",dp(22)),
                    ("Days",dp(10)),
                    ("Start Date",dp(20)),
                    ("End Date",dp(20)),
                    ("Start At", dp(15)),
                    ("End At",dp(15)),
                    ("Total Seats",dp(14)),
                    ("Remaining Slots", dp(20)),
                    ("Units",dp(10))
                ],
               
                row_data= dbList
            )
            availtable.bind(on_check_press=self.checked)  
            layout.add_widget(availtable) 
            self.manager.get_screen('enrollmentpage').availablecourseslist.add_widget(layout) 
            
    ######################## Enroll button event ##############  
    def finalcheck(self):
        global studentID
        """ Fuction will: 
               1. Access the cart, compare the courseID with already registered classes..
                   if similar courseID, will save message for not possible registration as you already have enrolled in this course.
                   if different courseID, will match the days, if days match with any registered classes, will check time conflicts.
                   If everything okay means days different and with days same, no time conflict, will call enroll function.
                   All messages will be shown to the user.."""
        #checking cart is empty or not, if empty, show error
        if self.cart:
            #cart is not empty..
            self.tconflict=False
            # take one class from cart at a time, and proceed.
            for cls in self.cart:
                # checking the user have any register classes or not, 
                if  self.regcls:
                    # user have register classes..
                    # find if user have registered any class of similar CourseID.. if so, show cannot register new class.
                    # Note: not doing the drop service in the app...
                    find=any(cls[0] in regclss for regclss in self.regcls)
                    if find is True:
                        self.msgs=self.msgs+f'Error: you have enrolled other section of CourseID {cls[0]}. \n'
                    # if no similar course have registered, check the time conflict..with other registered classes
                    else:
                        # check with all registered classes..
                        for rcls in self.regcls:
                            # matching days first..
                            if cls[5]==rcls[5]:
                                # days matched, check the time conflicts now.
                                # good condition: new class starttime< registered class starttime and new class endtime<registered class endtime
                                if datetime.strptime(cls[8],"%I:%M%p")< datetime.strptime(rcls[8],"%I:%M%p"):
                                    if datetime.strptime(cls[9],"%I:%M%p")< datetime.strptime(rcls[8],"%I:%M%p"):
                                        print("good to go")
                                    else:
                                       # print("time -clash")
                                        self.tconflict=True
                                        self.msgs= self.msgs+f'Error: Time conflict for class {cls[1]} with class {rcls[1]}.\n'
                                # good condition: new class starttime>registered class starttime and >registered class endtime..
                                elif datetime.strptime(cls[8],"%I:%M%p")> datetime.strptime(rcls[8],"%I:%M%p"):
                                    if datetime.strptime(cls[8],"%I:%M%p")> datetime.strptime(rcls[9],"%I:%M%p"):
                                        print("good to go")
                                    else:
                                        print("time -clash")
                                        self.tconflict=True
                                        self.msgs= self.msgs+f'Error: Time conflict for class {cls[1]} with class {rcls[1]}.\n'
                        # if there is no conflict, we can register class
                        if self.tconflict == False:
                            msg=classenrollment(studentID,cls[1])
                           
                            if 'success' in msg.keys():
                                print("class is registered")
                                self.msgs= self.msgs+f'Success: The class {cls[1]} is registered.\n'
                                self.regcls.append(cls)
                               
                            else:
                                self.msgs=self.msgs+f'Error: Internal error, cannot enroll class {cls[1]}.\n'

                else:
                    msg=classenrollment(studentID,cls[1])
                    if 'success' in msg.keys():
                        print("class is registered")
                        self.msgs= self.msgs+f'Success: The class {cls[1]} is registered.\n'
                        self.regcls.append(cls)
                    else:
                        self.msgs.append(f'Error: Internal error, cannot enroll class {cls[1]}.\n') 

            # final dialog box to show all errors and messages
            self.dialog = MDDialog(
            title= "Result.",
            auto_dismiss=False,
            text = self.msgs,
            buttons=[
                    MDFlatButton(
                        text="Close", text_color=self.specific_secondary_text_color,
                        on_press=self.reload,
                    ),
                ],
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
            title= "Error.",
            auto_dismiss=False,
            text = "Cart is empty.",
            buttons=[
                    MDFlatButton(
                        text="Close", text_color=self.specific_secondary_text_color,
                        on_press=self.dialog_close,
                    ),
                ],
            )
            self.dialog.open()
        
        
    # reload the enrollment page
    def reload(self,args):
        self.dialog.dismiss()
        self.on_enter()

    #close dialog when clicked on close button
    def dialog_close(self, obj):
        self.dialog.dismiss()
    
    ######################## ADD class in cart
    def addincart(self,agrs):
        self.cart.append(self.row)
        self.dialog.dismiss()
    ######################## Remove class from cart
    def removefromcart(self,args):
        self.cart.remove(self.row)
        self.dialog.dismiss()
    ####################################################################
    #clicked on the row to enroll
    # this function will check that is the class added already in cart or not
    ###########if the class present in cart, means user want to remove it from list-
    ########### show the message to ask : Do you want to remove from the cart or not
    ########### if yes: remove from cart, if no: don't do anything
    ###
    ########## if the class is not present in cart, means user want to add class to enroll
    ########## show the message to confirm the class addition in cart
    ########## if yes: ass in cart, if no: remove the checked mark.
    def checked(self, instance_table, current_row):
        self.row=current_row
        if current_row not in self.cart:
            self.dialog = MDDialog(
            title= "Confirmatio on cart addition.",
            auto_dismiss=False,
            text = f"adding class {current_row[1]} in your Enrollment cart.",
            buttons=[
                    MDFlatButton(
                        text="Confirm", text_color=self.specific_secondary_text_color,
                        on_press= self.addincart,
                    ),
                ],
        )

        elif current_row in self.cart:
            self.dialog = MDDialog(
            title= "Confirmatio on removal.",
            auto_dismiss=False,
            text = f"Removing class{current_row[1]} from your Enrollment cart.",
            buttons=[
                    MDFlatButton(
                        text="Confirm", text_color=self.specific_secondary_text_color,
                        on_press= self.removefromcart,
                    ),
                ],
        )
        self.dialog.open()
   
                                                      
########################## SELECTION PAGE #################################################
class SelectionPage(MDScreen):
   
    spinner_dept = ObjectProperty()
    spinner_prog = ObjectProperty()
   
    def on_enter(self, *args):
        self.manager.get_screen('selectionpage').spinner_dept.text="Select Department"
        self.manager.get_screen('selectionpage').spinner_prog.text="Select Program"
        
    def spinner_clicked(self,value):
        print(value)
        print(self.manager.get_screen('selectionpage').spinner_dept.text )
    def spinner_clicked_prog(self,value):
        print(value)
        print(self.manager.get_screen('selectionpage').spinner_prog.text )
    

################################# COURSE CATALOG PAGE ###################################
# ##################### CARD CONTENT CREATION ################################## 
class content2(BoxLayout):
    coursedesc=ObjectProperty(None)
    courseunit=ObjectProperty(None)


############################# COURSE CATALOG PAGE #################################
class CourseCatalogPage(MDScreen):
    displaycatalog=ObjectProperty(None)
    selectedeptandprogram=ObjectProperty(None)

    deaprtment=''
    program=''
    def on_enter(self, *args):
        # get the value of ids from screen 1 to screen2
    
        self.deaprtment= self.manager.get_screen('selectionpage').spinner_dept.text
        self.program = self.manager.get_screen('selectionpage').spinner_prog.text
      
        ##adjusting department and program selection values for database query
        
        if(self.deaprtment == "computer science"):
            self.deaprtment = "Computer Science"
        if(self.program == "Master" ):
            self.program = "Master in Computer Science"
        elif (self.program == "Bachelor" ):
            self.program = "Bachelor in Computer Science"
            
        self.manager.get_screen('catalogpage').selectedeptandprogram.text=f'Course Catalog For \n Department: {self.deaprtment} \nProgram: {self.program}'
        
        #call the database query function
        if (len(self.deaprtment) != 0  and len(self.program) !=0):
            data=getlistofcourses(self.deaprtment,self.program)
        #  if there is data rsult from the query, the data need to collect in a way that will show in next page
            if not data:
                print('no data found')
            else:
                #self.manager.get_screen('catalogpage').displaycatalog.add_widget(MDLabel(text='result'))
                
                for course in data:
                    insight=content2()
                    insight.coursedesc.text=f' Description:\n {course[2]}'
                    insight.courseunit.text= f'Unit: {course[3]}'
                    
                    self.manager.get_screen('catalogpage').displaycatalog.add_widget(
                                                            MDExpansionPanel(
                                                                icon=f"{'Images/'}folder.png",
                                                                content = insight,
                                                                panel_cls=MDExpansionPanelTwoLine(
                                                                                text=str(course[0]),
                                                                                secondary_text=str(course[1])
                                                                                )
                                                            )
                                                        ) 

    #GOing Back to selection page
    def Gobacktoselectionwork(self):
            self.manager.get_screen('catalogpage').displaycatalog.clear_widgets()
              
# ############################## SCREEN MANAGER ##########################
class PageManager(ScreenManager):
    pass


################# MAIN APP CLASS #################################
class TitanEnrolHelper(MDApp):
   
    def __init__(self,**kwargs):
        super(TitanEnrolHelper,self).__init__(**kwargs)
        self.root= Builder.load_file('pagescreen.kv')

    def logger(self):
        self.root.ids.CSU_Login.text = f'Hi {self.root.ids.user.text}!'

    def build(self):
        
        Window.size = (400,650)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette= "Blue"
        self.theme_cls.accent_palette= "Orange"
           
        return self.root
    

######################################################
#run the application
##using command line call
if __name__ == '__main__':
    TitanEnrolHelper().run()

#without command line in IDE
TitanEnrolHelper().run()
###################################################
