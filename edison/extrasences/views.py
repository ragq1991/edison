from random import randint
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from .serialaizers import SessionSerializer

psyhic_count = 2
lenght_num = 2

names = ['Поликарп', 'Аполинарий', 'Всеволон', 'Аксондриан', 'Камнотилий']


class Start(TemplateView):
    def get(self, request, *args, **kwargs):
        template = 'extrasences/start.html'
        context = {
            'title': 'Портал экстрасенсов',
        }
        return render(request, template)


class Step1(TemplateView):
    def get(self, request, *args, **kwargs):
        data = Process.step_1(request, 2)
        template = 'extrasences/step_1.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'data': data,
        }
        return render(request, template, context)


class Step2(TemplateView):
    def get(self, request, *args, **kwargs):
        template = 'extrasences/step_2.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'error': False,
            'value': ''
        }
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        gamer_num = request.POST.get('gamer_num')
        if gamer_num.isdigit():
            gamer_num = int(gamer_num)
            if 9 < gamer_num < 99:
                Process.Step_2(request, gamer_num)
                return redirect(to='finish')

        template = 'extrasences/step_2.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'error': True,
            'value': gamer_num
        }
        return render(request, template, context)


class Finish(TemplateView):
    def get(self, request, *args, **kwargs):
        data = Process.finish(request)
        template = 'extrasences/finish.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'extra': data['extra'],
            'gamer': data['gamer']
        }
        return render(request, template, context)


class Gamer:
    numbers = []
    last_num = 0

    def __init__(self, numbers=None, last_num=0):
        if numbers is None:
            numbers = []
        self.numbers = numbers
        self.last_num = last_num

    def set_number(self, num):
        self.numbers.append(num)
        self.last_num = num

    def get_history(self):
        return self.numbers

    def get_last_num(self):
        return self.last_num


class Extra:
    name = ''
    level = 50
    numbers = []
    last_num = 0

    def __init__(self, name, level=50, numbers=None, last_num = 0):
        if numbers is None:
            numbers = []
        self.level = level
        self.numbers = numbers
        self.name = name
        self.last_num = last_num

    def get_vars(self, count=1, lenght=2):
        res_list = []
        start = 10 ** (lenght - 1)
        stop = 10 ** lenght - 1

        if count > 1:
            while count > 0:
                res_list.append(randint(start, stop))
            self.numbers.append(res_list)
            return res_list
        random_num = randint(start, stop)
        self.numbers.append(random_num)
        self.last_num = random_num
        return random_num

    def get_history(self):
        return self.numbers

    def check(self, gamer_num):
        if self.last_num == gamer_num:
            self.level += 1
        else:
            self.level -= 1

    def get_level(self):
        return self.level


class Process:
    @staticmethod
    def step_1(request, extra_count):
        extra_dict = {}
        data = SessionSerializer.fr(request)
        if 'extra' in data:
            extra = data['extra']
            for key, value in extra.items():
                extra = Extra(value['name'], value['level'], value['numbers'], value['last_num'])
                extra.get_vars()
                extra_dict[key] = extra.__dict__

        else:
            while extra_count > 0:
                extra = Extra(names[randint(0, len(names)-1)])
                extra.get_vars()
                extra_dict[extra_count] = extra.__dict__
                extra_count -= 1

        data['extra'] = extra_dict
        SessionSerializer.to(request, data)

        return extra_dict

    @staticmethod
    def Step_2(request, gamer_num):
        data = SessionSerializer.fr(request)
        if 'gamer' in data:
            gamer = Gamer(data['gamer']['numbers'], int(data['gamer']['last_num']))
        else:
            gamer = Gamer()

        gamer.set_number(gamer_num)
        data['gamer'] = gamer.__dict__
        SessionSerializer.to(request, data)

    @staticmethod
    def finish(request):
        extra_dict = {}
        data = SessionSerializer.fr(request)
        extra = data['extra']
        gamer = Gamer(data['gamer']['numbers'], int(data['gamer']['last_num']))
        for key, value in extra.items():
            extra = Extra(value['name'], value['level'], value['numbers'], int(value['last_num']))
            extra.check(gamer.get_last_num())
            extra_dict[key] = extra.__dict__

        data['extra'] = extra_dict
        SessionSerializer.to(request, data)

        return data
