===================
Authoring a Toolbox
===================

Essentially, authoring a transmute toolbox involves providing two main
features:

1. a way to register a transmute function to the application object
2. a way to generate a swagger.json from an application object

for inspiration, here are a couple of reference implementations:

* https://github.com/toumorokoshi/aiohttp-transmute
* https://github.com/toumorokoshi/tornado-transmute

web-transmute is deliberately agnostic to the integration approach. It
is recommended to choose a pattern that works well with the
framework's style of adding handlers and extending functionality
(i.e. use decorators for flask, handler classes for tornado)
