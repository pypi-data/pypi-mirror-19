swc2vtk
=======

|travisci| |Coverage Status| |python-2.7,3.3,3.4-blue| |license|
|paraview| |NEURON|

| SWC to VTK converter for visualizing neurons and neural circuit
  simulations in ParaView.
| This software helps making easy and beautiful visualization of large
  scale multi-compartmental neuron simulation with highly parallelized
  environments.

Dependency
----------

-  tqdm
-  numpy
-  [STRIKEOUT:PyVTK]

Install
-------

-  $ pip install swc2vtk

Usage
-----

Basic way to generate VTK file from one SWC file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import swc2vtk
    vtkgen = swc2vtk.VtkGenerator()
    vtkgen.add_swc('simple.swc')
    vtkgen.write_vtk('simple.vtk')

generate a VTK file from multiple SWC files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import swc2vtk
    vtkgen = swc2vtk.VtkGenerator()
    vtkgen.add_swc('simple.swc')
    vtkgen.add_swc('simple1.swc')
    vtkgen.add_swc('simple2.swc')
    vtkgen.write_vtk('combined.vtk')

generate a VTK file from SWC file with simulation data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import swc2vtk
    vtkgen = swc2vtk.VtkGenerator()
    vtkgen.add_swc('simple.swc')
    vtkgen.add_datafile('result.dat')
    vtkgen.write_vtk('simple.vtk')

-  | data example
   | each rows correspondence to SWC compartments

   ::

       -65.0
       -65.0
       -65.0
       -65.0

generate VTK files from SWC file with sequential simulation data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import swc2vtk
    vtkgen = swc2vtk.VtkGenerator()
    vtkgen.add_swc('simple.swc')

    vtkgen.add_datafile('result1.dat')
    vtkgen.write_vtk('simple1.vtk')

    vtkgen.clear_datafile()
    vtkgen.add_datafile('result2.dat')
    vtkgen.write_vtk('simple2.vtk')

    vtkgen.clear_datafile()
    vtkgen.add_datafile('result3.dat')
    vtkgen.write_vtk('simple3.vtk')

generate VTK file for volume rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import swc2vtk
    vtkgen = swc2vtk.VtkGenerator()
    vtkgen.add_swc('simple.swc')
    vtkgen.write_volume_vtk('volume.vtk')

Settings
--------

Visualization Quality
~~~~~~~~~~~~~~~~~~~~~

-  ``Draw Mode`` change SWC compartment drawing method. Largeer number
   is better.
-  ``0``: simple cylinder
-  ``1``: one cylinder with variable top surface
-  ``2``: one cylinder with three cell mode
-  ``3``: one cylinder with a hemisphere

.. code:: python

    import swc2vtk
    vtkgen = swc2vtk.VtkGenerator()
    vtkgen.add_swc('simple.swc')
    vtkgen.set_draw_mode(4)
    vtkgen.write_vtk('simple.vtk')

-  ``Division Number``

   .. code:: python

       import swc2vtk
       vtkgen = swc2vtk.VtkGenerator()
       vtkgen.add_swc('simple.swc')
       vtkgen.set_division_number(20)
       vtkgen.write_vtk('simple.vtk')

adjust compartment diameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``normalize_diam``

Output Examples
---------------

Single Neuron Morphology
~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: https://github.com/DaisukeMiyamoto/swc2vtk/releases/download/v0.01/singleneuron_small.png
   :alt: single

   single

-  `high resolution
   version <https://github.com/DaisukeMiyamoto/swc2vtk/releases/download/v0.01/singleneuron.png>`__

Coloring Multiple SWC Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: https://github.com/DaisukeMiyamoto/swc2vtk/releases/download/v0.01/standardbrain_small20170110.png
   :alt: Coloring

   Coloring

Single Neuron Simulation
~~~~~~~~~~~~~~~~~~~~~~~~

Neural Circuit Simulation
~~~~~~~~~~~~~~~~~~~~~~~~~

Volume Rendering
~~~~~~~~~~~~~~~~

References
----------

-  SWC format: http://research.mssm.edu/cnic/swc.html
-  http://www.paraview.org/
-  http://www.vtk.org/

.. |travisci| image:: https://travis-ci.org/DaisukeMiyamoto/swc2vtk.svg?branch=master
.. |Coverage Status| image:: https://coveralls.io/repos/github/DaisukeMiyamoto/swc2vtk/badge.svg?branch=master
   :target: https://coveralls.io/github/DaisukeMiyamoto/swc2vtk?branch=master
.. |python-2.7,3.3,3.4-blue| image:: https://img.shields.io/badge/python-2.7,3.3,3.4-blue.svg
.. |license| image:: https://img.shields.io/badge/license-apache-blue.svg
.. |paraview| image:: https://img.shields.io/badge/Paraview-5.2-green.svg
.. |NEURON| image:: https://img.shields.io/badge/NEURON-7.4-green.svg

