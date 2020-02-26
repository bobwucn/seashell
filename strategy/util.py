import time, datetime

def getTimeByTimestamp(ts):
    timeArray = time.localtime(ts/1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return  otherStyleTime

def getTSByTime(timestr):
    timeArray = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))*1000
    return timeStamp
def getTimeArrayByTimeStr(timestr):
    return time.strptime(timestr, "%Y-%m-%d %H:%M:%S")


    