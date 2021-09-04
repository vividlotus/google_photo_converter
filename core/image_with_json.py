# -*- coding: utf-8 -*-

class ImageWithJson:
    def __init__(self, image_file: str, json_file: str) -> None:
        self.image_file = image_file
        self.json_file = json_file


    def __str__(self) -> str:
        return "image_file: %s, json_file: %s" % (self.image_file, self.json_file)
