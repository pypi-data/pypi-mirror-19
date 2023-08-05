pyplan
======

The pyplan project is being developed to provide tools for
planning-level alternative analysis of progresive capital improvement
projects. pyplan is well suited to illustrate the cost/benefit dynamics
of projects made up of several independent and combinable sub-projects.

Example use case:
^^^^^^^^^^^^^^^^^

A utility is interested in addresing a regional flooding issue with new
releif sewers. Relief sewers are being considered in three different
areas, each of which may be implemented at 1, 2, or 3 mile lengths. The
relief sewers in each area can be combined with relief sewers in the
other two areas, regardless of how long any reach is.

Engineers then produce cost estimates and measure the performance of
every logical combination of flood releif sewer installation. (The
`swmmio`_ package is being developed to generate flood releif models
with EPA SWMMM5 for this exact use case). With cost benefit data
available for every incremental flood relief sewer phase, pyplan can
find the most efficient implementation paths:

.. figure:: /docs/example-pyplan-output.png
   :alt: example output

   example output

.. _swmmio: https://github.com/aerispaha/swmmio
