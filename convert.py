# -*- coding: utf-8 -*-
import sys
import os

from core.finder import Finder
from core.google_photo import GooglePhoto



target_path = sys.argv[1]
print("target_path: %s" % target_path)

is_valid = True
if len(target_path) == 0:
    is_valid = False
    print("arg1(target_path) is required.")

if not os.path.exists(target_path):
    is_valid = False
    print("Does not exist dir: %s" % target_path)

if not is_valid:
    sys.exit()

finder = Finder(target_path, ['jpg', 'jpeg'])
files = finder.get_files()
export_base_path = os.path.dirname(os.path.abspath(target_path))
for file in files:
    export_path = "%s/converted/%s/" % (export_base_path, os.path.basename(os.path.dirname(file.image_file)))
    gp = GooglePhoto(export_path, file)
    if gp.convert():
        gp.move()

print("Complete!")
