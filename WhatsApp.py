from urllib.parse import quote
from platform import system
import webbrowser as web
import pyautogui as pg
from io import BytesIO
from PIL import Image
import win32clipboard
import Utils
import pathlib
import time
import os

def SendWhatsAppToNumber(phone_number: str, message: str, wait_time: int = 20, tab_close: bool = False, close_time: int = 3) -> None:

    if "+" not in phone_number:
        raise ValueError("Prefix missing from phone_number")

    parsed_message = quote(message)
    web.open('https://web.whatsapp.com/send?phone=' +
             phone_number + '&text=' + parsed_message)
    
    time.sleep(2)
    width, height = pg.size()
    pg.click(width / 2, height / 2)
    time.sleep(wait_time - 2)
    pg.press('enter')
    if tab_close:
        CloseTab(close_time)

def SendWhatsAppToGroup(group_id: str, message: str, wait_time: int = 20, tab_close: bool = False, close_time: int = 3) -> None:

    web.open('https://web.whatsapp.com/accept?code=' + group_id)
    time.sleep(2)
    width, height = pg.size()
    time.sleep(wait_time - 2)
    pg.click(width / 2, height - height / 10)
    pg.typewrite(message + "\n")
    if tab_close:
        CloseTab(wait_time=close_time)

def SendWhatsAppImageToPhone(phone_number: str, img_path: str, caption: str = "", wait_time: int = 15, tab_close: bool = True, close_time: int = 3) -> None:

    if "+" not in phone_number:
        raise ValueError("Prefix missing from phone_number")

    web.open('https://web.whatsapp.com/send?phone=' +
             phone_number + '&text=' + caption)
    time.sleep(5)
    ImageToClipboard(img_path, wait_time)
    if tab_close:
        CloseTab(wait_time=close_time)

def SendWhatsAppImageToGroup(group_id: str, img_path: str, caption: str = "", wait_time: int = 15, tab_close: bool = False, close_time: int = 3) -> None:
    
    web.open('https://web.whatsapp.com/accept?code=' + group_id)
    time.sleep(2)
    width, height = pg.size()
    time.sleep(wait_time - 2)
    pg.click(width / 2, height - height / 10)
    pg.typewrite(caption + "\n")
    ImageToClipboard(img_path, wait_time)
    if tab_close:
        CloseTab(wait_time=close_time)

def ImageToClipboard(img_path: str, wait_time: int) -> None:
    if system().lower() == "linux":
        if pathlib.Path(img_path).suffix in (".PNG", ".png"):
            os.system(
                f"xclip -selection clipboard -target image/png -i {img_path}")
        elif pathlib.Path(img_path).suffix in (".jpg", ".JPG", ".jpeg", ".JPEG"):
            os.system(
                f"xclip -selection clipboard -target image/jpg -i {img_path}")
        else:
            print(f"The file format {pathlib.Path(img_path).suffix} is not supported!")
            return
        time.sleep(2)
        pg.hotkey("ctrl", "v")
    elif system().lower() == "windows":
        image = Image.open(img_path)
        output = BytesIO()
        image.convert('RGB').save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        time.sleep(2)
        pg.hotkey("ctrl", "v")
    elif system().lower() == "darwin":
        if pathlib.Path(img_path).suffix in (".jpg", ".jpeg", ".JPG", ".JPEG"):
            width, height = pg.size()
            pg.click(width / 2, height / 2)
            os.system(f"osascript -e 'set the clipboard to (read (POSIX file \"{img_path}\") as JPEG picture)'")
        else:
            print(f"The file format {pathlib.Path(img_path).suffix} is not supported!")
            return
        time.sleep(2)
        pg.hotkey("command", "v")
    else:
        print(f"{system().lower()} not supported!")
        return
    time.sleep(wait_time)
    pg.press('enter')

def CloseTab(wait_time: int = 2) -> None:

    time.sleep(wait_time)
    if system().lower() in ("windows", "linux"):
        pg.hotkey("ctrl", "w")
    elif system().lower() in "darwin":
        pg.hotkey("command", "w")
    else:
        raise Warning(f"{system().lower()} not supported!")
    pg.press("enter")

def SendMessage(targets: list, message: list, date: str = "now") -> None:
    time_to_sleep = Utils.CalculateSleepTime(date)
    time.sleep(time_to_sleep)
    for target in targets:
        if "phone_number" in target:
            SendWhatsAppToNumber(target['phone_number'], message)
        elif "group_id" in target:
            SendWhatsAppToGroup(target['group_id'], message)
        else:
            raise AttributeError("A target has no valid attributes")

def SendImage(targets: list, image: str, caption: str = "", date: str = "now") -> None:
    time_to_sleep = Utils.CalculateSleepTime(date)
    time.sleep(time_to_sleep)
    for target in targets:
        if "phone_number" in target:
            SendWhatsAppImageToPhone(target['phone_number'], image, caption)
        elif "group_id" in target:
            SendWhatsAppImageToGroup(target['group_id'], image, caption)
        else:
            raise AttributeError("A target has no valid attributes")
