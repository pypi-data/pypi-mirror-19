CoR-Lab Sphinx Theme
====================

A theme for `CoR-Lab <https://www.cor-lab.org>`_ software documentation
projects.

Usage
-----

In your sphinx project `conf.py` add:

.. code:: python

   import corlab_theme
   # ...
   html_theme      = 'corlab_theme'
   html_theme_path = [ corlab_theme.get_theme_dir() ]
