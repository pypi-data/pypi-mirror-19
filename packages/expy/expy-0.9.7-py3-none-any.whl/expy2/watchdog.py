from pygame.locals import *
import time
from expy import shared

# import pyglet
# from pyglet.window import mouse,key

# window = pyglet.window.Window()

# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == mouse.LEFT:
#         print( 'The left mouse button was pressed.')

# @window.event
# def on_key_press(k, modifiers):
#     'decision'
#     if k == key_.ESC:
#         pg.quit()
#     elif k == key_.F12 and not suspending:
#         suspend_time = suspend()
#         start_tp += suspend_time
#     elif not watchdog_key:  # if allowed_key_. is None
#         watchdog_time = time.time()
#         watchdog_event = k
#         watchdog_has_event = True
#     elif k in watchdog_key:  # if k is in the allowed Keyname(s)
#         watchdog_time = time.time()
#         watchdog_event = watchdog_mapping[k]
#         watchdog_has_event = True

# def wait():
#     shared.pg.event.clear()
#     while True:
#         if not shared.threading.main_thread().is_alive():
#             return

#         now = time.time()

#         if shared.watchdog_out_time > 0 and now >= shared.watchdog_out_time:
#             shared.watchdog_time = now
#             shared.watchdog_event = 'out'
#             shared.watchdog_has_event = True

#         time.sleep(0.1)

def wait():
    shared.pg.event.clear()
    while True:
        if not shared.threading.main_thread().is_alive():
            return

        now = time.time()

        if shared.watchdog_out_time > 0 and now >= shared.watchdog_out_time:
            shared.watchdog_time = now
            shared.watchdog_event = 'out'
            shared.watchdog_has_event = True


        for e in shared.pg.event.get():
            # print(e)
            'get the pressed key'
            if e.type == KEYDOWN:
                print('KEYDOWN')
                k = e.key
            elif e.type == JOYBUTTONDOWN:
                k = e.button
            elif e.type == MOUSEBUTTONDOWN:  # e.type == MOUSEMOTION, k = e.pos
                print('MOUSEBUTTONDOWN')
                k = e.button
            else:
                continue

            'decision'
            if k == 27:
                shared.pg.quit()
                return
            elif k == key_.F12 and not suspending:
                suspend_time = suspend()
                start_tp += suspend_time
            elif not shared.watchdog_key:  # if allowed_keys is None
                shared.watchdog_time = now
                shared.watchdog_event = k
                shared.watchdog_has_event = True
            elif k in shared.watchdog_key:  # if k is in the allowed Keyname(s)
                shared.watchdog_time = now
                shared.watchdog_event = shared.watchdog_mapping[k]
                shared.watchdog_has_event = True

        time.sleep(0.1)
