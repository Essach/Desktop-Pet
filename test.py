import win32gui

hwnd = win32gui.GetForegroundWindow()

left, top, right, bottom = win32gui.GetClientRect(hwnd)
x, y = win32gui.ClientToScreen(hwnd, (right, 0))

print(x, y)