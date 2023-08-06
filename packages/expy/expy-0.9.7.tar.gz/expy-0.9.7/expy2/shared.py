# coding:utf-8
import os
import ctypes
import serial
import time

import pyglet
from pyglet import gl
import pyglet.window.key as key_

import librosa
import pyaudio
import numpy as np
import math

'''
Some variable that will be used in many place.
'''

'environment varibles'
path = os.path.dirname(os.path.abspath(__file__)) + '/'

win_width = 0
win_height = 0

win = None
need_update = False

'event varibles'
events = []

allowed_keys = []
allowed_keys_mapping = dict()

allowed_mouse_events = [] # {'x':range(), 'y':range(), 'button':..}

suspending = False

start_tp = 0

# import threading
# from .watchdog import *
# watchdog_lock = threading.Lock()
# watchdog = threading.Thread(target=wait)

'Sound'

# try:
#     from pyglet.media.drivers.openal import lib_openal as al
#     from pyglet.media.drivers.openal import lib_alc as alc
# except:
#     print('OpenAL not installed')
#     has_openal = False
# else:
#     has_openal = True


'experiment varibles'
subject = ''
start_block = 1

font = dict()
background_color = None
font_color = None

setting = dict()
timing = dict()

# init
try:
    port_dll = ctypes.windll.LoadLibrary(path + "inpoutx64.dll")
except:
    port_dll = ctypes.windll.LoadLibrary(path + "inpout32.dll")

ser = serial.Serial(baudrate=115200)



