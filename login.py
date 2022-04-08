from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from App import screen_helper
import sqlite3
import random
import phonenumbers
import dropbox
import hashlib
import string
from twilio.rest import Client
# Screne helper

acc_SID = 'ACf792d7660cfe1cbe6ce1f38d08b946e5'
auth_token  = '4f8562d63926e05652855bf717c28884'
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
        if self.root.get_screen('login').ids.username.text != "":
            try:
                x = int(self.root.get_screen('login').ids.phonenumber.text)

                my_number = phonenumbers.parse(self.root.get_screen('login').ids.phonenumber.text, "GB")
                if phonenumbers.is_valid_number(my_number):
                    msg = client.messages.create(
                    body = f"Your OTP is {otp}",
                    from_= "+17575305594",
                    to = f"+44{self.root.get_screen('login').ids.phonenumber.text}"
                    )
                    self.root.current = 'otpscreen'
                else:
                    os.system("""osascript -e 'Tell application "System Events" to display dialog "This is not a british phone number" with title "Action Needed"'""")
            except ValueError:
                os.system("""osascript -e 'Tell application "System Events" to display dialog "Please Enter a Valid phone number" with title "Action Needed"'""")
        else:
            os.system("""osascript -e 'Tell application "System Events" to display dialog "Please Enter a User name" with title "Action Needed"'""")


    def clear(self):
        # self.root.get_screen['login'].ids.Welcome_label.text = "Welcome"
        self.root.get_screen('login').ids.phonenumber.text = ""
        self.root.get_screen('login').ids.username.text = ""
    
    def verifyOtp(self):
        if otp ==  int(self.root.get_screen('otpscreen').ids.otp_user.text):
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
            token = 'sl.BFQZD0KyARKulR3VGT_GNw5ADpmCqeXu7LSWQKuaENqEAlQEuoiHQtv35-LPlpzMtFot_04fddo-c3_fVK0pJ50WzkfbnfC6Vkx-2-T4U6gE2_9W95sYwbSl5gWFQRplCnmqNR3Z5X9P'
        

            file_from = 'encrypted_secret.txt'
            file_to = '/LoginPortal/CypherTextStudentCredentials/StudentID_'+str(id_st[0])+'.txt'

            user = cloudStorage(token)
            user.UploadFile(file_from, file_to)
            # Update the welcome message
            self.root.get_screen('home').ids.homepage_label.text = "Welcome Student please note that your Student ID is: " + str(id_st[0])
        else:
            os.system("""osascript -e 'Tell application "System Events" to display dialog "Invalid OTP" with title "Action Needed"'""")
            self.root.current = 'otpscreen'

        # commit our changes
        
        conn.commit()
        # close connection
        conn.close()
        self.root.current = 'home'
        # else:
        #     self.root.get_screen('otpscreen').ids.otp_label.text = "Inavlid OTP"

    def checkCredentials(self):

        self.root.current ='showCredentials'
        # Create database or connect to one
        conn = sqlite3.connect('first-database.db')
        # create a cursor
        c = conn.cursor()
        # Selecting values from database 
        entered_SID = [(self.root.get_screen('stcredentials').ids.id_entered.text)]
        c.execute("SELECT * from students WHERE studentID=?",entered_SID)
        IDname = c.fetchall()
        hashCipher = IDname[0][3]
        encKey = IDname[0][5]
        hashId = IDname[0][4]
        # Checking if the hash values match
        with open('EncryptionKey.txt','wb') as k:
            k.write(encKey)

        namee = [(self.root.get_screen('login').ids.username.text)]
        c.execute("SELECT studentID from students WHERE name=?",namee,)
        id = c.fetchall()
        # Check sum function
        def file_has_checksum(file_path):
      
            check_path = file_path 
            if os.path.isfile(file_path) and os.path.isfile(check_path):
                with open(check_path, 'r') as check_f:
                    return True
            return False
        # get the ID and the name and write it into a text file (Cardentials)
        if IDname[0][0] == id[0][0]:
            
            # Retriving from the cloud
            token = 'sl.BFQZD0KyARKulR3VGT_GNw5ADpmCqeXu7LSWQKuaENqEAlQEuoiHQtv35-LPlpzMtFot_04fddo-c3_fVK0pJ50WzkfbnfC6Vkx-2-T4U6gE2_9W95sYwbSl5gWFQRplCnmqNR3Z5X9P'
            DBX = dropbox.Dropbox(token)
            res, rawData = DBX.files_download('/LoginPortal/CypherTextStudentCredentials/StudentID_'+str(IDname[0][0])+'.txt')
            s = ''
            for x in rawData.iter_lines():
                s += str(x.strip())
            b = s.encode('utf-8')
            with open('encryptetCloud.txt', 'wb') as df:
                df.write(b)

            with open('decrypted_secret.txt', 'rb') as df:
                checked_file = df.read()

            if file_has_checksum('decrypted_secret.txt'):
                self.root.get_screen('showCredentials').ids.change.text = f'This is your student credentials please keep it secure.\n\nStudent name: {IDname[0][1]}\nStudent Phone: {IDname[0][2]}'
            else:
                os.system("""osascript -e 'Tell application "System Events" to display dialog "File is corrupted." with title "Action Needed"'""")

        else:
            os.system("""osascript -e 'Tell application "System Events" to display dialog "Please Check your ID again" with title "Action Needed"'""")
            self.root.current = 'stcredentials'

        exec(open('AESD.py').read())
        # commit our changes
        conn.commit()
        # close connection
        conn.close()


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