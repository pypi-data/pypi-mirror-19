uconfig
=======

uconfig is a simple parser for unix style configurations written in pure python.

Sorry for the lack of documentation.

Examples
--------


``example.conf``

::

   foo bar;
   foo {
      foobar Hello World;
   }

``$ python``

.. code:: python

   >>> import uconfig
   >>> cfg = uconfig.ExtendedConfig()
   >>> cfg.load("example.conf")
   >>> cfg.get_value("foo")
   'bar'
   >>> cfg["foo"].get_value("foobar")
   'Hello World'
