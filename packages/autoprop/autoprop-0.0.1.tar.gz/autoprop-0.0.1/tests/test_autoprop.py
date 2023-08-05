#!/usr/bin/env python

import pytest
import autoprop

def test_accessors():
    @autoprop   # (no fold)
    class Example(object):
        def get_attr(self):
            return 'attr'

    ex = Example()
    assert ex.attr == 'attr'

    @autoprop   # (no fold)
    class Example(object):
        def set_attr(self, attr):
            self._attr = 'new ' + attr

    ex = Example()
    ex.attr = 'attr'
    assert ex._attr == 'new attr'

    @autoprop   # (no fold)
    class Example(object):
        def del_attr(self):
            self._attr = None

    ex = Example()
    del ex.attr
    assert ex._attr is None

    @autoprop   # (no fold)
    class Example(object):
        def get_attr(self):
            return self._attr
        def set_attr(self, attr):
            self._attr = 'new ' + attr

    ex = Example()
    ex.attr = 'attr'
    assert ex.attr == 'new attr'

    @autoprop   # (no fold)
    class Example(object):
        def get_attr(self):
            return self._attr
        def set_attr(self, attr):
            self._attr = 'new ' + attr
        def del_attr(self):
            self._attr = None

    ex = Example()
    ex.attr = 'attr'
    assert ex.attr == 'new attr'
    del ex.attr
    assert ex.attr is None

def test_ignore_similar_names():
    @autoprop   # (no fold)
    class Example(object):
        def getattr(self):
            return 'attr'

    ex = Example()
    with pytest.raises(AttributeError):
        ex.attr

def test_ignore_empty_names():
    @autoprop   # (no fold)
    class Example(object):
        def get_(self):
            return 'get'

    ex = Example()
    with pytest.raises(AttributeError):
        getattr(ex, '')

def test_ignore_non_methods():
    @autoprop   # (no fold)
    class Example(object):
        get_attr = 'attr'

    ex = Example()
    with pytest.raises(AttributeError):
        ex.attr

def test_inheritance():
    @autoprop   # (no fold)
    class Parent(object):
        def get_attr(self):
            return 'parent'
        def get_overloaded_attr(self):
            return 'parent'

    @autoprop   # (no fold)
    class Child(Parent):
        def get_overloaded_attr(self):
            return 'child'

    parent = Parent()
    child = Child()

    assert parent.attr == 'parent'
    assert parent.overloaded_attr == 'parent'
    assert child.attr == 'parent'
    assert child.overloaded_attr == 'child'

def test_dont_overwrite_existing_attributes():
    @autoprop   # (no fold)
    class Example(object):
        attr = 'class var'
        def get_attr(self):
            return 'attr'

    ex = Example()
    assert ex.attr == 'class var'

def test_optional_arguments():
    @autoprop   # (no fold)
    class Example(object):
        def get_attr(self, pos=None, *args, **kwargs):
            return self._attr
        def set_attr(self, new_value, pos=None, *args, **kwargs):
            print('asdasd')
            self._attr = 'new ' + new_value
        def del_attr(self, pos=None, *args, **kwargs):
            self._attr = None

    ex = Example()
    ex.attr = 'attr'
    assert ex.attr == 'new attr'
    del ex.attr
    assert ex.attr == None

def test_getters_need_one_argument():
    @autoprop   # (no fold)
    class Example(object):
        def get_attr():
            return 'attr'

    ex = Example()
    with pytest.raises(AttributeError):
        ex.attr

    @autoprop   # (no fold)
    class Example(object):
        def get_attr(self, more_info):
            return 'attr'

    ex = Example()
    with pytest.raises(AttributeError):
        ex.attr

def test_setters_need_two_arguments():
    @autoprop   # (no fold)
    class Example(object):
        def set_attr(self):
            self._attr = 'no args'

    ex = Example()
    ex.attr = 'attr'
    with pytest.raises(AttributeError):
        assert ex._attr != 'no args'

    @autoprop   # (no fold)
    class Example(object):
        def set_attr(self, new_value, more_info):
            self._attr = 'two args'

    ex = Example()
    ex.attr = 'attr'
    with pytest.raises(AttributeError):
        assert ex._attr != 'two args'

def test_deleters_need_one_argument():
    @autoprop   # (no fold)
    class Example(object):
        def del_attr():
            pass

    ex = Example()
    with pytest.raises(AttributeError):
        del ex.attr

    @autoprop   # (no fold)
    class Example(object):
        def del_attr(self, more_info):
            pass

    ex = Example()
    with pytest.raises(AttributeError):
        del ex.attr


import sys
if sys.version_info[0] == 2:

    def test_complain_about_old_style_classes():
        with pytest.raises(TypeError) as err:
            @autoprop
            class Example:
                pass

        assert '@autoprop can only be used with new-style classes' in str(err)
