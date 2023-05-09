#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""Телеграм-бот для изучения испанского языка: базовое ядро
Создатель: Okulus Dev (C) 2023 ALL RIGHTS REVERSED | ВСЕ ПРАВА СОХРАНЕНЫ
Лицензия: GNU GPL v3"""
import config as cfg


def check_rights(user_id):
	for admin in cfg.ADMINS:
		if user_id == admin:
			return True
	return False
