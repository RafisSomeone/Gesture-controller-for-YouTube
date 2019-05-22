from Browser_operator import Browser_operator
from Camera_Operator import CameraOperator
from Operation import *
import threading
import time
import sys


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
    camera_operator = CameraOperator()
    camera_operator_thread = threading.Thread(target=camera_operator.start, args=[])
    camera_operator_thread.start()
    # camera_operator_thread = threading.Thread(target=camera_operator.multitasking_keyboard_input_testing, args=[])
    # camera_operator_thread.start()

    browser_operator = Browser_operator("/home/rafal/Dokumenty/chromedriver/chromedriver")
    while True:

        # print(camera_operator.status_move, camera_operator.status,camera_operator.block)

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


main()
