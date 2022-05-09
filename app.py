import telebot
from extensions import APIException, CriptoConverter
from config import TOKEN, keys

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f'Привет, {message.chat.username}. \nЯ бот и умею конвертировать валюты.\n \
Чтобы начать работу, введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>.\n-Вывести список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = f'{message.chat.username}, введите команду для конвертации валют в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>.\n-Вывести список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Не верное количество параметров. \n-Вывести условия ввода параметров: /help')

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(
            message, f'\n{e} \nВозможно Вы ошиблись. \nПовторите запрос.')
    except Exception as e:
        bot.reply_to(
            message, f'Не удалось обработать команду.\n{e} \nПовторите запрос.')
    else:
        text = f'Стоимость {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)



bot.polling()
