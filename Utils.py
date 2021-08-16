from time import sleep, strftime
from os.path import isfile, isdir
from os import mkdir
from re import sub
import numpy as np
import pyautogui as pg
import requests
import datetime
import cv2

def GetTimestamp(format: str = '%Y-%m-%d_%H-%M-%S', date = None) -> str:
    if date is None:
        return strftime(format)
    else:
        return datetime.datetime.strptime(date, format)

def CalculateSleepTime(date : str) -> int:

    if date == "now":
        return 0

    try:
        dateobject = GetTimestamp('%Y-%m-%d_%H-%M', date)
    except ValueError:
        try:
            dateobject = GetTimestamp('%H-%M', date)
        except ValueError: 
            raise ValueError("The date is incorrectly formated")

    datediff = dateobject - datetime.datetime.today()
    return datediff.total_seconds()
    
def ReadFullFile(file_path : str) -> str:

    if not isfile(file_path):
        raise AttributeError("File path is invalid, either because a file is not there o it is unreadable.")

    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        raise e

def MakeStringParsable(string : str) -> str:
    return sub("[^0-9]", "", string)

def CheckInternetConnection() -> bool:
    url = "https://www.google.com"
    timeout = 5
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def WaitForInternetConnection(time_to_sleep : int = 20) -> None:
    while(True):
        if not CheckInternetConnection():
            sleep(time_to_sleep)
        else:
            break

def EnsurePathExists(path: str) -> None:
    if not isdir(path) and path == "Images":
        mkdir(path)

def TakeSnap(path: str) -> str:
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()
    timestr = GetTimestamp()
    filename='{}\\Capture-{}.jpg'.format(path,timestr)
    EnsurePathExists(path)
    cv2.imwrite(filename=filename, img=frame)
    webcam.release()
    return filename

def TakeScreenshot(path: str) -> str:
    image = pg.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    timestr = GetTimestamp()
    filename='{}\\Screenshot-{}.jpg'.format(path,timestr)
    cv2.imwrite(filename, image)
    return filename