#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""Телеграм-бот для администрирования канала
Создатель: Okulus Dev (C) 2023 ALL RIGHTS REVERSED | ВСЕ ПРАВА СОХРАНЕНЫ
Лицензия: GNU GPL v3"""
import json
import datetime
import telebot												# Импорт pytelegrambotapi
from telebot import types									# Импорт типов pytelegrambotapi

import config as cfg										# Импорт конфигурации
import core
import parser

# Создание бота
bot = telebot.TeleBot(cfg.TOKEN)


def alert():
	# Оповещаем администраторов о запуске бота
	for admin in cfg.ADMINS:
		bot.send_message(admin, 'Бот запущен!')


def send_to_channel(message):
	# Пересылаем сообщение в канал
	bot.send_message(cfg.CHANNEL, f'{message.text}')


@bot.message_handler(commands=['start'])
def start(message):
	# Проверяем, администратор ли пользоователь
	if core.check_rights(message.from_user.id):
		bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.username}')
	else:
		bot.send_message(message.chat.id, 'Вы не обладаете правами администратора!')


@bot.message_handler(commands=['add_post'])
def add_post(message):
	# Проверяем, администратор ли пользоователь
	if core.check_rights(message.from_user.id):
		bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.username}')
	else:
		bot.send_message(message.chat.id, 'Вы не обладаете правами администратора!')
		return

	mesg = bot.send_message(message.chat.id, 'Введите текст поста:')
	bot.register_next_step_handler(mesg, send_to_channel)


@bot.message_handler(commands=['fresh_news'])
def fresh_news(message):
	# Получение свежих новостей
	try:
		with open('fresh_news.json', 'r') as file:
			news_dict = json.load(file)
	except:
		try:
			parser.get_first_news()
		except:
			bot.send_message(message.chat.id, 'Новых сообщений не было...')
		else:
			with open('fresh_news.json', 'r') as file:
				news_dict = json.load(file)
	else:
		for k, v in sorted(news_dict.items()):
			news = f'''⚠️ <b>{v["article_title"]}</b> ⚠️

			{v["article_description"]}

			<i>{datetime.datetime.fromtimestamp(v["article_date_timestamp"])}</i>
			<a href="{v["article_link"]}">Источник</a>'''

			bot.send_message(cfg.CHANNEL, news, parse_mode='HTML')


@bot.message_handler(commands=['all_posts'])
def all_posts(message):
	# Получение всех новостей
	with open('news.json', 'r') as file:
		news_dict = json.load(file)

	for k, v in sorted(news_dict.items()):
		news = f'''⚠️ <b>{v["article_title"]}</b> ⚠️

		{v["article_description"]}

		<i>{datetime.datetime.fromtimestamp(v["article_date_timestamp"])}</i>
		<a href="{v["article_link"]}">Источник</a>'''

		bot.send_message(cfg.CHANNEL, news, parse_mode='HTML')


if __name__ == '__main__':
	# Запуск бота
	print('Бот запущен. CTRL+C для прерывания')
	alert()

	bot.infinity_polling()
