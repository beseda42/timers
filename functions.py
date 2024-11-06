import os
import threading
import time
import chime
from colorama import init
from colorama import Fore
import re

init() #инициализация colorama
#массив рабочих таймеров
running_arr = [0] * 10

def check_input():
    '''Проверка корректности ввода количества таймеров'''

    n = input(Fore.BLUE + "Введите количество таймеров, от 1 до 10 включительно:\n")

    while (not re.match(r'^-?\d+\.?\d*$', n)) or (int(n) < 1) or (int(n) > 10):
        if not re.match(r'^-?\d+\.?\d*$', n):
            print(Fore.YELLOW + "Введите целое число (цифрами)")
        elif (int(n) < 1) or (int(n) > 10):
            print(Fore.YELLOW + "Некорректное количество")
        n = input()

    return int(n)

def parse_time():
    '''Парсинг строки вида (s секунд m минут h часов) в любом порядке с возможностью отсутствия некоторых данных'''

    f = False
    while not f:
        str = input()

        match = re.match(r'(?:(\d+)\s*(?:секунд|секунды|секунда))?\s*(?:(\d+)\s*(?:минут|минуты|минута))?\s*(?:(\d+)\s*(?:часов|часа|час))?', str)
        sec = match.group(1)
        min = match.group(2)
        hour = match.group(3)

        res = 0
        if sec:
            res += int(sec)
        if min:
            res += 60 * int(min)
        if hour:
            res += 3600 * int(hour)

        if res != 0:
            f = True
        else:
            print(Fore.YELLOW + "Формат ввода: s секунд m минут h часов:\n")

    return res

def f_timer(id, period):
    '''Функция работы таймера, id=порядковый номер, period=время работы'''

    end_t = int(period) + int(time.time())

    while any (flag > 0 for flag in running_arr):
        if time.time() < end_t:
            running_arr[id] = int(end_t - time.time())
        else:
            running_arr[id] = 0

def time_formatting(sec):
    '''Функция превращения секунд в формат hh:mm:ss'''
    return f"{(sec//3600):02}:{((sec%3600)//60):02}:{(sec%60):02}"

def play_sound():
    '''Функция проигрывания звука завершения работы таймера'''
    chime.success()

def print_timers(n):
    '''Функция вывода таймеров в консоль'''
    os.system('cls')

    for i in range(n):
        if running_arr[i] == 0:
            print(Fore.CYAN + f"{i + 1} таймер сработал!")
        else:
            print(Fore.MAGENTA + f"{i + 1} таймер: осталось {time_formatting(running_arr[i])} секунд.")
        if running_arr[i] == 1:
            threading.Timer(1, play_sound).start()

    time.sleep(1)

#ввод количества таймеров
n = check_input()

#массив потоков
threads = []

#заполнение массива потоков и массива таймеров
for i in range (n):
    print(Fore.BLUE + f"Введите время для таймера {i+1} в виде (s секунд m минут h часов):\n")
    running_arr[i] = parse_time()
    threads.append(threading.Thread(target=f_timer, args= (i, running_arr[i], )))

#запуск потоков
for thread in threads:
    thread.start()

#вывод таймеров, пока работает хотя бы один
while any(flag > 0 for flag in running_arr):
    print_timers(n)

#финальный вывод таймеров
print_timers(n)

#проверка завершения потоков
for thread in threads:
    thread.join()
