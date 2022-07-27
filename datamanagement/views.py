import telepot
from datamanagement.background_functions import working_days
from django.shortcuts import render
from .strategy import *
# Create your views here.
from django.contrib import messages
import threading
from datamanagement.models import strategy
import random
import string
from .models import positions, orders, strategy
from .background_functions import *
from smartapi import SmartConnect
obj = SmartConnect(api_key="uWbpZyYm")
data = obj.generateSession("S776051", "Madhya246###")
refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()
userProfile = obj.getProfile(refreshToken)


bot = telepot.Bot("5448843199:AAEKjMn2zwAyZ5tu8hsLIgsakxoLf980BoY")
bot.getMe()

working_day_calculation(0)


def index(request):

    return render(request, "index.html")


def position(request):

    strategies = strategy.objects.filter(status="OPEN")
    lists = []
    strategy_id = []

    for i in range(len(strategies)):

        position = positions.objects.filter(
            strategy_id=strategies[i].strategy_id)
        position_list = []
        for j in range(len(position)):
            position_list.append(position[j])
            print(position[j].time_in)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        lists.append(position_list)
        strategy_id.append(strategies[i].strategy_id)

    return render(request, "position.html",    {
        'list': lists,
        'strategy_id': strategy_id
    })


def start_strategy(request):
    print(request)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    
    if request.method == "POST":
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        buy_factor = request.POST['buy_factor']
        per_premium = request.POST['per_premium']
        TP1 = request.POST['TP1']
        TP2 = request.POST['TP2']
        timeout = request.POST['timeout']
        sell_factor = request.POST['sell_factor']
        lot = request.POST['lot']
        et = request.POST['et']
        try:
            type = str(request.POST['type'])

        except:
            type = 'off'


        rand_str = random_string_generator(10, string.ascii_letters)
        # obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
        user = User1.objects.get(username='testing')

        strategy1 = strategy(

            strategy_id=rand_str,
            buy_factor=buy_factor,
            sell_factor=sell_factor,
            percentage_premium=per_premium,
            TP1=TP1,
            TP2=TP2,
            time_out=timeout,
            LIMIT=type,
            lot=lot,
            status="OPEN",
            ET=et,
            working_days_1=user.working_days_1,
            working_days_2=user.working_days_2,
            expiry_1=user.expiry_1,
            expiry_2=user.expiry_2,
            T_now=3

        )

        strategy1.save()

        strategy1 = strategy.objects.get(strategy_id=rand_str)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


        t = threading.Thread(target=do_something, args=[strategy1])
        t.setDaemon(True)
        t.start()

        # do_something(strategy1)

        strtegy12=20
        print("hello")
        return render(request, "index.html")


def do_something(strategy):
    print("$#################@@@@@@@@")
    strat = run_strategy(strategy)
    strat.run()

    # messages
    # while True:
    #     print(data)


def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))
