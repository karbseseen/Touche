from __future__ import annotations

import csv
from dataclasses import dataclass, field


@dataclass
class Lang:
	id: str
	name: str = ''
	index: int = -1
	data: dict[str, str] = field(default_factory=dict)
	def __getitem__(self, key: str): return self.data[key]

def _get_from_default(lang: Lang, key: str):
	value = lang.data.get(key, None)
	return value if value else _get_from_default(lang.default, key)


def _read():

	with open('translations.csv') as file:
		for row in csv.reader(file):
			key = row[0]
			if key == '_id':
				langs = { id: Lang(id) for id in row[1:] }
			elif key == '_default':
				for default_id, lang in zip(row[1:], langs.values()):
					if default_id:
						lang.default = langs[default_id]
			else:
				no_value: list[Lang] = []
				for value, lang in zip(row[1:], langs.values()):
					if value: lang.data[key] = value
					else: no_value.append(lang)
				for lang in no_value:
					lang.data[key] = _get_from_default(lang, key)
	lang_list = list(langs.values())
	lang_list.sort(key=lambda lang: lang.id)
	for index, lang in enumerate(lang_list):
		lang.index = index
		if hasattr(lang, 'default'):
			del lang.default
	return { lang.id: lang for lang in lang_list }


class Langs:
	all = _read()
	default = all['en']
	@classmethod
	def __class_getitem__(cls, lang_id: str):
		return cls.all.get(lang_id, cls.default)
