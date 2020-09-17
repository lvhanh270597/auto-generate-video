from datetime import date

class Timer :

    def convertToString(self, seconds) :
        seconds = int(seconds)
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
        seconds -= minutes * 60
        hours = '0' + str(hours) if hours < 10 else str(hours)
        minutes = '0' + str(minutes) if minutes < 10 else str(minutes)
        seconds = '0' + str(seconds) if seconds < 10 else str(seconds)
        return '{0}:{1}:{2}'.format(hours, minutes, seconds)
    
    def convertToInt(self, string) :
        hours, minutes, seconds = list(map(float, string.split(':')))
        return int(hours * 3600 + minutes * 60 + seconds)
    
    def getTodayString(self) :
        today = date.today()
        today = today.strftime("%Y%m%d")
        return today