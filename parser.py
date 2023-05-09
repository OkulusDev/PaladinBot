#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""Телеграм-бот для изучения испанского языка: парсер
Создатель: Okulus Dev (C) 2023 ALL RIGHTS REVERSED | ВСЕ ПРАВА СОХРАНЕНЫ
Лицензия: GNU GPL v3"""
import requests
from datetime import datetime
import time
import json
from bs4 import BeautifulSoup


def get_first_news():
	# Получение новостей
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
	}

	url = "https://www.securitylab.ru/news"
	response = requests.get(url=url, headers=headers)

	soup = BeautifulSoup(response.text, "lxml")
	articles = soup.find_all("a", class_="article-card")

	news_dict = {}
	for article in articles:
		article_title = article.find('h2', class_='article-card-title').text.strip()
		article_description = article.find('p').text.strip()
		article_link = f"https://www.securitylab.ru{article.get('href')}"
		article_date_time = article.find('time').get("datetime")

		article_date_time = article.find('time').get('datetime')
		date_from_iso = datetime.fromisoformat(article_date_time)
		date_time = datetime.strftime(date_from_iso, '%y-%m-%d %H:%M')
		article_date_timestamp = time.mktime(datetime.strptime(date_time, '%y-%m-%d %H:%M').timetuple())

		article_id = article_link.split('/')[-1]
		article_id = article_id[:-4]

		try:
			with open('news.json', 'r') as file:
				news_list = json.load(file)

				if article_id in news_list:
					continue
				else:
					news_dict[article_id] = {
						"article_date_timestamp": article_date_timestamp,
						"article_title": article_title,
						"article_description": article_description,
						"article_link": article_link
					}
		except:
			with open('fresh_news.json', 'w') as file:
				news_dict[article_id] = {
					"article_date_timestamp": article_date_timestamp,
					"article_title": article_title,
					"article_description": article_description,
					"article_link": article_link
				}

		with open('fresh_news.json', 'w') as file:
			json.dump(news_dict, file, indent=4, ensure_ascii=False)
		with open('news.json', 'w') as file:
			json.dump(news_dict, file, indent=4, ensure_ascii=False)


def get_last_news():
	with open('fresh_news.json', 'r') as file:
		data = json.load(file)

	return data


def get_all_news():
	with open('news.json', 'r') as file:
		data = json.load(file)

	return data


if __name__ == '__main__':
	get_first_news()
