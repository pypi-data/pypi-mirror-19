===============================
pandoc_minted
===============================


.. image:: https://img.shields.io/pypi/v/pandoc_minted.svg
        :target: https://pypi.python.org/pypi/pandoc_minted

.. image:: https://img.shields.io/travis/D3f0/pandoc_minted.svg
        :target: https://travis-ci.org/D3f0/pandoc_minted

.. image:: https://readthedocs.org/projects/pandoc-minted/badge/?version=latest
        :target: https://pandoc-minted.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/D3f0/pandoc_minted/shield.svg
     :target: https://pyup.io/repos/github/D3f0/pandoc_minted/
     :alt: Updates


Pandoc filter to provide minted support (github.com/nick-ulle/pandoc-minted)

Usage
-----

Besides installing minted, you'll have to include it either in your templates or in your markdown header metadata, as follows::

    ---
    title: Test
    author: Author Name
    header-includes:
        - \usepackage{minted}
    ---

Pandoc generates tex for minted in a temporary file so you'll experience this errors `read more <https://www.bountysource.com/issues/28453810-minted-in-pandoc>`_
::

        ! Package minted Error: Missing Pygments output; \inputminted was
        probably given a file that does not exist--otherwise, you may need
        the outputdir package option, or may be using an incompatible build tool.

So you'll need to use this commands as follows::

    pandoc -F pandoc-minted -s myfile.md -o myfile.tex
    pdflatex --shell-escape myfile.tex



Licence
-------

* Free software: MIT license
* Documentation: https://pandoc-minted.readthedocs.io.



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

