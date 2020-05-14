class Mouse:

    @staticmethod
    def click(pos=None):
        if not pos:
            pos = Mouse.get_pos()

        x,y = pos

        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    @staticmethod
    def get_pos():
        flags, hcursor, (x,y) = win32gui.GetCursorInfo()
        return (x,y)