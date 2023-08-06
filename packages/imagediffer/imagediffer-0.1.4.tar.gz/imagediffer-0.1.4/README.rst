Image Differ
============

.. image:: https://badge.fury.io/py/imagediffer.svg
    :target: https://pypi.python.org/pypi/imagediffer

.. image:: https://travis-ci.org/janslifka/imagediffer.svg?branch=master

.. image:: https://readthedocs.org/projects/imagediffer/badge/?version=latest
    :target: http://imagediffer.readthedocs.io/en/latest/?badge=latest


Image Differ is a tool for image comparison. It loads 2 images (either local files or from the internet) and generates the diff image that shows where the images are different. It also calculates:

- Percentage of pixels where the images differ (with adjustable threshold for difference)
- Mean Square Error for the images
- Structural Similarity Index

It can also calculate comparison stats for individual color channels or convert images to grayscale.

Image Differ can be used as a library for other projects or it provides GUI application.


Installation
------------

The easiest way to install imagediffer is using pip

.. code-block::

   python -m pip install imagediffer


You can also clone this repository, install requirements using pip and then install imagediffer
using setup.py.

.. code-block::

   python setup.py install


Documentation
-------------

- `API Documentation <http://imagediffer.readthedocs.io>`_

If you want to build documentation yourself, you need to have `sphinx doc <http://www.sphinx-doc.org/>`_ installed and
then run ``make html`` in the docs folder.


Development
-----------

Simply clone the project and install dependencies from ``requirements.txt`` file using pip.

.. code-block::

   python -m pip install -r requirements.txt


Used libraries
--------------

- `NumPy <https://pypi.python.org/pypi/numpy>`_
- `Pillow <https://pypi.python.org/pypi/Pillow>`_
- `PyQt5 <https://pypi.python.org/pypi/PyQt5>`_
- `pyssim <https://pypi.python.org/pypi/pyssim>`_
- `pytest <https://pypi.python.org/pypi/pytest>`_
- `requests <https://pypi.python.org/pypi/requests>`_
- `SciPy <https://pypi.python.org/pypi/scipy>`_
- `Sphinx <https://pypi.python.org/pypi/Sphinx>`_
