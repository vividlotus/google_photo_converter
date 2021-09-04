# -*- coding: utf-8 -*-
import glob
import os
import re

from .image_with_json import ImageWithJson



class Finder:
    def __init__(self, target_path: str, include_ext: list[str]) -> None:
        self.target_path = target_path
        self.include_ext = include_ext


    def get_files(self, recursive: bool = False) -> list[ImageWithJson]:
        """
        ファイル一覧を取得
        """
        return self._get_files(recursive)


    def _get_files(self, recursive: bool = False) -> list[ImageWithJson]:
        targets: list[ImageWithJson] = []

        pattarn = "%s*" % self.target_path
        if recursive:
            pattarn = "%s**/*" % self.target_path

        image_files = sorted([p for p in glob.glob(pattarn, recursive=recursive) if re.search("/.*?\.(%s)$" % '|'.join(self.include_ext), str(p), re.IGNORECASE)])
        for image_file in image_files:
            json_file = self._get_json_from_image(image_file)
            if json_file is None:
                continue

            targets.append(ImageWithJson(image_file, json_file))

        return targets


    def _get_json_from_image(self, image_file: str):
        """
        画像ファイルパスからJSONファイルパスを取得する
            note
                GooglePhotoをエクスポートした際、同名のファイル名は
                拡張子の後ろに(\d+)のフォーマットで数字がつくので
                それをヒントにjsonファイルを特定する
                ファイル名が重複しないならjsonファイルは画像と同じファイル名
        """
        json_file = self._convert_json_filename(image_file)
        if json_file is None or not os.path.exists(json_file) or not os.path.isfile(json_file):
            json_file = None

        return json_file


    def _convert_json_filename(self, image_file: str):
        result = re.match("^(.*?)\((\d+)\)\.(%s)$" % '|'.join(self.include_ext), image_file, re.IGNORECASE)
        if result:
            base = result.group(1)
            num = result.group(2)
            ext = result.group(3)
            filename = "%s.%s(%s).json" % (base, ext, num)
            if os.path.exists(filename) and os.path.isfile(filename):
                return filename

        base, ext = os.path.splitext(image_file)
        filename = "%s%s.json" % (base, ext)
        if os.path.exists(filename) and os.path.isfile(filename):
            return filename
        else:
            return None
