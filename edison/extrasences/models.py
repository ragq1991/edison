from random import randint


class Gamer:
    numbers_history = []
    last_num = 0

    def __init__(self, numbers_history=None, last_num=0):
        if numbers_history is None:
            numbers_history = []
        self.numbers_history = numbers_history
        self.last_num = last_num

    def set_number(self, num):
        self.numbers_history.append(num)
        self.last_num = num

    def get_history(self):
        return self.numbers_history

    def get_last_num(self):
        return self.last_num


class Extra:
    name = ''
    level = 50
    numbers_history = []
    last_num = 0

    def __init__(self, name, level=50, numbers_history=None, last_num=0):
        if numbers_history is None:
            numbers_history = []
        self.level = level
        self.numbers_history = numbers_history
        self.name = name
        self.last_num = last_num

    def get_var(self, count=1, lenght=2):
        res_list = []
        start = 10 ** (lenght - 1)
        stop = 10 ** lenght - 1

        if count > 1:
            while count > 0:
                res_list.append(randint(start, stop))
            self.numbers_history.append(res_list)
            return res_list
        random_num = randint(start, stop)
        self.numbers_history.append(random_num)
        self.last_num = random_num
        return random_num

    def get_history(self):
        return self.numbers_history

    def check(self, gamer_num):
        if self.last_num == gamer_num:
            self.level += 1
        else:
            self.level -= 1

    def get_level(self):
        return self.level
