from Browser_Operator import Browser_operator
from Camera_Operator import CameraOperator
from Operation import *
from Login import *
import threading
import time
import sys

'''Change to use keyboard'''
debug = False

def mode_one(camera_operator, browser_operator):
    if camera_operator.status_move == 1:
        browser_operator.radio_next_station()

    if camera_operator.status_move == -1:
        browser_operator.radio_previous_station()

    if camera_operator.status_move == 2:
        browser_operator.radio()

    time.sleep(1)


def mode_two(camera_operator, browser_operator):
    if camera_operator.status_move == -1:
        browser_operator.decrease_volume()
    if camera_operator.status_move == 1:
        browser_operator.increase_volume()
    if camera_operator.status_move == 3:
        browser_operator.like()
        time.sleep(1)
    if camera_operator.status_move == 4:
        browser_operator.not_like()
        time.sleep(1)


def mode_three(camera_operator, browser_operator):
    print(camera_operator.status_move)
    if camera_operator.status_move == -1:
        browser_operator.decrement_video_id_decision()
    if camera_operator.status_move == 1:
        browser_operator.increment_video_id_decision()
    if camera_operator.status_move == 2:
        browser_operator.change_video()
        time.sleep(1)


def mode_four(camera_operator, browser_operator):
    if camera_operator.status_move == -1:
        browser_operator.skip_left()
    if camera_operator.status_move == 1:
        browser_operator.skip_right()
    if camera_operator.status_move == 2:
        browser_operator.stop_or_continue()
        time.sleep(1)
    if camera_operator.status_move == 3:
        browser_operator.change_screen_mode()
        time.sleep(1)


def main():
    browser_operator = Browser_operator("/home/michal/chromedriver", "https://www.youtube.com/watch?v=cGNUpEerm9E")

    '''Logging in'''
    Login(browser_operator)


    if ( browser_operator.logging_in_state ):
        return




    camera_operator = CameraOperator()
    if ( not debug ):
        camera_operator_thread = threading.Thread(target=camera_operator.start, args=[])
        camera_operator_thread.start()
    else:
        camera_operator_thread = threading.Thread(target=camera_operator.multitasking_keyboard_input_testing, args=[])
        camera_operator_thread.start()

    while not debug:

        print(camera_operator.status_move, camera_operator.status,camera_operator.block)

        if camera_operator.status != -1:
            if camera_operator.status == 1:
                mode_one(camera_operator, browser_operator)

            if camera_operator.status == 2:
                mode_two(camera_operator, browser_operator)

            if camera_operator.status == 3:
                mode_three(camera_operator, browser_operator)

            if camera_operator.status == 4:
                mode_four(camera_operator, browser_operator)

            '''KOMENTARZ DO USUNIĘCIA:
            Ten delay jest po to żeby nie zbierać kilka razy tego samego
            W sensie procesor przydziela czas głównemu wątkowi, a on odczytuje stan zmiennej kilka razy, do momentu
             przydzielenia czasu temu co obsługuje kamerę zmienna status jest niezmieniona, co jest nieprawidłowe bo ona
             się ma zmieniac od razu na -1 '''
            time.sleep(0.1)
    while debug:
        if (camera_operator.status != -1):

            if (camera_operator.status == ord('a')):
                browser_operator.like()
            if (camera_operator.status == ord('s')):
                browser_operator.not_like()
            if (camera_operator.status == ord('f')):
                browser_operator.increment_video_id_decision()
            if (camera_operator.status == ord('d')):
                browser_operator.decrement_video_id_decision()
            if (camera_operator.status == ord('g')):
                browser_operator.change_video()
            if (camera_operator.status == ord('z')):
                browser_operator.decrease_volume()
            if (camera_operator.status == ord('x')):
                browser_operator.increase_volume()
            if (camera_operator.status == ord('c')):
                browser_operator.skip_left()
            if (camera_operator.status == ord('v')):
                browser_operator.skip_right()
            if (camera_operator.status == ord('b')):
                browser_operator.change_screen_mode()
            if (camera_operator.status == ord('n')):
                browser_operator.stop_or_continue()
            if (camera_operator.status == ord('m')):
                browser_operator.scroll_down_by(-100)
            if (camera_operator.status == ord('j')):
                browser_operator.scroll_down_by(100)
            print(camera_operator.status)

main()
