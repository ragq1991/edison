from random import randint
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets

psyhic_count = 4
lenght_num = 2


class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        # Создадим случайные номера
        Session.create_numbers(request)

        # Получим списки номеров
        psyhics = Session.get_numbers(request)

        # Получим уровень
        psyhics_level = Session.get_level(request)

        template = 'extrasences/index.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'psyhics': psyhics,
            'psyhics_level': psyhics_level
        }
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        # Получим списки номеров
        psyhics = Session.get_numbers(request)

        # Проставим уровни
        Session.set_level(request)

        # Получим уровни
        psyhics_level = Session.get_level(request)

        template = 'extrasences/index.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'psyhics': psyhics,
            'psyhics_level': psyhics_level
        }
        return render(request, template, context)


class Session(viewsets.ViewSet):
    # Получает из сессии по id список чисел, если такого id нет в сессии - создаст
    @staticmethod
    def get_from_session(request, psyhic_id):
        if psyhic_id not in request.session.keys():
            request.session[psyhic_id] = []
        return request.session[psyhic_id]

    # Записывает в сессию число в список по-соответствующему id, если такого id нет в сессии - создаст
    @staticmethod
    def set_to_session(request, psyhic_id, num):
        if psyhic_id not in request.session.keys():
            request.session[psyhic_id] = []
        psyhic_numbers = request.session[psyhic_id]
        psyhic_numbers.append(num)
        request.session[psyhic_id] = psyhic_numbers

    # Генерирует случайное число заданной длинны
    @staticmethod
    def get_guesswork(lenght):
        start = 10 ** (lenght - 1) - 1
        stop = 10 ** lenght
        return randint(start, stop)

    # Меняет уровни
    @staticmethod
    def set_level(request):
        user_num = int(request.POST.get('user_num'))
        i = 0
        for i in range(psyhic_count):
            i += 1
            if 'level' + str(i) not in request.session.keys():
                request.session['level' + str(i)] = 0
            physic_num = Session.get_from_session(request, str(i))[-1]
            if user_num == physic_num:
                request.session['level'+str(i)] = request.session['level'+str(i)] + 1
            else:
                request.session['level'+str(i)] = request.session['level'+str(i)] - 1

    # Возвращает список уровней
    @staticmethod
    def get_level(request):
        result = []
        i = 0
        for i in range(psyhic_count):
            i += 1
            if 'level' + str(i) not in request.session.keys():
                request.session['level' + str(i)] = 0
            result.append(request.session['level' + str(i)])
        return result

    # Создаёт случайные номера и записывает в сессию для каждого id
    @staticmethod
    def create_numbers(request):
        i = 0
        for i in range(psyhic_count):
            i += 1
            num = Session.get_guesswork(lenght_num)
            Session.set_to_session(request, str(i), num)

    # Возвращает список номеров по каждому id
    @staticmethod
    def get_numbers(request):
        result = []
        i = 0
        for i in range(psyhic_count):
            i += 1
            result.append(Session.get_from_session(request, str(i)))
        return result
