from Browser_operator import Browser_operator
from Camera_Operator import Camera_operator
from Operation import *
import threading
import time


def main():
    camera_operator = Camera_operator()
    camera_operator_thread = threading.Thread( target = camera_operator.start , args = [] )
    camera_operator_thread.start()
    # camera_operator_thread = threading.Thread(target=camera_operator.multitasking_keyboard_input_testing, args=[])
    # camera_operator_thread.start()

    '''TODO względne sciezki!!!'''


    browser_operator = Browser_operator("/home/rafal/Dokumenty/chromedriver")
    while(True):
        if ( camera_operator.status != -1 ):

            if (camera_operator.status_move == 1):
                browser_operator.increase_volume()
            if (camera_operator.status_move == -1):
                browser_operator.decrease_volume()

            if ( camera_operator.status == ord('a') ):
                browser_operator.like()
            if (camera_operator.status == ord('s') ):
                browser_operator.not_like()
            if ( camera_operator.status == ord('f') ):
                browser_operator.increment_video_id_decision()
            if ( camera_operator.status == ord('d') ):
                browser_operator.decrement_video_id_decision()
            if ( camera_operator.status == ord('g')):
                browser_operator.change_video()
            if ( camera_operator.status == ord('z')):
                browser_operator.decrease_volume()
            if ( camera_operator.status == ord('x')):
                browser_operator.increase_volume()
            if ( camera_operator.status == ord('c')):
                browser_operator.skip_left()
            if ( camera_operator.status == ord('v')):
                browser_operator.skip_right()
            if ( camera_operator.status == ord('b')):
                browser_operator.change_screen_mode()
            if ( camera_operator.status == ord('n')):
                browser_operator.stop_or_continue()
            if ( camera_operator.status == ord('m')):
                browser_operator.scroll_down_by(-102)
            if ( camera_operator.status == ord('j')):
                browser_operator.scroll_down_by(102)
            if ( camera_operator.status == ord('k')):
                browser_operator.go_to_top_of_the_page()
            # print(camera_operator.status)



            '''KOMENTARZ DO USUNIĘCIA:
            Ten delay jest po to żeby nie zbierać kilka razy tego samego
            W sensie procesor przydziela czas głównemu wątkowi, a on odczytuje stan zmiennej kilka razy, do momentu
             przydzielenia czasu temu co obsługuje kamerę zmienna status jest niezmieniona, co jest nieprawidłowe bo ona
             się ma zmieniac od razu na -1 '''
            time.sleep(0.1)




main()
