import time
from pynput.keyboard import Key, Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys


class Browser_operator:

    def highlight_browser_element(self, element):
        self.driver.execute_script("arguments[0].setAttribute('style', 'background: blue; border: 2px solid red;');",
                                   element)

    def unhighlight_browser_element(self, element):
        self.driver.execute_script("arguments[0].style.border='0px'", element)
        self.driver.execute_script("arguments[0].style.background='white'", element)

    def scroll_down_by(self, value):
        self.driver.execute_script("window.scrollBy(0," + str(value) + ")")

    def scroll_up_by(self, value):
        self.driver.execute_script("window.scrollBy(0," + str(value) + ")")

    def __init__(self, path):

        self.driver = webdriver.Chrome(path)
        self.driver.set_page_load_timeout(10)

        self.driver.get("https://www.youtube.com/watch?v=8kVI621fZug")

        self.keyboard = Controller()

        self.url = self.driver.current_url

        '''Variable shows whenever system can work (When video is watched)'''
        self.status = False

        '''Next video decision:'''
        self.next_video_decision = 0

        self.full_screen = False
        
        self.radio_mode = False
        self.last_radio_station = 0
        self.radio_stations =[
                               "https://www.youtube.com/watch?v=taD9hqwCb1o",
                               "https://www.youtube.com/watch?v=6dHrafwh974",
                               "https://www.youtube.com/watch?v=6dHrafwh974"
                             ]

        '''Following variable shows how many times screen has been scrolled
        screen is scrolled every time, user wants to change next video decision
        So when user choses video 4, screen is scrolled
        Then to watch, back to top
        If user wants to change to video 5, screen is scrolled by 2 times ( n-3 to make chosen video at center)'''
        self.current_shifts = 0

        self.identifier = None
        self.password = None

    def __del__(self):

        self.driver.close()

    def synch(self):
        '''SYNCHronize'''
        '''Method must be called before every operation to check if system can work'''
        print(self.url)
        self.url = self.driver.current_url

        self.status = ("/watch?" in self.url)

    def press_f_key(self):
        '''UNUSED'''
        self.synch()

        '''Switching between modes'''
        if (not self.status):
            '''User is not in video section'''
            return

        self.keyboard.press('f')
        self.keyboard.release('f')
        self.full_screen = True

    def press_space(self):
        '''UNUSED'''
        self.synch()
        '''Pause/Go'''
        if (not self.status):
            '''User is not in video section'''
            return

        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)

    def press_upper_key(self):
        '''UNUSED'''
        self.synch()
        if not self.status:
            '''User is not in video section'''
            return

        self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)

    def press_right_key(self):
        '''UNUSED'''
        self.synch()
        if not self.status:
            '''User is not in video section'''
            return

        self.keyboard.press(Key.right)
        self.keyboard.release(Key.right)

    def press_down_key(self):
        '''UNUSED'''
        self.synch()
        if not self.status:
            '''User is not in video section'''
            return

        self.keyboard.press(Key.down)
        self.keyboard.release(Key.down)

    def press_left_key(self):
        '''UNUSED'''
        self.synch()
        if not self.status:
            '''User is not in video section'''
            return

        self.keyboard.press(Key.left)
        self.keyboard.release(Key.left)

    def shift_down(self):

        if self.next_video_decision > 1 and self.next_video_decision < 39:
            print("OK")
            print(self.next_video_decision - 1 - self.current_shifts)
            self.scroll_down_by((self.next_video_decision - 1 - self.current_shifts) * 102)
            self.current_shifts = (self.next_video_decision - 1)

    def shift_up(self):
        if self.next_video_decision > 0 and self.next_video_decision < 38:
            self.scroll_up_by((self.next_video_decision - 1 - self.current_shifts) * 102)
            self.current_shifts = self.next_video_decision - 1

    def go_to_top_of_the_page(self):
        self.scroll_up_by(((-1) * self.current_shifts) * 102)
        self.current_shifts = 0

    def decrement_video_id_decision(self):
        self.synch()
        if not self.status:
            '''User is not in video section'''
            return

        self.unhighlight_browser_element(self.driver.find_elements_by_id("video-title")[self.next_video_decision])

        self.next_video_decision -= 1
        if self.next_video_decision < 0:
            self.next_video_decision = 0

        self.highlight_browser_element(self.driver.find_elements_by_id("video-title")[self.next_video_decision])

        self.shift_up()

    def increment_video_id_decision(self):
        self.synch()
        if not self.status:
            '''User is not in video section'''
            return

        self.unhighlight_browser_element(self.driver.find_elements_by_id("video-title")[self.next_video_decision])

        self.next_video_decision = (self.next_video_decision + 1)
        if self.next_video_decision > 39:
            self.next_video_decision = 39

        self.highlight_browser_element(self.driver.find_elements_by_id("video-title")[self.next_video_decision])

        '''measuring how many shifts has to be done'''
        if self.current_shifts > (40 - 3):
            self.currrent_shifts = (40 - 3)

        self.shift_down()

    def decrease_volume(self):
        self.synch()
        self.go_to_top_of_the_page()
        if not self.status:
            '''User is not in video section'''
            return

        movie_screen = self.driver.find_element_by_id("movie_player")
        movie_screen.send_keys(Keys.DOWN)

    def increase_volume(self):
        self.synch()
        self.go_to_top_of_the_page()
        if not self.status:
            '''User is not in video section'''
            return

        movie_screen = self.driver.find_element_by_id("movie_player")
        movie_screen.send_keys(Keys.UP)

    def skip_right(self):
        self.synch()
        self.go_to_top_of_the_page()
        if not self.status:
            '''User is not in video section'''
            return

        movie_screen = self.driver.find_element_by_id("movie_player")
        movie_screen.send_keys(Keys.RIGHT)

    def skip_left(self):
        self.synch()
        self.go_to_top_of_the_page()
        if not self.status:
            '''User is not in video section'''
            return

        movie_screen = self.driver.find_element_by_id("movie_player")
        movie_screen.send_keys(Keys.LEFT)

    def stop_or_continue(self):
        self.synch()
        self.go_to_top_of_the_page()
        if not self.status:
            '''User is not in video section'''
            return

        movie_screen = self.driver.find_element_by_id("movie_player")
        movie_screen.click()

    def like(self):
        self.synch()
        self.go_to_top_of_the_page()
        if (not self.status) and (not self.full_screen):
            '''User is not in video section'''
            return
        '''19 is index of like button'''
        self.driver.find_elements_by_id("button")[19].click()

    def not_like(self):
        self.synch()
        self.go_to_top_of_the_page()
        if (not self.status) and (not self.full_screen):
            '''User is not in video section'''
            return
        '''20 is index of like button'''
        self.driver.find_elements_by_id("button")[20].click()

    def change_video(self):
        self.synch()
        self.go_to_top_of_the_page()
        if (not self.status) and (not self.full_screen):
            '''User is not in video section'''
            return

        self.shift_up()

        self.unhighlight_browser_element(self.driver.find_elements_by_id("video-title")[self.next_video_decision])
        self.driver.find_elements_by_id("video-title")[self.next_video_decision].click()
        self.next_video_decision = 0

    def change_screen_mode(self):
        self.synch()
        self.go_to_top_of_the_page()
        if (not self.status):
            '''User is not in video section'''
            return

        whole_page = self.driver.find_element_by_xpath("/html")
        whole_page.send_keys("f")

    def __radio(self):
        """UNUSED"""
        self.synch()
        self.go_to_top_of_the_page()

        self.driver.find_elements_by_id("button")[8].click()
        self.driver.find_elements_by_id("label")[2].click()

    def take_identifier_and_password(self):
        '''Temporary method'''
        self.identifier = input()
        print(self.identifier)
        self.password = input()
        print(self.password)

    def login(self):

        if (self.identifier is None or self.password is None):
            return

        self.synch()
        self.go_to_top_of_the_page()

        self.driver.find_elements_by_id("button")[17].click()

        self.driver.find_element_by_id("identifierId").send_keys(self.identifier)
        self.driver.find_element_by_id("identifierNext").click()

        time.sleep(1)

        'if login passes then it goes for password, else it falls back'
        try:
            self.driver.find_element_by_name("password").send_keys(self.password)
            self.driver.find_element_by_id("passwordNext").click()
        except:
            self.driver.back()

        'if password does not pass, fall back twice'
        'There is no element such as passwordNext if user has logged in succesfuly'
        if (len(self.driver.find_elements_by_id("passwordNext")) != 0):
            self.driver.back()
            time.sleep(0.5)
            self.driver.back()
    
    def radio(self):
        if not self.radio_mode :
            self.driver.get( self.radio_stations [ self.last_radio_station ] )
        else:
            self.driver.back()
            self.last_radio_station = ( self.last_radio_station + 1 ) % 3



        self.radio_mode = not self.radio_mode
        
        
    def __str__(self):
        out = "Driver:"
        out += str(self.driver)
        out += "\nURL:"
        out += str(self.url)
        out += "\nStatus:"
        out += str(self.status)
        out += "\nNext_video_decision:"
        out += str(self.next_video_decision)
        out += "\nFull_screen:"
        out += str(self.full_screen)
        return out


'''W istalacji będzie musiało być pobranie chromedriver'a do konkretnej, względnej ścieżki'''
