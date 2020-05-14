class Screen:

    def __init__(self, window_name, change_area=5):
        self.sct = mss.mss()

        # see if csgo is open
        self.hwnd = win32gui.FindWindow(None, window_name)
        if self.hwnd == 0:
            exit("please open CSGO")

        # get csgo window size
        rect = win32gui.GetClientRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        
        # get center of screen
        self.region = {
            'top': int(y + h/2) - int(change_area/2),
            'left': int(x + w/2) - int(change_area/2),
            'width': change_area,
            'height': change_area
        }


    def grab(self):
        ''' take a screenshot '''
        return self.sct.grab(self.region)