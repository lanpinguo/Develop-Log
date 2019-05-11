#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:         Andrew Xu

# CreateDate: 2012/12/18
#自动化测试和python群组： http://groups.google.com/group/automation_testing_python

#参考资料：

# 实验环境：Python2.6.6 CentOS release 6.2 (Final) 32bits
'''
         最近公司准备自动化Spirent TestCenter仪表。Spirent的技术支持说有python的Api提供，价钱需要2万元人民币，还爱买不买的样子。看了一下他们的外围代码，居然是用swig从C API中转过来的。执行起来效率低下，bug层出不穷。遂对之彻底失去信心。改为用python的Tkinter直接调用TCL. 代码如下：
'''

import Tkinter

 

def build_cmd(*args):

    cmd = ''

    for arg in args:

        cmd = cmd + arg + ' '

    return cmd

 

class Stc(object):

    def __init__(self):

        self.tclsh =Tkinter.Tcl()

       self.tclsh.eval("package require SpirentTestCenter")

 

    def stc_init(self, *args):

        cmd =build_cmd('stc::init', *args)

        returnself.tclsh.eval(cmd)

 

    def stc_connect(self,*args):

        cmd =build_cmd('stc::disconnect', *args)

        returnself.tclsh.eval(cmd)

 

 

    def stc_connect(self,*args):

        cmd =build_cmd('stc::connect', *args)

        returnself.tclsh.eval('stc::connect')

 

 

    def stc_disconnect(self,*args):

        cmd =build_cmd('stc::disconnect', *args)

        returnself.tclsh.eval(cmd)

 

 

    def stc_create(self,*args):

        cmd =build_cmd('stc::create', *args)

        returnself.tclsh.eval(delete)

 

 

    def stc_delete(self,*args):

        cmd =build_cmd('stc::delete', *args)

        returnself.tclsh.eval(cmd)

 

 

    def stc_config(self,*args):

        cmd =build_cmd('stc::config', *args)

        returnself.tclsh.eval(cmd)

 

 

    def stc_get(self, *args):

        cmd = build_cmd('stc::get', *args)

        returnself.tclsh.eval(cmd)

 

 

    def stc_perform(self,*args):

        cmd =build_cmd('stc::perform', *args)

        returnself.tclsh.eval(cmd)

 

 

    def stc_reserve(self,*args):

        cmd =build_cmd('stc::reserve', *args)

        returnself.tclsh.eval(cmd)

 

    def stc_release(self,*args):

        cmd =build_cmd('stc::release', *args)

        returnself.tclsh.eval(cmd)

 

 

    def stc_subscribe(self,*args):

        cmd = build_cmd('stc::subscribe',*args)

        returnself.tclsh.eval(cmd)

 

    def stc_unsubscribe(self,*args):

        cmd =build_cmd('stc::unsubscribe', *args)

        returnself.tclsh.eval(cmd)

 

    def stc_help(self, *args):

        cmd = build_cmd('stc::help',*args)

        returnself.tclsh.eval(cmd)