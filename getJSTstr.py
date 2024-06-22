import ntptime
import time

def getJSTstr():
    try:
        jst = ntptime.time() + 3600 * 9
        tm = time.localtime(jst)
        year = int(tm [0])
        month = int(tm [1])
        day = int(tm [2])
        hour = int(tm [3])
        minute = int(tm [4])
        second = int(tm [5])
        res = f'{year}/{month:0=2}/{day:0=2} {hour:0=2}:{minute:0=2}'
        return res
    except:
        return 'cannot get time'
    
if __name__ == "__main__":
    print(getJSTstr())