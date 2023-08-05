======
TODO's
======

* it would be great if multi-templates could refer to other templates
  relatively... eg:

    ## file myapp/static/templates/common/person.hbs

      ##! summary
        <div>
          {{> "./name"}} is {{> "./gender"}}.
        </div>
      ##! name
        <span class="name">{{lastname}}, {{firstname}}</span>
      ##! gender
        {{#if-eq gender 'm'}}
          male
        {{else}}{{#if-eq gender 'f'}}
          female
        {{else}}{{#if-eq gender 't'}}
          transgender
        {{else}}
          unknown gender
        {{/if-eq}}{{/if-eq}}{{/if-eq}}

  would resolve "common/person/summary" to:

    {{> "common/person/name"}} is {{> "common/person/gender"}}.

  since there are *many* issues with doing that, perhaps a
  workaround could be to have the "summary" template start off
  with one of these:

    {{> "__here__/name"}} is {{> "__here__/gender"}}.
    {{> "__HERE__/name"}} is {{> "__HERE__/gender"}}.
    {{> "${__here__}/name"}} is {{> "${__here__}/gender"}}.
    {{> "${JSTC:HERE}/name"}} is {{> "${JSTC:HERE}/gender"}}.

  note that it should prolly be able to support (and resolve):

    {{> "__here__/../../name"}}

  ==> how to escape that??? perhaps:

    Python double underscore attributes, e.g. \__here__, are special.
    (in the jstc output, there would be no "\")


* move to new "weighted" collision mode, where collision can have:

  "weighted"
  "weighted-first"
  "weighted-last"
  "use-first" (deprecate: "ignore")
  "use-last" (deprecate: "override")

  and add "weight" attribute, which defaults to 0.

* if `precompile` is true, but a PrecompilerUnavailable error is
  returned, jstc silently goes into precompile=false mode... perhaps
  there should be a way to override that so that it throws an
  exception?

* If a template type is not registered in Compiler.mimetypes:
  * warn via log.warn()
  * force 'precompile' to false

* Support non-asset-specs in Compiler.render()
  (maybe Compiler.render_files(), etc, ala lessc.Compiler.render_*()?)

* Move `jstc.engines.base.Engine` into `jstc.api`
