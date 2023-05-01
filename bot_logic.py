import logging
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from settings import *
from database import register_user, update_score, get_score, \
    get_best_score
from keybords import kb_client

# Initialization using a direct connection
bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


# Set of auxiliary functions

def load_cities_dict():
    # chr(1040) - 'А', chr(1072) - 'Я'
    # Use your own 'A to Z' range specific to your language in settings.py
    cities_dict = {chr(l): [] for l in range(LOCAL_A, LOCAL_Z + 1)}
    with open(LIST_OF_CITIES, 'r', encoding='utf-8') as f_input:
        for line in f_input:
            c = line[0]
            cities_dict[c].append(line.rstrip('\n'))
    return cities_dict


def valid_city(city):
    # Checks whether we have this city or not
    return True if city[0] in game_state['cities'] and city in \
                   game_state['cities'][city[0]] else False


def find_last_char(city):
    i = -1
    while city[i] in game_state['empty_letters']:
        i -= 1
    return city[i]


def find_city_for(letter):
    if game_state['cities'][letter]:
        random.shuffle(game_state['cities'][letter])
        return game_state['cities'][letter].pop()
    else:
        return 'error'


@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    chat_id = message.from_user.id
    username = message.from_user.username
    if get_score(message.from_user.username) != -1:
        success, response = register_user(chat_id, username)
        score = get_score(username)
        best_score = get_best_score(username)
    else:
        success = True
        score = -1
    if success:
        game_state['cities'] = load_cities_dict()
        game_state['playing'] = True
        game_state['city_char'] = ''
        game_state['empty_letters'] = [chr(i) for i in range(LOCAL_A,
                                                             LOCAL_Z + 1)
                                       if not game_state['cities'][chr(i)]]

        if score == -1:
            await message.answer(
                f"Хочешь сыграть снова, {username}? Твой счёт обнулён, поехали! Рекорд: {get_best_score(username)}")
            update_score(message.from_user.username, 0)
        else:
            await message.answer(
                f"Молодец, {username}, ты успешно зарегистрировался.\n"
                f"Твой счёт равен {score}. Лучший счёт {best_score}.\n"
                "Давай начнём игру: ты ходишь первым.")

    else:
        await message.answer(response)


@dp.callback_query_handler(lambda query: query.data == 'help')
async def help_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, HELP_MSG)


@dp.callback_query_handler(lambda query: query.data == 'stop')
async def stop_game_callback(callback_query: types.CallbackQuery):
    game_state['playing'] = False
    update_score(callback_query.from_user.username, -1)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, GAME_STOPPED_MSG)


@dp.message_handler()
async def play_game(message: types.Message):
    current_city = message.text.strip().upper()
    reply_msg = ''
    chat_id = message.from_user.id
    username = message.from_user.username
    if not game_state['playing']:
        await message.reply(START_GAME_MSG)
    elif current_city[0] == game_state['city_char'] or game_state[
        'city_char'] == '':
        if valid_city(current_city):
            game_state['cities'][current_city[0]].remove(current_city)
            ch = find_last_char(current_city)
            reply_msg = 'Мне на букву {} \n\n'.format(ch)
            city = find_city_for(ch)
            if city != 'error':
                reply_msg += '{} \n\n'.format(city)
                game_state['city_char'] = find_last_char(city)
                reply_msg += 'Тебе на букву {}'.format(game_state['city_char'])
                update_score(username,
                             get_score(username) + 1)  # увеличить счёт
                score = get_score(username)
                reply_msg += f"\n\nТвой текущий счет: {score}. Твой лучший счёт {get_best_score(username)}"
                await bot.send_message(message.chat.id, reply_msg,
                                       reply_markup=kb_client)
            else:
                reply_msg += 'Города на букву {} закончились. Я проиграл :('.format(
                    ch)
                # await stop_game_callback_handler(types.CallbackQuery)
                await message.reply(reply_msg)
        else:
            await message.reply(MISSPELLED_OR_REPEAT_MSG)
    else:
        reply_msg = 'Вспомни правила! Тебе на букву {} \n'.format(
            game_state['city_char'])
        reply_msg += 'Help - прочитать правила игры'
        await bot.send_message(message.chat.id, reply_msg,
                               reply_markup=kb_client)
