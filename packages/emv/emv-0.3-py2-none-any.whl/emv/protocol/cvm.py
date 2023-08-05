# coding=utf-8
from __future__ import division, absolute_import, print_function, unicode_literals


class CVMList(object):

    @classmethod
    def unmarshal(self, data):
        assert len(data) > 8

