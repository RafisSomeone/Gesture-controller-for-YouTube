import cv2
from PyQt5.QtWidgets import *
import os
from Browser_operator import Browser_operator



'''Solving problem with non compatible environment variables
QApplication looks for environment variable QT_STYLE_OVERRIDE which must be Fusion or Windows
'''
os.environ["QT_STYLE_OVERRIDE"] = "Fusion"

login_and_password_file_path = "Data"

class File_reader:

    def isValid(self):

        i = 0

        '''File must contain only one newLine character, because first line is login and second line is password'''
        newline_char_counter = 0

        while( i < len(self.file_content) ):

            if ( self.file_content[i] == '\n' ):
                newline_char_counter += 1


            i += 1

        if (newline_char_counter != 1):
            return False

        return True

    def getLogin(self):
        if(not self.operation_result ):
            return ""
        separatedID = self.file_content.index("\n")
        return self.file_content[0:separatedID]
    def getPassword(self):
        if (not self.operation_result):
            return ""
        separatedID = self.file_content.index("\n")
        return self.file_content[ 1 + separatedID : len(self.file_content)]



    def __init__(self):
        self.file_content = ""
        self.operation_result = True


        '''If file does not exist - cannot read email and password'''
        try:
            self.file = open(login_and_password_file_path, "r")
        except (FileNotFoundError):
            self.operation_result = False



        if ( self.operation_result):
            self.file_content = self.file.read()
            self.operation_result = self.isValid()


class File_writer:
    def __init__(self, login, password):
        if ( type(login) != str):
            raise(Exception("Login is not string!"))
        if ( type(password) != str):
            raise(Exception("Password is not string"))

        file = open(login_and_password_file_path, "w")
        file.write(login)
        file.write("\n")
        file.write(password)
        file.close()

class Login:


    def finish_logging(self):
        self.waiting_for_logging_in = False
    def end_login_process(self):
        self.finish = True
    def get_login(self):
        return self.login_string
    def get_password(self):
        return self.password_string
    def get_login_and_password_from_file(self):

        file_parser = File_reader()
        self.data_file_is_valid = file_parser.isValid()
        self.autologin_string = ""
        self.autopassword_string = ""
        if ( self.data_file_is_valid ):

            self.autologin_string = file_parser.getLogin()
            self.autopassword_string = file_parser.getPassword()



    def login_clicked(self):
        self.login_string = self.login_input.text()
        #self.password_string = self.password_input.text() //if password is hidden, this should not be executed
        print(self.password_string)
        self.browser.set_identifier_and_password(self.login_string, self.password_string)
        result = self.browser.login()
        if ( result and self.remember_me_button.isChecked() ):
            File_writer(self.login_string, self.password_string)
        elif ( not result ):
            self.autologin_impossible_label.setVisible(False)
            self.login_impossible_label.setVisible(True)
        '''Observer calls Browser operator to check if login is valid and changes this attribute value'''
        '''If login is succesful, system goes on'''

        if ( result ):
            self.browser.set_logged_in(True)
            self.browser.set_logging_in_state(False)
            self.exit()

    def autologin(self):
        if ( not self.data_file_is_valid ):
            self.login_impossible_label.setVisible(False)
            self.autologin_impossible_label.setVisible(True)
            return
        self.browser.set_identifier_and_password(self.autologin_string, self.autopassword_string)
        result = self.browser.login()
        if (not result):
            self.login_impossible_label.setVisible(False)
            self.autologin_impossible_label.setVisible(True)
        else:
            self.browser.set_logged_in(True)
            self.browser.set_logging_in_state(False)
            self.exit()

    def dont_login(self):
        self.browser.set_logged_in(False)
        self.browser.set_logging_in_state(False)
        self.exit()

    def exit(self):
        self.app.exit()

    def hide_password(self):
        if ( self.after_change ):
            self.after_change = not self.after_change
            return

        hidden_password_wtih_added_char = self.password_input.text()
        #print(self.password_string)
        #print(hidden_password_wtih_added_char)
        if ( len(hidden_password_wtih_added_char) > len(self.password_string) ):
            self.password_string += str(hidden_password_wtih_added_char[len(hidden_password_wtih_added_char) - 1])
            self.after_change = not self.after_change
        else:
            self.password_string = self.password_string[0:len(self.password_string)-1]
        #print(self.password_string)

        hidden_password_with_added_char = ""
        for i in range(0,len(self.password_string) ):
            hidden_password_with_added_char = hidden_password_with_added_char + "*"
        #print("A")
        #print(hidden_password_wtih_added_char)
        self.password_input.setText(hidden_password_with_added_char)

    def __init__(self, browser_operator):
        if ( type(browser_operator) != Browser_operator):
            raise(Exception("Expected browser operator in Login initializer"))


        self.app = QApplication([])


        '''Variables used for measuring where to put elements'''
        self.screen_width = self.app.desktop().screenGeometry().width()
        self.screen_height = self.app.desktop().screenGeometry().height()
        width_middle = self.screen_width / 2
        height_middle = self.screen_height / 2


        #tlo = cv2.imread("tlo.jpg", 1)
        #cv2.imshow("display", tlo)

        self.browser = browser_operator
        self.browser.set_logged_in(False)
        self.browser.set_logging_in_state(True)
        '''Interface:'''
        self.window = QWidget()

        self.autologin_impossible_label = QLabel("Autologin is impossible", self.window)
        self.autologin_impossible_label.move(width_middle + 30, height_middle + 45 )
        self.autologin_impossible_label.setStyleSheet("QLabel { color : red; }")
        self.autologin_impossible_label.setVisible(False)

        self.login_impossible_label = QLabel("Invalid Login or Password", self.window)
        self.login_impossible_label.move(width_middle + 30, height_middle + 45 )
        self.login_impossible_label.setStyleSheet("QLabel { color : red; }")
        self.login_impossible_label.setVisible(False)


        self.get_login_and_password_from_file()
        self.password_string = ""
        self.login_string = ""

        QLabel("Insert your YouTube account login and password \nto make all functions avalible:",self.window).\
            move(width_middle - 150, height_middle - 80)

        caution_label = QLabel("Caution: Login and Autologin operations may take a few seconds",
                               self.window)
        caution_label.setStyleSheet("QLabel { color : red; }")
        caution_label.move(width_middle - 150, height_middle + 120)

        self.login_label = QLabel("Login:", self.window)
        self.login_label.move(width_middle - 150, height_middle - 20)

        self.password_label = QLabel("Password:", self.window)
        self.password_label.move(width_middle - 150, height_middle + 10)

        self.login_input = QLineEdit(self.window)
        self.login_input.move(width_middle - 80, height_middle - 25 )

        self.password_input = QLineEdit(self.window)
        self.password_input.move(width_middle - 80, height_middle + 5 )

        self.remember_me_button = QCheckBox("Remember me",self.window)
        self.remember_me_button.move(width_middle - 140, height_middle + 45)

        self.login_button = QPushButton("Login", self.window)
        self.login_button.move(width_middle - 110, height_middle + 85)
        self.login_button.clicked.connect(self.login_clicked)

        self.autologin_button = QPushButton("Autologin",self.window)
        self.autologin_button.move(width_middle + 50, height_middle - 25)
        self.autologin_button.clicked.connect(self.autologin)

        self.do_not_login_button = QPushButton("Don't Login", self.window)
        self.do_not_login_button.move(width_middle + 50, height_middle + 5)
        self.do_not_login_button.clicked.connect(self.dont_login)

        self.exit_button = QPushButton("Exit", self.window)
        self.exit_button.move(self.screen_width - 80,0)
        self.exit_button.clicked.connect(self.exit)
        self.window.showFullScreen()



        '''Logic:'''
        self.shut_down = False
        self.inserted_login = ""
        self.inserted_password = ""

        self.after_change = False
        self.password_input.textChanged.connect(self.hide_password)

        #self.get_login_and_password_from_file()
        self.app.exec_()
