Introduction
============

.. image:: https://img.shields.io/pypi/v/imagefactory.svg
   :target: https://pypi.python.org/pypi/imagefactory

.. image:: https://img.shields.io/travis/jaantollander/imagefactory.svg
   :target: https://travis-ci.org/jaantollander/imagefactory

.. image:: https://readthedocs.org/projects/imagefactory/badge/?version=latest
   :target: https://imagefactory.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jaantollander/imagefactory/shield.svg
   :target: https://pyup.io/repos/github/jaantollander/imagefactory/
   :alt: Updates


Python package for creating test images. Test images can be created as in
memory images or saved in to the filesystem. Package is released under MIT
license.

Examples
--------

Examples of the images created by the package.

.. list-table::
   :header-rows: 1

   * - jpeg
     - png
     - svg

   * - .. image:: _images/untitled.jpeg
          :target: _images/untitled.jpeg
          :alt: example.jpeg

     - .. image:: _images/untitled.png
          :target: _images/untitled.png
          :alt: example png

     - .. image:: _images/untitled.svg
          :target: _images/untitled.svg
          :alt: example svg

Basic Usage
-----------
Currently there is only one function ``create_image``.

.. autofunction:: imagefactory.imagefactory.create_image
