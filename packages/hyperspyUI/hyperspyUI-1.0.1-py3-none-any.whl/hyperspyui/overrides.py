# -*- coding: utf-8 -*-
# Copyright 2014-2016 The HyperSpyUI developers
#
# This file is part of HyperSpyUI.
#
# HyperSpyUI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpyUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperSpyUI.  If not, see <http://www.gnu.org/licenses/>.
"""
Created on Fri Dec 19 03:43:51 2014

@author: Vidar Tonaas Fauske
"""


from python_qt_binding import QtCore
import hyperspy.drawing.utils

orig_on_figure_window_close = hyperspy.drawing.utils.on_figure_window_close


def _on_figure_window_close(figure, function):
    """Connects a close figure signal to a given function.

    Parameters
    ----------

    figure : mpl figure instance
    function : function

    """
    window = figure.canvas.manager.window
    if not hasattr(figure, '_on_window_close'):
        figure._on_window_close = list()
    if function not in figure._on_window_close:
        figure._on_window_close.append(function)

    # PyQt
    # In PyQt window.connect supports multiple funtions
    window.connect(window, QtCore.SIGNAL('closing()'), function)


def override_hyperspy():
    hyperspy.drawing.utils.on_figure_window_close = _on_figure_window_close
