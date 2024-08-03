"""
telegram command handlers

all the handlers for the bot's commands goes here
"""

from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup,KeyboardButton
from predicter import Predictor,get_data

PREDICTOR = Predictor('history')

START_MSG = '''
Este bot es para la prediccion de valores en el casino virtual aviator. Para mas informacion sobre el uso,
use el comando /help
'''

HELP_MSG = '''
Las predicciones de este bot se basan en el historial de valores que hayan salido en momentos anteriores, para
alcanzar el maximo de efectividad, se debe haber recopilado una cantidad especifica de informacion continua 
durante un periodo de tiempo.

Para actualizar el historial, se debe pasar un mensaje en el cual los valores vistos deben aparecer, en dicho mensaje,
todo numero sera interpretado como un valor que ha salido.

Para obtener una prediccion, se ejecuta el comando /predict, este devuelve el valor mas probable por default. Si desea una lista de
los valores mas probables, a traves del comando /list se especifica la cantidad de resultados deseados.

Para mas informacion sobre como se hacen las predicciones use el comando /predict_details
'''

ACTIONS_MSG = '''
1. /predict Devuelve una lista con la cantidad especificada a traves del comando /list, de los posibles valores mas probables

2. /update <arguments> Cada uno de los valores pasados en los parametros es agregado a la base de datos de los valores que hayan salido
Eg: /update 1 1.2 34.56
WARNING!! los valores que no sean numeros seran ignorados

3. /predictx100class Devuelve una lista con la cantidad especificada a traves del comando /list, con los intervalos de ancho 100
mas probables
Eg: /predictx100class devuelve 0 <= x < 100 probability: 0.9

4. /predictx10class <menor> <mayor> Misma funcion que /predictx100class con el cambio de que hay que especificar el limite
inferior y el limite superior.
Eg: /predictx10class 100 200
WARNING!! si se proporciona una cantidad de argumentos distinta de 2, se devolvera un error de uso del comando

5. /predict_atomic_class <menor> <mayor> Mismo funcionamiento que el anterior. Devuelve la cifra de las unidades
mas probable en el rango definido

6. /predict_value <menor> <mayor> Mismo funcionamiento que el anterior. Devuelve el valor mas probable
WARNING!! los valores pasados como parametros deben ser enteros, otros valores pueden llevar a comportamientos
indefinidos
'''

buttons = [
    ['/help','/predict'],
    ['/predict_details','/list_actions'],
    
]

Buttons = ReplyKeyboardMarkup(buttons)

def check_params(*params):
    if not len(params) == 2: return False
    return True

async def start(update,context):
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=START_MSG,reply_markup=Buttons)
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def bot_help(update,context):
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=HELP_MSG)
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def list_size(update,context):
    try:
        PREDICTOR.set_result_limit(int(context.args[0]))
        await context.bot.send_message(chat_id=update.effective_chat.id,text='Cambio completado')
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def update_data(update,context):
    try:
        string = ''
        for value in context.args:
            string += f' {value}'
            pass
        for value in get_data(string):
            PREDICTOR.update(value)
            pass
        await context.bot.send_message(chat_id=update.effective_chat.id,text='Cambios completados')
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def menu(update,context):
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=ACTIONS_MSG)
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def predict(update,context):
    try:
        string = '\t\tPREDICTIONS'
        predictions = PREDICTOR.prediction
        for key in predictions.keys():
            string += f'\n\n{key} probability:\t\t {predictions[key]}'
            pass
        await context.bot.send_message(chat_id=update.effective_chat.id,text=string)
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def predictx100class(update,context):
    try:
        string = '\t\tPREDICTIONS'
        predictions = PREDICTOR.x100interval()
        for key in predictions[1].keys():
            string += f'\n\n{key} probability:\t\t {predictions[1][key]}'
            pass
        await context.bot.send_message(chat_id=update.effective_chat.id,text=string)
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def predictx10class(update,context):
    try:
        if not check_params(*context.args):
            await context.bot.send_message(chat_id=update.effective_chat.id,text='Solo se deben pasar dos argumentos')
            pass
        else:
            bottom,top = int(context.args[0]),int(context.args[1])
            string = '\t\tPREDICTIONS'
            predictions = PREDICTOR.x10interval(bottom,top)
            for key in predictions[1].keys():
                string += f'\n\n{key} probability:\t\t {predictions[1][key]}'
                pass
            await context.bot.send_message(chat_id=update.effective_chat.id,text=string)
            pass
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def predict_atomic_class(update,context):
    try:
        if not check_params(*context.args):
            await context.bot.send_message(chat_id=update.effective_chat.id,text='Solo se deben pasar dos argumentos')
            pass
        else:
            bottom,top = int(context.args[0]),int(context.args[1])
            string = '\t\tPREDICTIONS'
            predictions = PREDICTOR.atinterval(bottom,top)
            for key in predictions[1].keys():
                string += f'\n\n{key} probability:\t\t {predictions[1][key]}'
                pass
            await context.bot.send_message(chat_id=update.effective_chat.id,text=string)
            pass
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

async def predict_decimal_class(update,context):
    try:
        if not check_params(*context.args):
            await context.bot.send_message(chat_id=update.effective_chat.id,text='Solo se deben pasar dos argumentos')
            pass
        else:
            bottom,top = int(context.args[0]),int(context.args[1])
            string = '\t\tPREDICTIONS'
            predictions = PREDICTOR.dinterval(bottom,top)
            for key in predictions[1].keys():
                string += f'\n\n{key} probability:\t\t {predictions[1][key]}'
                pass
            await context.bot.send_message(chat_id=update.effective_chat.id,text=string)
            pass
        pass
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Error {ex}')
        pass
    pass

start_handler = CommandHandler('start',start)
help_handler = CommandHandler('help',bot_help)
list_handler = CommandHandler('list',list_size)
update_handler = CommandHandler('update',update_data)
menu_handler = CommandHandler('list_actions',menu)
predict_handler = CommandHandler('predict',predict)
predictx100_handler = CommandHandler('predictx100class',predictx100class)
predictx10_handler = CommandHandler('predictx10class',predictx10class)
predict_atomic_handler = CommandHandler('predict_atomic_class',predict_atomic_class)
predict_value_handler = CommandHandler('predict_value',predict_decimal_class)