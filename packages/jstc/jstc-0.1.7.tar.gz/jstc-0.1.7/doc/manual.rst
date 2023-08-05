===================================
JavaScript Template Compiler Manual
===================================

The `jstc` Python package compiles and packages JavaScript templates
for delivery to browsers for client-side evaluation.

Currently, only `Handlebars`_ and `Mustache`_ template formats are
supported natively, however this is easily extended via jstc's plugin
mechanism.


Example
=======

The following (fully functional!) example should illustrate how `jstc`
works. Given the following files exist in the Python package `myapp`:

File ``myapp/static/templates/application.hbs``::

  {{#with recipient}}
    <h1>{{> "common/salutation"}}</h1>
  {{/with}}
  <h2>Your Family Members</h2>
  <ul>
    {{#each family}}
      <li>
        {{> "common/person"}}
      </li>
    {{/each}}
  </ul>


File ``myapp/static/templates/common/salutation.hbs``::

  Hello, {{first}}!


File ``myapp/static/templates/common/person.hbs`` (a "multi-template" file)::


  ##! __here__

    <div>
      <div class="name">{{> "common/person/name"}}</div>
      <div class="relation">{{> "common/person/rel"}}</div>
    </div>

  ##! name

    {{last}}, {{first}}

  ##! rel

    (your {{relation}})


And the Mako_ template (`inline` and `precompile` attributes used for
output simplicity):

.. code:: mako

  <%! import jstc %>
  <html>
    <head>
      <script type="text/javascript"
        src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
      <script type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.0.6/handlebars.min.js"></script>
    </head>
    <body>

      <div id="Main">Loading...</div>

      <!-- load all the *.hbs templates with jstc -->
      <div id="Templates" style="display:none">
        ${jstc.render_assets(
          'myapp:static/templates/**.hbs', 'static/templates',
          force_inline=True, force_precompile=False)|n}
      </div>

      <!-- use the templates with jquery and handlebars -->
      <script type="text/javascript">
        var data = {
          recipient: {first: 'Daenerys', last: 'Targaryen'},
          family: [
            {first: 'Viserys', last: 'Targaryen', relation: 'brother'},
            {first: 'Aerys II', last: 'Targaryen', relation: 'father'}
          ]
        };
        var templates = {};
        $('#Templates script[type="text/x-handlebars"]').each(function() {
          var node = $(this);
          var name = node.data('template-name');
          templates[name] = Handlebars.compile(node.html());
          Handlebars.registerPartial(name, node.html());
        });
        // render the "application" template into the "#Main" DOM element
        var template = templates['application'];
        $('#Main').html(template(data));
      </script>

    </body>
  </html>


Will result in the following HTML (non-displaying DOM elements removed):

.. code:: html

  <html>
    <body>
      <div id="Main">
        <h1>Hello, Daenerys!</h1>
        <h2>Your Family Members</h2>
        <ul>
          <li>
            <div>
              <div class="name">Targaryen, Viserys</div>
              <div class="relation">(your brother)</div>
            </div>
          </li>
          <li>
            <div>
              <div class="name">Targaryen, Aerys II</div>
              <div class="relation">(your father)</div>
            </div>
          </li>
        </ul>
      </div>
    </body>
  </html>


**AWESOME!**


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

  * ``dedent`` (the default):

    "Dedent" the template (i.e. remove all whitespace that prefixes
    every line in the template) and also apply the ``trim``
    transformation.

  * ``collapse``:

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

    The `collapse` whitespace handling approach isn't perfect (which
    is why it isn't the default). See the Whitespace_ section for
    details.

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

  # declare that this is a "jstc.engines.plugins" plugin of type "text/x-easytpl"
  @asset.plugin('jstc.engines.plugins', 'text/x-easytpl')
  class EasyTemplateEngine(jstc.engines.base.Engine):

    # declare the official mime-type of this engine
    mimetype    = 'text/x-easytpl'

    # and extensions that should map to this mime-type
    extensions  = ('.et',)

    # and that this engine does not support precompilation
    precompile  = jstc.PrecompilerUnavailable


And then in your myapp's ``setup.py``, add the following parameter to
your `setup` call (to make it available in the plugin entrypoints):

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
tokenization for faster client-side runtime evaluation), more
collapsable whitespace tokens, and other features, then take a look at
the `handlebars implementation
<https://github.com/canaryhealth/jstc/blob/master/jstc/engines/handlebars.py>`_.


Whitespace
==========

If you do a search for `how to remove whitespace between inline-block
elements in HTML
<http://lmgtfy.com/?s=d&q=how+to+remove+whitespace+between+inline-block+elements+in+HTML>`_,
you'll discover that this has long been an issue... `jstc` can help "a
bit" when you enable "space=collapse" mode.

When collapsing of whitespace is enabled, the following template:

.. code::

  {{#if flag}}
    <div>
      <img src="foo.png"/>
      {{value}}
    </div>
  {{/if}}


will be collapsed to:

.. code::

  {{#if flag}}<div><img src="foo.png"/>{{value}}</div>{{/if}}


which is **great**! Except when it it's not... For example, in the
following, you *want* the spaces between the "<span>" elements to
persist. To do that, add a space before the closing ">":

.. code::

  <div>
    <span>Joe</span >
    <span>Schmoe</span>
  </div>


and that will be collapsed to:

.. code::

  <div><span>Joe</span> <span>Schmoe</span></div>


Sorry. Ugly. I know. But it works and I couldn't come up with anything
else.


.. _Handlebars: http://handlebarsjs.com/
.. _Mustache: http://mustache.github.io/
.. _Mako: http://www.makotemplates.org/
