
from datetime import *
import random


class date_time:
    def __init__(self, initTime: datetime = None):
        self.__dateTime = initTime
        if initTime is None:
            self.__dateTime = datetime.utcnow()

    def getKorTime(self):
        return self.__dateTime + timedelta(hours=9)

    def getUtcTime(self):
        return self.__dateTime


def getNextRandomDate():
    current = date_time()
    hour = random.randint(0, 25)
    minute = random.randint(0, 60)
    return current.getUtcTime() + timedelta(hours=hour, minutes=minute)

