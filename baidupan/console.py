# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import context
from baidupan.command import manager
import readline
import traceback

__all__ = ['run']

def _completer(prefix, index):
    # 获取当前行
    line = readline.get_line_buffer()
    cmd, args = manager.parse_input(line)
    words = []
    if cmd is None:
        # 自动提示命令
        words = manager.get_command_names()
        words = map(lambda x:'%s ' % x, words)
        words = filter(lambda x:x.startswith(prefix), words)
    else:
        # 自动提示参数
        words = cmd.get_completer_words(args)
    return words[index] if words and index < len(words) else None

class _Console():
    def __init__(self):
        # 绑定readline
        readline.parse_and_bind('tab: complete')
        readline.set_completer(_completer)
    def run(self):
        while context.alive:
            prompt = 'BaiduPan:%s> ' % context.get_rwd()
            # 获取输入
            line = raw_input(prompt).strip()
            # 跳过空行
            if len(line) == 0: continue
            # 解析命令和参数
            cmd, args = manager.parse_input(line)
            if cmd is None:
                print 'No such command'
                continue
            if cmd.need_login and not context.client.is_login:
                print 'You MUST login before use %s' % cmd.name
                continue
            # 执行命令
            try:
                cmd.execute(args)
            except:
                traceback.print_exc()
        # 流程结束时保存cookie
        context.cookie_jar.save()

def run():
    _Console().run()