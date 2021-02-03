"""KDE Services"""

import os
from functools import reduce
from albert import *

__title__ = "KDE Services"
__version__ = "0.1.0"
__authors__ = "Arto Manuel"

kde_services_path = "/usr/share/kservices5/"
def get_services(query_string):
	files = [file for file in os.listdir(kde_services_path) if ".desktop" in file]
	for file in files:
		has_exec = False
		with open(kde_services_path + file, 'r') as f:
			for line in f.readlines():
				if "Exec=" in line:
					has_exec = True
				if "X-KDE-Keywords=" in line:
					if reduce(lambda prev, query: prev and (query in line[15:]), query_string.split(' '), True) and has_exec:
						yield file

def get_service_data(service):
	data = {"Exec": "", "Icon": "", "Name": "", "Comment": "", "X-KDE-Keywords": ""}
	with open(kde_services_path + service) as file:
		for line in file.readlines():
			if "Exec=" in line:
				data["Exec"] = line.replace("Exec=", "").strip()
			elif "Icon=" in line:
				data["Icon"] = iconLookup(line.replace("Icon=", "").strip())
			elif "Name=" in line: 
				data["Name"] = line.replace("Name=", "").strip()
			elif "Comment=" in line: 
				data["Comment"] = line.replace("Comment=", "").strip()
			elif "X-KDE-Keywords=" in line:
				data["X-KDE-Keywords"] = line.replace("X-KDE-Keywords=", "").strip()
	return data

def handleQuery(query):
	if query.string:
		items = []
		for service in get_services(query.string):
			service_data = get_service_data(service)
			items.append(Item(
				id=service_data["Name"],
				icon=service_data["Icon"],
				text=service_data["Name"],
				subtext=service_data["Comment"],
				actions=[
					ProcAction(text=service_data["Exec"], commandline=service_data["Exec"].split())
				]
			))
		return items
