# -*- coding: utf-8 -*-
"""
█▀▀▄ █▀▀ ▀█░█▀ ▀▀█▀▀ █▀▀█ █▀▀█ █░░ █▀▀
█░░█ █▀▀ ░█▄█░ ░░█░░ █░░█ █░░█ █░░ ▀▀█
▀▀▀░ ▀▀▀ ░░▀░░ ░░▀░░ ▀▀▀▀ ▀▀▀▀ ▀▀▀ ▀▀▀                                            

These are my Developer tools to make life easier.
Distributed at GitHub under MIT license.
v. 0.3 from 20.05.2018
rrraposa @ github.com
"""
##########################################
# Monkeypatch for QT (OLE error 80070005)#
##########################################
import pythoncom
pythoncom.CoInitialize()

##########################################
# For JSONfile                           #
##########################################

from collections import defaultdict as dd
from copy import deepcopy
import json, time

##########################################
# For asyncronous threads                #
##########################################

from threading import Thread, Timer
from functools import wraps

##########################################
# Global DEBUG switch                    #
##########################################

DEBUG = True

##########################################
# Some useful functions                  #
##########################################


def cls():
    for _ in range(1024):
        print('\n\r')


##########################################
# Async decorator                        #
##########################################

# Not my code, it's taken from:
# https://gist.github.com/nubotz/34222531c4fb2f88cccf34c2cc812113


def do_async(func):
    """
    Example:
    @async
    def some_function(.....)
    """

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.daemon = False
        func_hl.start()
        return func_hl

    return async_func


##########################################
# Improved object to handle empty kwargs #
##########################################


class BetterObject(object):
    def __init__(self, **kwargs):
        self.kw = dd(lambda: None)
        self.kw.update(kwargs)
        print(kwargs)


##########################################
# JSON file as a dict on disk            #
##########################################


class JSONfile(BetterObject):
    def __init__(self, **kwargs):
        super(JSONfile, self).__init__(**kwargs)
        print('JSONfile: kwargs are: %s' % self.kw) if DEBUG else None
        self.data = dd(lambda: None)
        _ = self.kw['filename']
        self.autosave = self.kw['autosave']
        self.filename = 'dump.json' if not _ else _
        self.requests = 0
        print('JSONfile: filename is %s' % self.filename) if DEBUG else None
        self.load()
        self.clear = True

    def load(self):
        try:
            with open(self.filename, 'r') as jsonfile:
                _ = json.load(jsonfile)
                self.data.update(_)
        except:
            print('JSONfile: No file found') if DEBUG else None
            self.save()

    @do_async
    def save(self):
        self.clear = False
        self.requests += 1
        _ = deepcopy(self.requests)
        time.sleep(0.01)
        if _ == self.requests:
            print('Writing...')
            self.requests = 0
            with open(self.filename, 'w') as jsonfile:
                try:
                    json.dump(self.data, jsonfile)
                except:
                    pass
                    return False
            self.clear = True
            return True
        else:
            return False

    def clear(self):
        self.data = dd(lambda: None)
        self.save()

    def __call__(self):
        return self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save() if self.autosave else None

    def __del__(self):
        self.save()
        while not self.clear:
            time.sleep(0.0001)


if __name__ == '__main__':
    cls()
    print('Testing JSONfile...')
    jsondata = JSONfile(
        filename='test.json', autosave=True)  # or, jsondata.save()
    print(jsondata['test'])
    a = str(jsondata())
    print("jsondata['test']=%s" % a[0:100])
    jsondata['test'] = 'somevalue'
    jsondata['ones'] = '11111111'
    print(jsondata['test'])
    for save in (True, False):
        print('Autosave state is: %s' % save)
        jsondata.autosave = save
        for n in range(10000):
            jsondata[str(n)] = n
        jsondata.save() if save else None
    jsondata.clear()