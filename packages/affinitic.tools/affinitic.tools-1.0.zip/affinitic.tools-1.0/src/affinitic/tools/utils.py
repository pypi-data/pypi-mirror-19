# -*- coding: utf-8 -*-
"""
affinitic.tools
---------------

Created by mpeeters
:copyright: (c) 2016 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import pkg_resources


def run_entry_points(group, *args, **kwargs):
    for entrypoint in pkg_resources.iter_entry_points(group=group):
        plugin = entrypoint.load()
        plugin(*args, **kwargs)
