import logging
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')


delay = 20
button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            clicked = 0
            while self.running:
                mouse.click(self.button)
                clicked += 1
                logging.info('Clicked %d time(s)' % clicked)
                time.sleep(self.delay)
            time.sleep(0.1)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            logging.info('Stopping')
            click_thread.stop_clicking()
        else:
            logging.info('Starting')
            click_thread.start_clicking()
    elif key == exit_key:
        logging.info('Exiting')
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
