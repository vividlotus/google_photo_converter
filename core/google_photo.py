# -*- coding: utf-8 -*-
import piexif
import shutil
import os

from .image_with_json import ImageWithJson
from .json_data import JsonData



class GooglePhoto:
    def __init__(self, export_path: str, target: ImageWithJson) -> None:
        self.export_path = export_path
        self.target = target
        self._json = JsonData(target.json_file)
        self._exif = piexif.load(target.image_file)
        # for ifd in ("0th", "Exif", "GPS", "1st"):
        #     for tag in self._exif[ifd]:
        #         print("File: %s, ifd: %4s, tag: %6s, tagName: %30s, Data: %s" % (target.image_file, ifd, tag, piexif.TAGS[ifd][tag]["name"], self._exif[ifd][tag]))


    def convert(self) -> bool:
        """
        変換処理
        """
        if self._is_already_exists_photo_taken_time():
            return True

        if not self._apply_photo_taken_time():
            return False

        # Exifの変更反映
        piexif.insert(piexif.dump(self._exif), self.target.image_file)

        return True


    def move(self):
        """
        移動
        """
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)

        shutil.move(self.target.image_file, self.export_path + os.path.basename(self.target.image_file))
        shutil.move(self.target.json_file, self.export_path + os.path.basename(self.target.json_file))


    def _is_already_exists_photo_taken_time(self) -> bool:
        return self._exif['0th'].get(piexif.ImageIFD.DateTime) != None \
            and self._exif['Exif'].get(piexif.ExifIFD.DateTimeOriginal) != None \
            and self._exif['Exif'].get(piexif.ExifIFD.DateTimeDigitized) != None


    def _apply_photo_taken_time(self) -> bool:
        """
        撮影日時を反映
        """
        photo_taken_time = self._json.photo_taken_time()
        if photo_taken_time is None:
            return False

        self._exif['0th'][piexif.ImageIFD.DateTime] = photo_taken_time.strftime('%Y:%m:%d %H:%M:%S')
        self._exif['Exif'][piexif.ExifIFD.DateTimeOriginal] = photo_taken_time.strftime('%Y:%m:%d %H:%M:%S')
        self._exif['Exif'][piexif.ExifIFD.DateTimeDigitized] = photo_taken_time.strftime('%Y:%m:%d %H:%M:%S')

        return True
