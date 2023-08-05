======
TODO's
======


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
