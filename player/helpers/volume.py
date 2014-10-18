# -*- coding: utf-8 -*-

from amoki_music.settings import PROJECT_ROOT
import platform
import os


def increase():
    if platform.system() == "Windows":
        print(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume 4000')
        os.system(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume 4000')


def decrease():
    if platform.system() == "Windows":
        print(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume -4000')
        os.system(PROJECT_ROOT + '\\utils\\nircmd.exe changesysvolume -4000')
