# -*- coding: utf-8 -*-

"""Matching KDE Services"""

import os
from functools import reduce
from albert import *

__title__ = "KDE Services"
__version__ = "0.2.1"
__authors__ = "Arto Manuel"

KDE_SERVICES_PATH = "/usr/share/kservices5/"

def get_services_path(query: str) -> list:
	services = []
	files = [file for file in os.listdir(KDE_SERVICES_PATH) if ".desktop" in file]
	for file_path in files:
		with open(KDE_SERVICES_PATH + file_path, 'r', encoding="utf-8") as f:
			for line in f.readlines():
				if "X-KDE-Keywords=" in line:
					if reduce(lambda prev, query: prev and (query in line.removeprefix("X-KDE-Keywords=").lower()), query.lower().split(' '), True):
						services.append(file_path)
	return services

def get_service_data(service_path: str) -> dict:
	data = {"Icon": "", "Name": "", "Comment": ""}
	with open(KDE_SERVICES_PATH + service_path, "r", encoding="utf-8") as file:
		for line in file.readlines():
			for key in data.keys():
				if key+"=" in line:
					data[key] = line.replace(key+"=", "").strip()
	return data

def handleQuery(query):
	if query.string:
		items = []
		services = get_services_path(query.string)
		for service_path in services:
			service_data = get_service_data(service_path)
			items.append(Item(
				id=service_data["Name"],
				icon=iconLookup(service_data["Icon"]),
				text=service_data["Name"],
				subtext=service_data["Comment"],
				actions=[
					ProcAction(text = f"kcmshell5 {service_path}", commandline=["kcmshell5", service_path])
				]
			))
		return items


if __name__ == "__main__":
	services  = get_services_path("kwin")
	for service_path in services:
		service_data = get_service_data(service_path)
		print()
		print(service_path, ":", service_data)