# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"


class AttributeMarker(object):
    def __init__(self, value, final=False, description="", *expend_args, **expend_kwargs):

        self.value = value
        self.final = final
        self.description = description
        self.expend_args = expend_args
        self.expend_kwargs = expend_kwargs

    def __str__(self):

        return "{value} ------> {description}".format(value=self.value, description=self.description)


class ConstAttributeMarker(AttributeMarker):
    def __init__(self, value, description="", *expend_args, **expend_kwargs):

        AttributeMarker.__init__(self, value, True, description, *expend_args, **expend_kwargs)
