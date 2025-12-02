from datetime import datetime
import random


class SixSevenException(Exception):
    six_seven = "six_seven"
    def __init__(self, detail):
        self.name = "This is a six seven exception!!! HYPE HYPE"
        self.detail = detail

    @property
    def time_of_occur(self):
        return datetime.now()


class JustAWrongNumberException(Exception):
    def __init__(self, reason):
        self.name = "Wrong number exception (is an abbreviation, because full number of this is ..."
        self.reason = reason

    @property
    def random_number(self):
        return random.choice([1,2,3,4,5,6,7,8,9,0])







