import time
import json
import random
import Utils
import WhatsApp

def Help():
    pass

def ExecutionMode_0(targets: list, message: list) -> None:

    if "date" not in message:
        raise ValueError("The date is mandatory in the execution_mode 0, please specify one.")
    
    try:

        Utils.WaitForInternetConnection()

        if ('path' in message) and (message['path'] != ""):
            final_message = Utils.ReadFullFile(message['path'])
            WhatsApp.SendMessage(targets, final_message, message['date'])

        elif 'message' in message:
            WhatsApp.SendMessage(targets, message['message'], message['date']) 

        else:
            raise AttributeError("Attribute that contains the message is not found, or the attributes found are incorrect.")

    except Exception as e:
        print(e)
        
def ExecutionMode_1(targets: list, messages: list) -> None:

    if not (('path' in messages) and (messages['path'] != "")):
        raise AttributeError("Attribute that contains the path to the messages is not found or is empty.")

    if "time" not in messages or "interval" not in messages['time']:
        raise AttributeError("Attribute with time information, like interval or how many times the program should run, is not found in the configuration.")

    if messages['time']['times'] <= 0:
        raise ValueError("The attribute times, that represents how many times the program should run, must be at least 1")

    try:

        interval = messages['time']['interval']
        times = messages['time']['times']
        interval_in_seconds = int(Utils.MakeStringParsable(interval)) if interval.count('h') == 0 else int(Utils.MakeStringParsable(interval))*3600
        data = Utils.ReadFullFile(messages['path']).split(messages['separator'])

        try:
            if "start" in messages['time']:
                time_to_sleep = Utils.CalculateSleepTime(messages['time']['start'])
        except:
            time_to_sleep = 0

        time.sleep(time_to_sleep)

        for i in range(times):
            if "random" not in messages or not messages['random']:
                message = data[0]; data.pop(0)
            else:
                message = random.choice(data); data.remove(message)

            Utils.WaitForInternetConnection()
            start_time = time.time()
            WhatsApp.SendMessage(targets, message)
            time.sleep(interval_in_seconds - (time.time() - start_time))

            if len(data) == 0 and i < times:
                data = Utils.ReadFullFile(messages['path']).split(messages['separator'])
            
    except Exception as e:
        print(e)
    
def ExecutionMode_2(targets: list, snaps_config: list) -> None:
    
    if "path" not in snaps_config or snaps_config['path'] == "":
        path = "Images"
    else:
        path = snaps_config['path']

    if "time" not in snaps_config or "interval" not in snaps_config['time']:
        raise AttributeError("Attribute with time information, like interval or how many times the program should run, is not found in the configuration.")

    if snaps_config['time']['times'] <= 0:
        raise ValueError("The attribute times, that represents how many times the program should run, must be at least 1")

    try:

        interval = snaps_config['time']['interval']
        times = snaps_config['time']['times']
        interval_in_seconds = int(Utils.MakeStringParsable(interval)) if interval.count('h') == 0 else int(Utils.MakeStringParsable(interval))*3600

        try:
            if "start" in snaps_config['time'] and snaps_config['time'] != "":
                time_to_sleep = Utils.CalculateSleepTime(snaps_config['time']['start'])
        except:
            time_to_sleep = 0

        time.sleep(time_to_sleep)

        for i in range(times):
            if snaps_config['type'] == 0:
                image = Utils.TakeSnap(path)
            else:
                image = Utils.TakeScreenshot(path)
            Utils.WaitForInternetConnection()
            if "caption" in snaps_config:
                caption = snaps_config['caption'].replace("{date}",Utils.GetTimestamp())
            else:
                caption = ""
            start_time = time.time()
            WhatsApp.SendImage(targets, image, caption)
            time.sleep(interval_in_seconds - (time.time() - start_time))
            
    except Exception as e:
        print(e)

def main():
    with open('config.json') as f:
        config = json.load(f)
    if config['execution_mode'] == 0:
        ExecutionMode_0(config['targets'], config['message'])
    elif config['execution_mode'] == 1:
        ExecutionMode_1(config['targets'], config['messages'])
    elif config['execution_mode'] == 2:
        ExecutionMode_2(config['targets'], config['snaps'])
    else:
        Help()
    
if __name__ == "__main__":
    main()