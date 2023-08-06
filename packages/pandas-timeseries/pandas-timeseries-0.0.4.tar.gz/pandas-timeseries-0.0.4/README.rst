.. image:: https://travis-ci.org/sealevelresearch/timeseries.svg?branch=master
    :target: https://travis-ci.org/sealevelresearch/timeseries
.. image:: https://coveralls.io/repos/github/sealevelresearch/timeseries/badge.svg?branch=master
    :target: https://coveralls.io/github/sealevelresearch/timeseries?branch=master


Time Series
==================

A time series built upon `pandas <http://pandas.pydata.org>`_ for dealing with window/point data sources, which has interpolation mindful of gap's.


Design
######

Each window is represented by `valid_from`, `valid_to`, `value`.

During interpolation, the window time range is transformed into a center point `datetime`.

A constraint on the data model is a predefined length of a window, this length is used to query all suitable data and compute gaps.

Gaps are determined and a mask is applied to the original data frame.

When performing a query on a data frame, missing data at the tail and head are filled in.

Sample data
###########
Below are a visual representation of data within the tests.

.. image:: design/ExampleA0.png
    :alt: Example A0 - Single data day
    :width: 100% 
    :align: center

.. image:: design/ExampleA1.png
    :alt: Example A1 - Non-numeric content
    :width: 100% 
    :align: center

.. image:: design/ExampleA2.png
    :alt: Example A2 - Multiple with non-numeric content
    :width: 100% 
    :align: center

.. image:: design/ExampleB0.png
    :alt: Example B0 - Missing window at the start
    :width: 100% 
    :align: center

.. image:: design/ExampleB1.png
    :alt: Example B1 - Missing window in the middle
    :width: 100% 
    :align: center

.. image:: design/ExampleB2.png
    :alt: Example B2 - Missing window at the end 
    :width: 100% 
    :align: center

.. image:: design/ExampleC.png
    :alt: Example C - Gaps between windows
    :width: 100% 
    :align: center

.. image:: design/ExampleD.png
    :alt: Example D - No data
    :width: 100% 
    :align: center

.. image:: design/ExampleE.png
    :alt: Example E - Multiple columns
    :width: 100% 
    :align: center

.. image:: design/ExampleF.png
    :alt: Example F - Multiple with non-numeric content
    :width: 100% 
    :align: center


Compatibility
*************
This project is compatible with Python 3.5+, Pandas 0.19.

Development state
*****************
This library is in alpha state and is subject to revision. 
