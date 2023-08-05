#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/12
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import os, sys, setuptools
from setuptools import setup, find_packages

# require python 2.7+
if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts, **kw):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return kw.get('default', '')

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.5.3',
  'fso                  >= 0.3.1',
]

dependencies = [
  'asset                >= 0.6.10',
  'six                  >= 1.6.0',
  'morph                >= 0.1.2',
]

entrypoints = {
  ## TODO: use `asset.find_plugins` when it exists...
  'jstc.engines.plugins' : [
    'text/x-handlebars  = jstc.engines.handlebars:HandlebarsEngine',
    'text/x-mustache    = jstc.engines.mustache:MustacheEngine',
  ],
}

classifiers = [
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Operating System :: OS Independent',
  'Topic :: Internet',
  'Topic :: Software Development',
  'Topic :: Internet :: WWW/HTTP',
  'Natural Language :: English',
  'License :: OSI Approved :: MIT License',
  'License :: Public Domain',
]

setup(
  name                  = 'jstc',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = 'Server-side JavaScript template compilation and packaging',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'Philip J Grabner, Canary Health Inc',
  author_email          = 'oss@canary.md',
  url                   = 'http://github.com/canaryhealth/jstc',
  keywords              = 'javascript server-side template compiler packager',
  packages              = find_packages(),
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'jstc',
  entry_points          = entrypoints,
  license               = 'MIT (http://opensource.org/licenses/MIT)',
)

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
