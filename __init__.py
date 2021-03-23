# -*- coding: utf-8 -*-

"""Matching KDE Services"""

import os
from functools import reduce
from albert import *

__title__ = "KDE Services"
__version__ = "0.1.0"
__authors__ = "Arto Manuel"

KDE_SERVICES_PATH = "/usr/share/kservices5/"

def get_services(query_string) -> list:
	services: list = []
	files = [file for file in os.listdir(KDE_SERVICES_PATH) if ".desktop" in file]
	for file in files:
		with open(KDE_SERVICES_PATH + file, 'r', encoding="utf-8") as f:
			for line in f.readlines():
				if "X-KDE-Keywords=" in line:
					if reduce(lambda prev, query: prev and (query in line[15:]), query_string.split(' '), True):
						services.append(file)
	return services

def get_service_data(service_path: str) -> dict:
	data = {"Exec": "", "Icon": "", "Name": "", "Comment": "", "X-KDE-Keywords": ""}
	with open(KDE_SERVICES_PATH + service_path, "r", encoding="utf-8") as file:
		for line in file.readlines():
			for key in data.keys():
				if key+"=" in line:
					data[key] = line.replace(key+"=", "").strip() 
	return data

def handleQuery(query):
	if query.string:
		items = []
		services = get_services(query.string)
		for service_path in services:
			service_data = get_service_data(service_path)
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

if __name__ == "__main__":
	services  = get_services("kwin")
	for service in services:
		service_data = get_service_data(service)
		print()
		print(service_data)
	else:
		print("No services", services)
