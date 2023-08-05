#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('../'))


project = u'pykafka-tools'
copyright = u'2016, Stephan Müller'
author = u'Stephan Müller'

version = release = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
]

templates_path = ['_templates']
exclude_patterns = ['_build']
html_static_path = ['_static']

source_suffix = '.rst'
master_doc = 'index'

html_theme = 'sphinx_rtd_theme'
pygments_style = 'sphinx'
htmlhelp_basename = 'pykafka-tools'

autodoc_default_flags = ['special-members', 'private-members', 'show-inheritance']
