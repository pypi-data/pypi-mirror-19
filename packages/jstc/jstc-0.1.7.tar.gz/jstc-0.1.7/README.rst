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
* Manual: https://github.com/canaryhealth/jstc/blob/master/doc/manual.rst


Installation
============

.. code:: bash

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
  <html>
    <!-- ... -->
    <body>

      <div id="Main">Loading...</div>

      <!-- load all the *.hbs templates -->
      <div id="Templates" style="display:none">
        ${jstc.render_assets('myapp:static/scripts/**.hbs')|n}
      </div>

      <script type="text/javascript">
        // your javascript that makes use of the templates
      </script>

    </body>
  </html>


Example
=======

Given that the following files exist in the Python package `myapp`:

File ``myapp/static/templates/common/hello.hbs``::

  Hello, {{name}}!


File ``myapp/static/templates/common/inputs.hbs`` (a "multi-template" file)::

  ##! text

    <input type="text" name="{{name}}" value="{{value}}"/>

  ##! checkbox

    <input type="checkbox" name="{{name}}" value="1" {{#if value}}checked="checked"{{/if}}/>


Then, the Python code (`inline` and `precompile` attributes used for
output simplicity):

.. code:: python

  import jstc
  jstc.render_assets(
    'myapp:static/templates/common/**.hbs', 'static/templates',
    force_inline=True, force_precompile=False)


Outputs the following HTML (whitespace and newlines added for clarity):

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


See https://github.com/canaryhealth/jstc/blob/master/doc/manual.rst for
more documentation.


.. _Handlebars: http://handlebarsjs.com/
.. _Mustache: http://mustache.github.io/
.. _Mako: http://www.makotemplates.org/
