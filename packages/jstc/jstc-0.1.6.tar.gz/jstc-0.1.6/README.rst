============================
JavaScript Template Compiler
============================

The `jstc` Python package compiles and packages JavaScript templates
for delivery to browsers for client-side evaluation.

Currently, only `Handlebars`_ and `Mustache`_ template formats are
supported natively, however this is easily extended via jstc's plugin
mechanism.


Project
=======

* Homepage: https://github.com/canaryhealth/jstc
* Bugs: https://github.com/canaryhealth/jstc/issues


Installation
============

.. code:: bash

  # install jstc
  $ pip install jstc

Optionally, the handlebars pre-compiler can be installed to
pre-compile JavaScript templates for faster client-side rendering:

.. code:: bash

  # OPTIONAL: install handlebars pre-compiler
  $ npm install handlebars
  $ export PATH="`pwd`/node_modules/.bin:$PATH"


Usage
=====

The typical usage is to have something similar to the following in
your HTML generation template (here, using `Mako`_ syntax):

.. code:: mako

  <%! import jstc %>
  <div id="Templates" style="display:none">
    ${jstc.render_assets(
      'myapp:static/scripts/**.hbs', force_inline=True, force_precompile=False)|n}
  </div>


Example
=======

Given that the following files exist in the Python package `myapp`:

File ``static/templates/common/hello.hbs``::

  Hello, {{name}}!


File ``static/templates/common/inputs.hbs`` (with multiple templates)::

  ##! text

    <input type="text" name="{{name}}" value="{{value}}"/>

  ##! checkbox

    <input type="checkbox" name="{{name}}" value="1" {{#value}}checked="checked"{{/value}}/>


Then, the Python code (`inline` and `precompile` attributes used for
output simplicity):

.. code:: python

  import jstc
  jstc.render_assets(
    'myapp:static/templates/common/**.hbs', 'static/templates',
    force_inline=True, force_precompile=False)


Outputs the HTML (whitespace and newlines added for clarity):

.. code:: html

  <script type="text/x-handlebars" data-template-name="common/hello">
    Hello, {{name}}!
  </script>

  <script type="text/x-handlebars" data-template-name="common/inputs/text">
    <input type="text" name="{{name}}" value="{{value}}"/>
  </script>

  <script type="text/x-handlebars" data-template-name="common/inputs/checkbox">
    <input type="checkbox" name="{{name}}" value="1" {{#if value}}checked="checked"{{/if}}/>
  </script>


Template Attributes
===================

When multiple templates are defined in a file, each template can
specify, or override, a set of attributes after the template name. For
example:

.. code:: text

  ##! template1

    <span>The first template.</span>

  ##! template2; precompile; !inline; space: preserve

    <span>The second template.</span>

The above file creates two templates, one named "template1" with no
attribute overrides, and a second one named "template2" with three
attributes: "precompile" set to true, "inline" set to false, and
"space" set to "preserve".

The following attributes control how `jstc` processes each template
(all other attributes are passed through either to callbacks or to the
output):

* ``type``:

  The template engine type, normally extracted from the mime-type of
  the file (i.e. the filename's extension), can be overridden thus
  allowing multiple template types within a single file.

* ``space``:

  Controls whitespace handing in template content. The following
  values are supported:

  * ``preserve``:

    Leave all whitespace exactly as-is.

  * ``trim``:

    Remove leading and trailing whitespace.

  * ``dedent``:

    "Dedent" the template (i.e. remove all whitespace that prefixes
    every line in the template) and also apply the ``trim``
    transformation.

  * ``collapse`` (the default):

    This applies the ``dedent`` transformation and then removes
    "ignorable" whitespace. Note that what is considered "ignorable"
    is dependent on the ``type``, but all assume that HTML is the
    target output. For example, for a `Handlebars`_ template, the
    following content:

    .. code::

      {{#if value}}
        <b>
          {{value}}
        </b>
      {{else}}
        <i>default</i>
      {{/if}}

    will be collapsed to:

      {{#if value}}<b>{{value}}</b>{{else}}<i>default</i>{{/if}}

* ``precompile``:

  Flag to control server-side pre-compilation.

* ``collision``:

  See help(jstc.Compiler.compile).

  TODO: dynamically duplicate pydoc here.

* ``inline``:

  See help(jstc.Compiler.compile).

  TODO: dynamically duplicate pydoc here.

* ``protected``:

  See help(jstc.Compiler.compile).

  TODO: dynamically duplicate pydoc here.

* ``partial``:

  See help(jstc.Compiler.compile).

  TODO: dynamically duplicate pydoc here.

* ``pass-through``:

  See help(jstc.Compiler.compile).

  TODO: dynamically duplicate pydoc here.

* ``prefix-through``:

  See help(jstc.Compiler.compile).

  TODO: dynamically duplicate pydoc here.

* ``trim``:

  DEPRECATED; use ``space`` instead.


Some Assumptions
================

The `jstc` package makes the following assumptions that cannot be
easily changed:

* Template names use the forward slash ("/") hierarchical delimiter,
  e.g. ``components/widgets/textform`` would be a typical template
  name.


Adding Template Formats
=======================

Let us assume that you want to add support for a new templating
engine, with a mime-type of ``text/x-easytpl``, file extension
``.et``, without pre-compilation support, and all within the Python
package ``myapp``.

Create module ``myapp/easytpl.py``:

.. code:: python

  import jstc
  import asset

  @asset.plugin('jstc.engines.plugins', 'text/x-easytpl')
  class EasyTemplateEngine(jstc.engines.base.Engine):
    mimetype    = 'text/x-handlebars'
    extensions  = ('.et',)
    precompile  = jstc.PrecompilerUnavailable


And then in your myapp's ``setup.py``, add the following parameter
to your `setup` call:

.. code:: python

  setup(
    ...
    entry_points = {
      'jstc.engines.plugins' : [
        'text/x-easytpl = myapp.easytpl:EasyTemplateEngine'
      ]
    }
  )


Et voilà, soufflé!

If you also want to support pre-compilation (i.e. server-side template
tokenization for faster client-side runtime evaluation), then take a
look at the `handlebars implementation
<https://github.com/canaryhealth/jstc/blob/master/jstc/engines/handlebars.py>`_.


.. _Handlebars: http://handlebarsjs.com/
.. _Mustache: http://mustache.github.io/
.. _Mako: http://www.makotemplates.org/
