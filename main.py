import win32api, win32gui, win32con
import mss, cv2
import time
import sys
from PIL import Image, ImageChops
from pynput.keyboard import Key, Listener, KeyCode

import mouse, screen


class Shooter:

    def __init__(self):
        self.window_name = "Counter-Strike: Global Offensive"
        self.screen = Screen(self.window_name)

        self.last_frame = None
        self.last_click = time.time()
        self.click_limit = 3
        self.active = False

         # check for toggle button
        listener = Listener(on_press=self.on_press)
        listener.start()

        while True:

            if self.active:
                
                # window in focus
                if self.is_playing(self.window_name):
                    sct_img = self.screen.grab()
                    img = self.process_image(sct_img)

                    # no reference frame, skip
                    if self.last_frame == None:
                        self.last_frame = img
                        continue
                    
                    # difference
                    if self.is_difference(img, self.last_frame):
                        self.log('yes')
                        if self.can_click():
                            Mouse.click()
                        self.last_frame = img

                    # no difference
                    else:
                        self.log('no ')
                
                # window out of focus
                else:
                    self.active = False
            
            else:
                self.log('no') # update active on screen

    def is_playing(self, csgo_window_name):
        ''' check if user has focus on game window '''
        current_window = win32gui.GetWindowText(
            win32gui.GetForegroundWindow()
        )
        return current_window == csgo_window_name

    def is_difference(self, image1, image2):
        ''' detect changes in frames '''
        diff = ImageChops.difference(image1, image2)
        return diff.getbbox()

    def process_image(self, sct_img):
        ''' covert image to grayscale '''
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img.convert('LA')
        return img

    def on_press(self, key):
        ''' handle keypress for toggle bind '''
        if key == KeyCode.from_char('k'):
            self.active = not self.active
            self.log("n\\a")

    def can_click(self):
        ''' has the click delay expired? '''
        now = time.time()
        clickable = (now - self.last_click) > self.click_limit
        self.last_click = now
        return clickable

    def log(self, is_difference):
        ''' display nicely what is happening '''
        print("\r[-] Active: {} | Difference: {}".format(
            self.active, is_difference
        ), end="")
        sys.stdout.flush()


if __name__ == "__main__":
    print('Pixel Trigger for CSGO')
    print('(press k to active)\n')
    s = Shooter()
