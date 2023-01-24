# Fuzzy comparing by thefuzz lib (https://github.com/seatgeek/thefuzz )
# author: Vladislav Janvarev

import os

from vacore import VACore
from thefuzz import fuzz

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "Fuzzy text by TheFuzz lib",
        "version": "1.0",
        "require_online": False,

        "fuzzy_processor": {
            "thefuzz": (init,predict) # первая функция инициализации, вторая - обработка
        }
    }
    return manifest

def init(core:VACore):
    pass

def predict(core:VACore, command:str, context:dict): # на входе - команда + текущий контекст в формате Ирины
    bestres = 0
    bestret = None

    for keyall in context.keys():
        keys = keyall.split("|")
        for key in keys:
            cmdsub = command[0:len(key)]
            #print("Subcmd: ",cmdsub,key)

            res = fuzz.ratio(cmdsub,key) # для всех ключей вычисляем схожесть
            if res > bestres:
                bestres = res
                bestret = (keyall,float(res)/100,command[(len(key)+1):])
                # возвращаем тройку: ключ команды, уверенность (от 0 до 1), остаток фразы.

    return bestret


