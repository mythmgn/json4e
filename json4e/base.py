#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright - See LICENSE for details
# Authors: Guannan Ma @mythmgn
"""
:description:
    base description of echarts
"""

import abc

SUPPORTED_POS = ['top', 'bottom', 'left', 'right']


def _check_valid(item, checklist):
    """
    check if the item is valid
    """
    if item not in checklist:
        raise TypeError('{0} is NOT in support list ({1})'.format(
            item, checklist)
        )


class JsonRender(object):
    """
    json render for echarts
    """
    __metaclass__ = abc.ABCMeta
    _DEFAULT_POS = ['top', 'bottom', 'left', 'right']

    @abc.abstractproperty
    def json(self):
        """return json of the object"""


class Series(JsonRender):
    """
    series for echarts, reference:https://echarts.baidu.com/option.html#series
    """
    DEFAULT_TYPES = [
        'line', 'bar', 'pie', 'scatter', 'effectScatter', 'radar',
        'tree', 'treemap', 'sunburst', 'boxplot', 'candlestick',
        'heatmap', 'map', 'parallel', 'lines', 'graph', 'sankey',
        'funnel', 'gauge', 'pictorialBar', 'themeRiver', 'custom'
    ]

    def __init__(self, assigned_type, name, data=None, **kwargs):
        """
        init

        :param assigned_type:
            should be one of Series.DEFAULT_TYPES

        :raise TypeError:
            raise TypeError if assigned_type not supported,
            see https://echarts.baidu.com/option.html#series for details
        """
        _check_valid(assigned_type, self.DEFAULT_TYPES)
        self._type = assigned_type
        self._name = name
        self._data = data
        self._optional_args = kwargs

    @property
    def json(self):
        """json dict of series"""
        jsondict = {
            'name': self._name,
            'data': self._data,
            'type': self._type,
        }
        if self._optional_args is not None:
            jsondict.update(self._optional_args)
        return jsondict


class Line(Series):
    """
    line of echarts
    """
    def __init__(self, name, data, **kwargs):
        """
        :param data:
            could be None for empty
        """
        Series.__init__(self, 'line', name, data, **kwargs)


class Axis(JsonRender):
    """
    axis in echarts
    """
    SUPPORTED_TYPE = ['category', 'value', 'time', 'log']

    def __init__(self, assigned_type, name, pos, data=None, **kwargs):
        """
        axis

        :param assigned_type:
            should be one of 'category', 'value', 'time', 'log'
        """
        _check_valid(assigned_type, self.SUPPORTED_TYPE)
        self._atype = assigned_type
        self._pos = pos
        self._name = name
        self._data = data
        self._optional_args = kwargs

    def position(self):
        """
        return position
        """
        return self._pos

    def x_axis(self):
        """if it's xais"""
        if self._pos in ('bottom', 'top'):
            return True
        else:
            return False

    def y_axis(self):
        """
        return if it's y xais
        """
        return not self.x_axis()

    @property
    def json(self):
        """
        return json of the axis
        """
        jsondict = {
            'name': self._name,
            'type': self._atype,
            'data': self._data,
            'position': self._pos
        }
        if self._optional_args is not None:
            jsondict.update(self._optional_args)
        return jsondict


class Legend(JsonRender):
    """Legend of Echart."""
    SUPPORTED_TYPE = ['plain', 'scroll']
    SUPPORTED_ORIENT = ['horizontal', 'vertical']

    def __init__(self,
            position, data, assigned_type='plain',
            orient='horizontal', **kwargs
        ):
        """

        :param position:
            a tuple like (1, 2)
        :param assigned_type:
            'plain' or 'scroll'
        :raise Exception:
            TypeError if orient is neither 'horizontal' nor 'vertical'
        """
        self._data = data
        _check_valid(orient, self.SUPPORTED_ORIENT)
        self._orient = orient
        self._type = assigned_type
        self._pos = position
        self._optional_args = kwargs

    @property
    def json(self):
        """JSON format data."""
        jsondict = {
            'orient': self._orient,
            'data': self._data,
            'x': self._pos[0],
            'y': self._pos[1],
            'type': self._type
        }
        if self._optional_args is not None:
            jsondict.update(self._optional_args)
        return jsondict


class Tooltip(JsonRender):
    """A tooltip when hovering."""
    TRIGGERS = ['axis', 'item']
    AXISPOINTER_TYPES = ['line', 'shadow', 'none', 'cross']

    def __init__(self, trigger='axis', axis_pointer_type='line', **kwargs):
        """
        :param trigger:
            one of Tooltip.TRIGGERS
            (https://echarts.baidu.com/option.html#tooltip.axisPointer.type)
        """
        _check_valid(trigger, self.TRIGGERS)
        self._trigger = trigger
        self._axis_pointertype = axis_pointer_type
        self._optional_args = kwargs

    @property
    def json(self):
        """JSON format data."""
        jsondict = {
            'trigger': self._trigger,
            'axisPointer': {
                'type': self._axis_pointertype
            }
        }
        if self._optional_args is not None:
            jsondict.update(self._optional_args)
        return jsondict


class Bar(Series):
    "Bar of echarts"
    def __init__(self, name=None, data=None, **kwargs):
        Series.__init__(self, 'bar', name=name, data=data, **kwargs)


class Chart(JsonRender):
    """
    echarts object
    """
    SUPPORTED_COMPONENT = [
        Axis, Series
    ]

    def __init__(self, text, subtext, axis_enabled, animation=True, **kwargs):
        """
        init chart

        :param title:
            title of the Chart

        :param subtext:
            sub-title of the chart

        :param axis:
            True or False
        """
        self._text = text
        self._subtext = subtext
        self._axis_enabled = axis_enabled
        self._animation = animation
        if self._axis_enabled:
            self._x_axis = []
            self._y_axis = []
        self._series = []
        self._optional_args = kwargs
        self._components = {
            'legend': None,
            'tooltip': None,
            'series': None,
            'toolbox': None,
            'visualMap': None
        }

    def add_component(self, component):
        """
        :raise exception:
            if component can NOT be recoginized
        """
        if isinstance(component, Series):
            self._components['series'] = component
        elif isinstance(component, Legend):
            self._components['legend'] = component
        elif isinstance(component, Tooltip):
            self._components['tooltip'] = component
        elif isinstance(component, Axis):
            if component.x_axis():
                self._x_axis.append(component)
            else:
                self._y_axis.append(component)
        else:
            raise TypeError('does not have this component')

    @property
    def json(self):
        """
        return json of chart
        """
        jsondict = {
            'title': {
                'text': self._text,
                'subtext': self._subtext
            },
            'animation': self._animation
        }
        for key, value in self._components.items():
            if value is not None:
                jsondict[key] = value.json
        if self._axis_enabled:
            jsondict['xAxis'] = [item.json for item in self._x_axis] or [{}]
            jsondict['yAxis'] = [item.json for item in self._y_axis] or [{}]
        jsondict.update(self._optional_args)
        return jsondict

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
