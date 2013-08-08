import ctypes

WM_GETTEXTLENGTH = 14 # c_int
SMTO_ABORTIFHUNG = 2 # c_int
WM_GETTEXT = 13 # c_int

topOnly = True
windows = []

if not topOnly:
    desktop_handle = ctypes.windll.user32.GetDesktopWindow()
    print(desktop_handle.__class__)
    if not desktop_handle is int:
        print ('wow')

    '''messege box hello world
    ctypes.windll.user32.MessageBoxW(0, "msun", "Hello World", 0)
    '''

    def enum_child_windows(handle):
        '''Find the child windows for this handle'''

        child_windows = []

        def EnumChildProc(hwnd, lparam):
            child_windows.append(hwnd)
            return True

        enum_child_proc = ctypes.WINFUNCTYPE(
            ctypes.c_int,    # return type
            ctypes.c_long,   # window handle
            ctypes.c_long,)  # extra information

        proc = enum_child_proc(EnumChildProc)
        ctypes.windll.user32.EnumChildWindows(handle, proc, 0)

        return child_windows

    windows = enum_child_windows(desktop_handle)
else:
    def EnumWindowProc(hwnd, lparam):
        windows.append(hwnd)
        return True

    enum_win_proc = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_long, ctypes.c_long)

    proc = enum_win_proc(EnumWindowProc)
    ctypes.windll.user32.EnumWindows(proc, 0)
    
print(len(windows))

title = 'NI Execution Adapter for IBM Rational Quality Manager'

def handle_text(handle):
    '''Return the text of the handle.'''

    length = ctypes.c_long()
    ctypes.windll.user32.SendMessageTimeoutW(
        handle,
        WM_GETTEXTLENGTH,
        0,
        0,
        SMTO_ABORTIFHUNG,
        100,
        ctypes.byref(length))

    length = length.value

    textval = ''
    if length:
        length += 1

        buffer_ = ctypes.create_unicode_buffer(length)

        ret = ctypes.windll.user32.SendMessageW(
            handle,
            WM_GETTEXT,
            length,
            ctypes.byref(buffer_))

        if ret:
            textval = buffer_.value

        return textval

##for win in windows:
##    print(handle_text(win))

windows = [win for win in windows if handle_text(win) == title]
window = windows[0]
print(window)
print(handle_text(window))
ctypes.windll.user32.SwitchToThisWindow(window, True)
ctypes.windll.user32.SetFocus(window)
