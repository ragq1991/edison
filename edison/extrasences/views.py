from random import randint
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .serialaizers import *
from .models import *

extra_count = 2

names = ['Поликарп', 'Аполинарий', 'Всеволон', 'Аксондриан', 'Камнотилий']


class Index(TemplateView):
    def get(self, request, *args, **kwargs):

        # gamer = Gamer(numbers_history=[10, 12, 14, 16], last_num=16)
        # ser = GamerSerializer(gamer)
        # ser.save_to_session(request)
        # print()
        # ser = GamerSerializer()
        # gamer2 = ser.create_from_session(request)
        # print()
        #
        # idx = randint(0, len(names) - 1)
        # extra = Extra(names[idx], level=50, numbers_history=[10, 15, 32, 99], last_num=99)
        # names.pop(idx)
        # ser = ExtraSerializer(extra)
        # ser.save_to_session(request)
        # idx = randint(0, len(names) - 1)
        # extra = Extra(names[idx], level=50, numbers_history=[10, 15, 32, 99], last_num=99)
        # names.pop(idx)
        # ser = ExtraSerializer(extra)
        # ser.save_to_session(request)
        # print()
        # ser = ExtraSerializer()
        # extra_dict = ser.create_from_session(request)
        #
        # print()

        template = 'extrasences/Index.html'
        context = {
            'title': 'Портал экстрасенсов',
        }
        return render(request, template, context)


class ProvidingOptions(TemplateView):
    def get(self, request, *args, **kwargs):
        # Запросим словарик экстрасенсов у сериализатора (из сессии)
        ser = ExtraSerializer()
        extra_dict = ser.create_from_session(request)

        # Если там есть экстрасенсы
        if extra_dict:
            for extra in extra_dict:
                # Создание у экстрасенса вариантов
                extra_dict[extra].get_var()

        # А если их там нет, то значит это первый цикл игрока и экстрасенсов нужно создать с нуля
        else:
            extra_dict = {}
            for i in range(extra_count):
                # Создание экстрасенса
                idx = randint(0, len(names) - 1)
                extra = Extra(names[idx])
                names.pop(idx)

                # Создание у экстрасенса вариантов
                extra.get_var()

                # Запись экстрасенса в словарь
                extra_dict[i] = extra

        # Отдадим сериалайзеру для записи в сессию экстрасенса
        for extra in extra_dict:
            ser = ExtraSerializer(extra_dict[extra])
            ser.save_to_session(request)

        template = 'extrasences/ProvidingOptions.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'data': extra_dict,
        }
        return render(request, template, context)


class UserSetNumber(TemplateView):
    def get(self, request, *args, **kwargs):
        template = 'extrasences/UserSetNumber.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'error': False,
            'value': ''
        }
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        # Получим число от игрока
        gamer_num = request.POST.get('gamer_num')

        # Проверим
        if gamer_num.isdigit():
            gamer_num = int(gamer_num)
            if 9 < gamer_num < 100:

                # Запросим игрока у сериализатора (из сессии)
                ser = GamerSerializer()
                gamer = ser.create_from_session(request)

                # если нет, создадим с нуля
                if gamer is None:
                    gamer = Gamer()

                # Запишем число загаданное игроком
                gamer.set_number(gamer_num)

                # Отдадим сериалайзеру для записи в сессию
                ser = GamerSerializer(gamer)
                ser.save_to_session(request)

                # Отправим игрока на страницу результатов
                return redirect(to='Results')

        template = 'extrasences/UserSetNumber.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'error': True,
            'value': gamer_num
        }
        return render(request, template, context)


class Results(TemplateView):
    def get(self, request, *args, **kwargs):
        # Запросим словарик экстрасенсов и игрока у сериализатора (из сессии)
        ser = ExtraSerializer()
        extra_dict = ser.create_from_session(request)
        ser = GamerSerializer()
        gamer = ser.create_from_session(request)

        # Пробежимся по всем экстрасенсам
        for extra in extra_dict:
            # сообщаем число загаданное игроком, тем самым меняем уровень экстрасенса
            extra_dict[extra].check(gamer.get_last_num())

            # Отдадим сериалайзеру для записи в сессию экстрасенса
            test = extra_dict[extra]
            ser = ExtraSerializer(test)
            ser.save_to_session(request)

        template = 'extrasences/Results.html'
        context = {
            'title': 'Тестирование экстрасенсов',
            'extra_dict': extra_dict,
            'gamer': gamer
        }
        return render(request, template, context)
