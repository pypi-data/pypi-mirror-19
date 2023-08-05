#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   data.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''


class DataInexistence(object):
    pass


def extract(data, path, quire=True, default=DataInexistence):
    if isinstance(path, basestring):
        path = path.split('.')

    for index in path:
        try:
            data = data[index]
        except:
            if quire:
                return default

            raise

    return data


def ensure_inexistence(data, pathes):
    for path in pathes:
        assert extract(data=data, path=path) is DataInexistence
