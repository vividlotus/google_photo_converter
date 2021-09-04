# -*- coding: utf-8 -*-
import datetime
import json



class JsonData:
    def __init__(self, json_file: str) -> None:
        self._data = self._load_json(json_file)
        self._warnings: list[str] = []


    def photo_taken_time(self):
        if 'photoTakenTime' not in self._data:
            self._warn('photoTakenTime', "no data")
            return None

        return self._convert_time_from_key('photoTakenTime')


    def _load_json(self, json_file: str):
        buf = open(json_file, 'r')
        return json.load(buf)


    def _convert_time_from_key(self, key: str):
        result = self._data[key]['formatted'].split(' ')
        date = result[0].split('/')
        time = result[1].split(':')
        zone = result[2]

        if zone != 'UTC':
            self._warn(key, "UTC以外のタイムゾーン")
            return None

        return datetime.timedelta(hours=9) + datetime.datetime(
            int(date[0]), int(date[1]), int(date[2]),
            int(time[0]), int(time[1]), int(time[2])
        )


    def _warn(self, key, message):
        self._warnings.append("[key: %s] message: %s, value: %s" % (key, message, self._data[key]))
