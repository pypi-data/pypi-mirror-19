=========
ChangeLog
=========


v0.1.6
======

* Reverted the default value for ``space`` to "dedent" to avoid the
  overly aggressive whitespace collapsing (this needs to be rectified
  before re-enabling "collapse" as the default)


v0.1.5
======

* Added template attribute ``space`` with support to collapse
  "ignorable" whitespace
* Deprecated template attribute ``trim`` in favor of ``space``


v0.1.4
======

* Renamed `render_assets()` parameters `inline` and `precompile` to be
  prefixed with `force_` so as to make consequence clearer
* Added `render_assets()` parameter `script_wrapper`
* Fixed `render_assets()` to properly handle pre-compilers that can be
  optimized via partial JavaScript code generation


v0.1.3
======

* Removed `distribute` dependency
* Updated documentation
* Implemented pre-compilation for handlebars engine


v0.1.0
======

* First release
