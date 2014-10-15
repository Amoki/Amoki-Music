# -*- coding: utf-8 -*-

from amoki_music.settings import PROJECT_ROOT
import platform
import os


def increase_volume():
    if platform.system() == "Windows":
        print(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume 4000')
        os.system(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume 4000')


def decrease_volume():
    if platform.system() == "Windows":
        print(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume -4000')
        os.system(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume -4000')
