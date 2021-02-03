# -*- coding: utf-8 -*-

"""Matching KDE Services"""

import os
from functools import reduce
from albert import *

__title__ = "KDE Services"
__version__ = "0.1.0"
__authors__ = "Arto Manuel"

KDE_SERVICES_PATH = "/usr/share/kservices5/"

def get_services(query_string):
	files = [file for file in os.listdir(KDE_SERVICES_PATH) if ".desktop" in file]
	for file in files:
		has_exec = False
		with open(KDE_SERVICES_PATH + file, 'r') as f:
			for line in f.readlines():
				if "Exec=" in line:
					has_exec = True
				if "X-KDE-Keywords=" in line:
					if has_exec and reduce(lambda prev, query: prev and (query in line[15:]), query_string.split(' '), True):
						yield file

def get_service_data(service):
	data = {"Exec": "", "Icon": "", "Name": "", "Comment": "", "X-KDE-Keywords": ""}
	with open(KDE_SERVICES_PATH + service) as file:
		for line in file.readlines():
			for key in data.keys():
				if key+"=" in line:
					data[key] = line.replace(key+"=", "").strip() 
	return data

def handleQuery(query):
	if query.string:
		items = []
		for service in get_services(query.string):
			service_data = get_service_data(service)
			items.append(Item(
				id=service_data["Name"],
				icon=iconLookup(service_data["Icon"]),
				text=service_data["Name"],
				subtext=service_data["Comment"],
				actions=[
					ProcAction(text=service_data["Exec"], commandline=service_data["Exec"].split())
				]
			))
		return items
