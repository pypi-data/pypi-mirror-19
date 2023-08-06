# coding:utf-8
import os
import ctypes
import serial
import time
import threading

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
states = dict()

allowed_keys = []
allowed_keys_mapping = dict()

allowed_mouse_events = [] # {'x':range(), 'y':range(), 'button':..}

suspending = False

start_tp = 0

'Sound'

lock = threading.Lock()

def changeState(name, value):
    '''
    Change the value of a global state
    Parameters
    ----------
    name: anything
        The name of the target state
    value: anything
        The target value of the target state

    Return
    ---------
    None
    '''
    lock.acquire()
    try:
        states[name] = value
    finally:
        lock.release()
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

'sound'
pa = pyaudio.PyAudio()
sound_event = Queue()
sound_process = None

# init
try:
    port_dll = ctypes.windll.LoadLibrary(path + "inpoutx64.dll")
except:
    port_dll = ctypes.windll.LoadLibrary(path + "inpout32.dll")

ser = serial.Serial(baudrate=115200)



