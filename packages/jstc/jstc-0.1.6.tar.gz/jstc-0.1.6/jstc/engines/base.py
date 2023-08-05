# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/12
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import re

#------------------------------------------------------------------------------
class Engine(object):

  mimetype              = None
  extensions            = None
  open_markers          = ('<',)
  close_markers         = ('>',)

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(Engine, self).__init__(*args, **kw)
    self._ws_cre = re.compile(
      '(?P<close>' + '|'.join([re.escape(m) for m in self.close_markers]) + ')'
      + '\\s*\n\\s*'
      + '(?P<open>' + '|'.join([re.escape(m) for m in self.open_markers]) + ')',
      flags = re.DOTALL)

  #----------------------------------------------------------------------------
  def whitespace(self, text, attrs):
    '''
    Remove "ignorable" whitespace from `text`. Note that `text` will
    already have been dedented and stripped.
    '''
    # todo: ok, this is a *SUPER* simple ignorable whitespace
    #       detection algorithm... this needs to be refactored
    #       somehow...
    #return text
    return self._ws_cre.sub('\\g<close>\\g<open>', text)

  #----------------------------------------------------------------------------
  def precompile(self, text, attrs):
    '''
    Pre-compiles the JavaScript template `text` for delivery to a
    JavaScript enabled client in a "pre-compiled"
    format. Pre-compilation means that the template character stream
    has been, at minimum, parsed into tokens and typically rendered
    into JavaScript native syntax in order to accelerate template
    parsing on the client via highly optimized JavaScript parsing
    code. If pre-compilation is not available (e.g. because the
    specified template type does not support pre-compilation or the
    necessary pre-requisites for pre-compilation are not available),
    then a `jstc.api.PrecompilerUnavailable` exception (or subclass)
    should be raised. The `attrs` specifies template attributes; see
    `jstc.compiler.Compiler.compile` for details.
    '''
    raise NotImplementedError()


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
