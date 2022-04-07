from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from App import screen_helper
import sqlite3
import random
import phonenumbers
import dropbox
from twilio.rest import Client
# Screne helper

acc_SID = 'ACf792d7660cfe1cbe6ce1f38d08b946e5'
auth_token  = '9c820e5dc8570dc528d1cadfa409748a'
global studentID
studentID = 20220000

client = Client(acc_SID,auth_token)


# Cloud storage upload class
class cloudStorage:
    def __init__(self, access_token):
        self.at = access_token

    def UploadFile(self, file_from, file_to):
        f = open(file_from, 'rb')
        f = f.read()
        dbx = dropbox.Dropbox(self.at)

        if file_from != '' and file_to != '':

            dbx.files_upload(f, file_to, mode=dropbox.files.WriteMode.overwrite)
            print("Your files are uploaded")
        else:
            print("Files are empty")

# define our different screens
class HomePage(Screen):
    pass

class OTPScreen(Screen):
    pass

class LoginPage(Screen):
    pass
class studentCredentials(Screen):
    pass
class showStudentCredentials(Screen):
    pass
class WindowManager(ScreenManager):
    pass

sn = ScreenManager()
sn.add_widget(LoginPage(name='login'))
sn.add_widget(HomePage(name='home'))
sn.add_widget(OTPScreen(name='otpscreen')) 
sn.add_widget(studentCredentials(name='stcredentials'))
sn.add_widget(showStudentCredentials(name='showCredentials'))

class StudentPortalApp(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = "DeepOrange"
        screen = Builder.load_string(screen_helper)
        # Create database or connect to one
        conn = sqlite3.connect('first-database.db')
        # create a cursor
        c = conn.cursor()
        # create a table 
        c.execute(""" CREATE TABLE if not exists students(
            studentID INTEGER PRIMARY KEY,
            name text,
            number text,
            hash_cypher text,
            id_hash text,
            encryption_key text)
        """)
        # commit our changes
        conn.commit()
        # close connection
        conn.close()

        return screen
    
    def logger(self):
        global otp
        otp = random.randint(1000,9999)

        try:
            x = int(self.root.get_screen('login').ids.phonenumber.text)

            my_number = phonenumbers.parse(self.root.get_screen('login').ids.phonenumber.text, "GB")
            if phonenumbers.is_valid_number(my_number):
                # msg = client.messages.create(
                # body = f"Your OTP is {otp}",
                # from_= "+17575305594",
                # to = f"+44{self.root.get_screen('login').ids.phonenumber.text}"
                # )
                self.root.current = 'otpscreen'
            else:
                os.system("""osascript -e 'Tell application "System Events" to display dialog "This is not a british phone number" with title "Hello Matey"'""")
        except ValueError:
            os.system("""osascript -e 'Tell application "System Events" to display dialog "Please Enter a Valid phone number" with title "Hello Matey"'""")


    def clear(self):
        # self.root.get_screen['login'].ids.Welcome_label.text = "Welcome"
        self.root.get_screen('login').ids.phonenumber.text = ""
        self.root.get_screen('login').ids.username.text = ""
    
    def verifyOtp(self):
        # if otp ==  int(self.root.get_screen('otpscreen').ids.otp_user.text):
            # Create database or connect to one
        conn = sqlite3.connect('first-database.db')
        # create a cursor
        c = conn.cursor()
        
        # create a table 
        # c.execute("SELECT number FROM students WHERE number = ?", (self.root.get_screen('login').ids.phonenumber.text,))
        # snum = c.fetchall()
        # if len(snum) == 0:

        data_person_name = [(self.root.get_screen('login').ids.username.text, self.root.get_screen('login').ids.phonenumber.text)]

        c.executemany('INSERT INTO students(name, number) VALUES (?,?)',  data_person_name)
        

        # Get the Name of the student from the form and get his id from the database
        namee = [(self.root.get_screen('login').ids.username.text)]
        c.execute("SELECT studentID from students WHERE name=?",namee,)
        id = c.fetchall()
        # get the ID and the name and write it into a text file (Cardentials)
        id_st = id [0]
        id_string = str(id_st[0])
        with open ('secret.txt', 'w') as e:
            e.write(f'{id_string}, {namee[0]}')
        # executing the AES file
        exec(open('AES.py').read())

        # coverting the cypher text and the id
        with open ('encrypted_secret.txt', 'rb') as r:
            cypher_text = r.read()

        cypher_text_hash = hash(cypher_text)
        student_id_hash = hash(id_st[0])
        print("Hashed Cardentials:",cypher_text_hash,student_id_hash)

        with open ('EncryptionKey.txt', 'rb') as r:
            encryptionK = r.read()
        #
        # encKeyStr = encryptionK.decode('utf-8')
        c.execute('''UPDATE students SET hash_cypher = ?, id_hash = ?, encryption_key = ? WHERE studentID = ? ''',(cypher_text_hash, student_id_hash, encryptionK,id_st[0])) 


        #  Uploading files to Dropbox
        token = 'sl.BFPlTZa4Ji1En4cmHQ7NS4Q1Je-5Ygq8svs0dBK0y8T1Ux53I2Wuj6lgDkyNgpLbiN3OYMrFKSEuP8bLV5SDTi2bZ4ftuaXbQMjy7b0DQQs8cAQKorNHTVZkLHGaEZorvki9ibSvDzwl'
    

        file_from = 'encrypted_secret.txt'
        file_to = '/LoginPortal/CypherTextStudentCredentials/StudentID_'+str(id_st[0])+'.txt'

        user = cloudStorage(token)
        user.UploadFile(file_from, file_to)
        # Update the welcome message
        self.root.get_screen('home').ids.homepage_label.text = "Welcome Student please note that your Student ID is: " + str(id_st[0])
        # else:
        #     print("Number exists")

        # commit our changes
        
        conn.commit()
        # close connection
        conn.close()
        self.root.current = 'home'
        # else:
        #     self.root.get_screen('otpscreen').ids.otp_label.text = "Inavlid OTP"
    def checkCredentials(self):

        self.root.current ='showCredentials'
        self.root.get_screen('showCredentials').ids.change.text = 'Hi {}'.format(str(self.root.get_screen('stcredentials').ids.id_entered.text))
        


# root.manager.current = 'home'
StudentPortalApp().run()






# def show_records(self):
    #     # Create database or connect to one
    #     conn = sqlite3.connect('first-database.db')
    #     # create a cursor
    #     c = conn.cursor()
    #     # create a table 
    #     c.execute("SELECT * FROM students")
    #     records = c.fetchall()

    #     word = ''

    #     for record in records:
    #         word = f'{word}\n{record}'
    #         self.root.get_screen('login').ids.Welcome_label.text = f'{word}'
    #     # commit our changes
    #     conn.commit()
    #     # close connection
    #     conn.close()


      # c.execute("INSERT INTO students VALUES(:name, :number)",{
        #     'name': self.root.get_screen('login').ids.username.text,
        #     'number':  self.root.get_screen('login').ids.phonenumber.text
            
        # })