'''
hs_auto_open_packs.py
炉石自动开卡包工具
win10需要管理员权限运行
'''

import time
import os
import sys
import win32api
import win32con
import win32gui
import win32process

kProcessName = 'Hearthstone'  # 程序名
kSearchTime = 5  # 寻找顶级窗口时间


# 寻找标题为title,父窗口为parent_hWnd的顶级窗口的句柄
# parent_hWnd可以为None
# func为自定义判断函数,调用为func(hWnd, *args),可以为None
def find_window_handle(title, parent_hWnd, func, *args):
  target_hWnd = None
  hWnd_list = []
  clk = time.time()
  while True:
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    for hWnd in hWnd_list:
      if win32gui.GetWindowText(hWnd).find(title) != -1 \
          and (not parent_hWnd or win32gui.GetParent(hWnd) == parent_hWnd) \
          and (not func or func(hWnd, *args)):
        target_hWnd = hWnd
        break
    if target_hWnd or kSearchTime < time.time() - clk:
      break
    hWnd_list.clear()
  return target_hWnd


# 向类名为wnd_class,标题为wnd_text的子窗口发送消息
# msg为windows消息,msg为list是可以发送多条消息
def send_messages_to_child_window(parent_hWnd, wnd_class, wnd_text, msgs, wParams, lParams):
  child_hWnd = win32gui.FindWindowEx(parent_hWnd, None, wnd_class, None)
  while child_hWnd:
    if not wnd_text or win32gui.GetWindowText(child_hWnd).find(wnd_text) != -1:
      if type(msgs) is list:
        for msg, wParam, lParam in zip(msgs, wParams, lParams):
          win32gui.SendMessage(child_hWnd, msg, wParam, lParam)
      else:
        win32gui.SendMessage(child_hWnd, msgs, wParams, lParams)
      break
    child_hWnd = win32gui.FindWindowEx(parent_hWnd, child_hWnd, wnd_class, None)
  return child_hWnd


def wait_seconds(wait_time):
  time.sleep(wait_time)


def in_pid_list(hWnd, *args):
  pid_list = args[0]
  for pid in pid_list:
    if pid in win32process.GetWindowThreadProcessId(hWnd):
      return True
  return False


if __name__ == '__main__':
  task_list = os.popen('tasklist')
  pid_list = []
  for task in task_list:
    if task.find(kProcessName) != -1:
      pid_list.append(int(task[29:34]))
  if not pid_list:
    print('未能找到名为{0}的程序'.format(kProcessName))
    exit()

  main_hWnd = find_window_handle("炉石传说", None, in_pid_list, pid_list)
  if not main_hWnd:
    print('未能找到主窗口标题含有{0}的uTorrent程序'.format(kUTVersion))
    exit()

  while 1:
    win32gui.SendMessage(main_hWnd, win32con.WM_KEYDOWN, 0x20, 0x390001)
    win32gui.SendMessage(main_hWnd, win32con.WM_CHAR, 0x20, 0x390001)
    win32gui.SendMessage(main_hWnd, win32con.WM_KEYUP, 0x20, 0xc0390001)
    wait_seconds(0.5)
