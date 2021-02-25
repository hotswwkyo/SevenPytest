# -*- coding:utf-8 -*-
"""

"""

from .marker import AttributeMarker
from sevenautotest.exceptions import ConstAttributeException

__version__ = "1.0"
__author__ = "si wen wei"


class AttributeMetaclass(type):

    _CLASS_ATTRIBUTES = "_CLASS_ATTRIBUTES"  # 禁止修改的类属性和类实例属性名

    def __new__(cls, name, bases, attrs):

        attributes = dict()

        for base in bases:
            if hasattr(base, cls._CLASS_ATTRIBUTES):
                attributes.update(base._CLASS_ATTRIBUTES)

        for attribute, value in attrs.items():
            if isinstance(value, AttributeMarker):
                attributes[attribute] = value

        for attribute in attributes.keys():
            if attribute in attrs.keys():
                # attrs.pop(attribute)
                attrs[attribute] = attributes[attribute].value
        attrs[cls._CLASS_ATTRIBUTES] = attributes

        return type.__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):

        return type.__init__(cls, name, bases, attrs)

    def __setattr__(cls, name, value):

        if name in cls.const_attrs.keys():
            raise ConstAttributeException("Unable to modify constant attribute(%s)" % name)
        type.__setattr__(cls, name, value)

    @property
    def const_attrs(cls):
        """禁止修改的属性"""

        attrs = {}
        for attr, marker in cls._CLASS_ATTRIBUTES.items():

            if marker.final:
                attrs[attr] = marker
        return attrs

    def get_attribute_marker(cls, attribute_name):

        if attribute_name in cls.const_attrs.keys():
            return cls.const_attrs[attribute_name]
        else:
            raise ConstAttributeException("'%s' class has no attribute '%s'" % (cls.__name__, attribute_name))


class AttributeManager(object, metaclass=AttributeMetaclass):
    def __setattr__(self, name, value):

        if name in self.__class__.const_attrs.keys():
            raise ConstAttributeException("Unable to modify constant attribute(%s)" % name)
        object.__setattr__(self, name, value)

    def get_attr_marker(self, attribute_name):

        return self.__class__.get_attribute_marker(attribute_name)
