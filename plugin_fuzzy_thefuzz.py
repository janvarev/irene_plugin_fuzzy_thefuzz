# Fuzzy comparing by thefuzz lib (https://github.com/seatgeek/thefuzz )
# author: Vladislav Janvarev

import os

from vacore import VACore
from thefuzz import fuzz

modname = os.path.basename(__file__)[:-3] # calculating modname
options = {}

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "Fuzzy text by TheFuzz lib",
        "version": "2.0",
        "require_online": False,

        "options_label": {
            "strict": "Использовать более строгое сравнение строк (ratio вместо Wratio)",  #
        },

        "default_options": {
            "strict": False
        },

        "fuzzy_processor": {
            "thefuzz": (init,predict) # первая функция инициализации, вторая - обработка
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    global options
    options = manifest["options"]
    #print('thefuzzy',options)
    #pass

def init(core:VACore):
    pass

def predict(core:VACore, command:str, context:dict, allow_rest_phrase:bool = True): # на входе -
            # команда; текущий контекст в формате Ирины; разрешен ли остаток фразы, или это фраза целиком
    bestres = 0
    bestret = None

    for keyall in context.keys():
        keys = keyall.split("|")
        for key in keys:
            if allow_rest_phrase: # разрешены остатки фраз? сравниваем только с началом
                cmdsub = command[0:len(key)]
                rest_phrase = command[(len(key)+1):]
            else:
                cmdsub = command
                rest_phrase = ""
            # print("Subcmd: ",cmdsub,key)

            if options["strict"]:
                res = fuzz.ratio(cmdsub, key)  # для всех ключей вычисляем схожесть
            else:
                res = fuzz.WRatio(cmdsub,key) # для всех ключей вычисляем схожесть

            if res > bestres:
                bestres = res
                bestret = (keyall,float(res)/100,rest_phrase)

    return bestret


