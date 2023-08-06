=======
Jekkish
=======

Introduction
------------------------------

Inspired by the writing workflow of Markdown + YAML used in Jekyll, I wanted a system that would allow me to do something similar for LaTeX files. More often than not, I reuse my LaTeX styles, and import a file of content in the {maincontent} environment. Hopefully you can find it useful too.

This program takes files that look like the sample below (LaTeX content with YAML header), generates a full LaTeX file, and then compiles this with pdftex.

Disclaimer
------------------------------

While this code works (with no guarantees), it definitely needs tests and better error handling and more flexible of code. That said, this is far enough along that it works... so that's pretty awesome! These files can be built directly in Sublime Text if you follow the instructions below.

I intend to keep this compatible with both Python 2 and 3, but since it is in alpha, Python 3 support is not always guaranteed.

Successfully run on OSX, Ubuntu, and Windows (cygwin).

Installation
-------------------------

This package is available on PyPI. To install, just type ``pip install jekkish`` in your terminal.

If you use SublimeText, you can use place jekkish.sublime-build in your Sublime Packages/User directory.

Dependencies.
--------------------------

This package uses PyYAML, Jinja2. It assumes that pdftex is installed and included in the system path.

There is a bare-bones template called "default" included in this package and can be used as a reference. Additional templates should be placed in ~/.jekkish/

Sample document, conventions, and instructions
-----------------------------------------------------------------

Below is a sample document.

::

    ---
    template: default
    title: I wrote a something
    subtitle: A tale of longing and desperation
    author: Gebralter Crowlin
    date:   "January 11, 1906"
    packages:
      - GaramondPremierPro
      - endnotes
    spacing: \doublespace
    ---
    Look at \emph{all} of the things I wrote!

The only reserved variable names are *template* and *content*.

Feel free to use any others you find useful for your documents. The system uses Jinja2, so you are free to make templates as simple or complicated as you please.

-   Assumes that *template*.tex can be found in ~/.jekkish
-   Should be placed in the mainmatter of your template as (((content))).
-   Everything above the YAML header will be ignored.
-   Everything below the YAML header will be rendered in the (((content))) tag.

In the template, these files are essentially LaTeX files, but with some templating logic.

-   ((\* \*)) is used for template logic
-   (((variable\_name))) is used for where variables will be rendered.
-   ((= comments =)) are found between these characters

Command Line
----------------------
A full list of options can be found by running ``jekkish --help``

Basic use ``jekkish <filename>``

An optional jobname can be added, e.g. ``jekkish <filename> <jobname>``

To run Jekkish in watch mode type the above with the optional tag ``--watch``

License
-------

This software is available under the `MIT <http://en.wikipedia.org/wiki/MIT_License>`__ license
