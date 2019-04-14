from Operation import *
from copy import deepcopy
import cv2
import cv2 as cv
import numpy as np
import math

left_clicked = False
mouse_drawing_rect_coords = []


def handle_mouse_event(event, x, y, flags, param):
    global left_clicked
    global mouse_drawing_rect_coords

    if (left_clicked):
        '''User is drawing case, so new end is taken'''
        if (len(mouse_drawing_rect_coords) > 2):
            mouse_drawing_rect_coords = []
        if (len(mouse_drawing_rect_coords) > 1):
            del (mouse_drawing_rect_coords[-1])
        mouse_drawing_rect_coords.append((x, y))

    if (event == cv2.EVENT_LBUTTONDOWN and not left_clicked):
        '''User just clicked case - starting to draw'''
        mouse_drawing_rect_coords.append((x, y))
        left_clicked = True
    elif (event == cv2.EVENT_LBUTTONUP):
        '''User stopped drawing case, so area is left as it is'''
        if (len(mouse_drawing_rect_coords) == 2):
            del (mouse_drawing_rect_coords[-1])
        mouse_drawing_rect_coords.append((x, y))
        left_clicked = False


class Camera_operator:

    def __init__(self):
        '''Global variable, when leave is true, program ends'''
        self.leave = False

        '''This attribute stores current user decision'''
        self.status = None

        '''This attribute shows if observer took status'''
        self.status_delivered = True

    def get_status(self):
        '''Function used by observer to get current user decision'''
        self.status_delivered = True
        return self.status

    def get_cropped_image(self, image,fist):
        '''if the area in which hand recognition maus take place was specified, this function prints cropped image'''

        for (x, y, w, h) in fist:
            leftdown = x-w
            rightdown = x+2*w
            leftup = y-h
            rightup = y+2*h

            cropped_image = image[leftdown:rightdown, leftup:rightup]

        return cropped_image


    def operate_cropped_file(self, thresh,img):

        if (thresh is not None ):

            im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            cv.imshow("mask", thresh)

            contour = max(contours, key=lambda x: cv.contourArea(x))

            x, y, w, h = cv.boundingRect(contour)

            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 0)

            hull = cv.convexHull(contour)

            drawing = np.zeros(img.shape, np.uint8)
            cv.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
            cv.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

            hull = cv.convexHull(contour, returnPoints=False)
            defects = cv.convexityDefects(contour, hull)
            if(defects is not None):
                count_defects = 0

                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(contour[s][0])
                    end = tuple(contour[e][0])
                    far = tuple(contour[f][0])

                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

                    if angle <= 90:
                        count_defects += 1
                        cv.circle(img, far, 1, [0, 0, 255], -1)

                    cv.line(img, start, end, [0, 255, 0], 2)

                cv.putText(img, str(count_defects), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                cv.imshow("gest", img)
                all = np.hstack((drawing, img))
                cv.imshow("Contours", all)

    def start(self):
        global mouse_drawing_rect_coords
        global left_clicked

        capture = cv2.VideoCapture(0)

        key_pressed = 'q'

        base_thresh_val = 59
        base_gaussian_val = 5
        base_med_val = 11
        printing_label = True

        fist_cascade = cv2.CascadeClassifier("/home/rafal/PycharmProjects/Python2/fist_v3.xml")
        palm_cascade = cv2.CascadeClassifier("/home/rafal/PycharmProjects/Python2/palm.xml")

        thresh1 = None
        '''variable used to assign for variable prev_image'''

        fgbg = cv2.createBackgroundSubtractorMOG2()
        flag = 1
        lx=0
        ly=0
        lw=0
        lh =0
        while (capture.isOpened() and (not self.leave)):

            prev_image = deepcopy(thresh1)

            '''Reading image:'''
            ret, frame = capture.read()
            if (ret == False):
                print("Failed to catch")

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fist = fist_cascade.detectMultiScale(gray, 1.3, 5)

            palm = palm_cascade.detectMultiScale(gray, 1.3, 5)

            if flag == 1:
                cropped_image = None

            for (x, y, w, h) in fist:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if fist != ():
                    lx=x
                    ly =y
                    lw =w
                    lh =h

                    flag = 0

            if flag == 0:
                cropped_image = thresh1[lx-lw:lx+2*lw,ly-lh:ly+2*lh]

            for (x, y, w, h) in palm:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)




            self.operate_cropped_file(thresh1,frame)


            fgmask = fgbg.apply(frame)

            cv2.imshow('fg', frame)


            blur = cv2.GaussianBlur(gray, (base_gaussian_val, base_gaussian_val), 0)

            med = cv2.medianBlur(blur, base_med_val)

            ret, thresh1 = cv2.threshold(med, base_thresh_val, 255, cv2.THRESH_BINARY_INV)





            difference = None
            if (prev_image is not None):
                difference = cv2.absdiff(prev_image, thresh1)

            # '''Label printing:'''
            # if printing_label:
            #     cv2.rectangle(thresh1, (0, 0), (700, 100), (255, 255, 0), cv2.FILLED)
            #     cv2.putText(thresh1,
            #                 "Callibrate threshold using W and S key untill your hand will have good contrast with background.",
            #                 (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(thresh1,
            #                 "Callibrate gausianBlur using E and D key untill your hand will have good contrast with background.",
            #                 (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(thresh1,
            #                 "Callibrate medianBlur using R and F key untill your hand will have good contrast with background.",
            #                 (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(thresh1,
            #                 "Use your mouse to specify hand gesture catching region",
            #                 (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(thresh1,
            #                 "WARNING: Select area with the greatest contrast beetween background and your hand",
            #                 (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(thresh1,
            #                 "When finished - press ENTER",
            #                 (15, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(thresh1,
            #                 "C - toggle label visibility",
            #                 (15, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(thresh1,
            #                 "Q - finish",
            #                 (15, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #
            # if (len(mouse_drawing_rect_coords) == 2):
            #     cv2.rectangle(thresh1, mouse_drawing_rect_coords[0], mouse_drawing_rect_coords[1], (130, 255, 200), 2)

            cv2.imshow('Current frame', thresh1)
            cv2.setMouseCallback('Current frame', handle_mouse_event)
            '''if ( prev_image is not None ):
                cv2.imshow('Prevoius frame', prev_image)'''
            '''if ( difference is not None):
                cv2.imshow('Pixel Differences', difference)'''
            key_pressed = cv2.waitKey(10)

            if (key_pressed == ord('w')):
                base_thresh_val += 1
            if (key_pressed == ord('s')):
                base_thresh_val -= 1
            if (key_pressed == ord('e')):
                base_gaussian_val += 2
            if (key_pressed == ord('d')):
                if (base_gaussian_val > 1):
                    base_gaussian_val -= 2
            if (key_pressed == ord('r')):
                base_med_val += 2
            if (key_pressed == ord('f')):
                if (base_med_val > 1):
                    base_med_val -= 2
            if (key_pressed == ord('c')):
                printing_label = not printing_label
            if (key_pressed == ord('q')):
                self.leave = True
            if (key_pressed != -1):
                print(base_thresh_val)
                print(base_gaussian_val)
                print(base_med_val)
                print()

        '''Cleaning:'''
        cv2.destroyAllWindows()
        capture.release()
