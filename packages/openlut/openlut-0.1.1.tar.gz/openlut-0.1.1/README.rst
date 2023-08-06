openlut
=======

Open-source tools for practical color management.
-------------------------------------------------

What is it?
-----------

openlut is, at its core, a color management library, accessible from
**Python 3.5+**. It’s built on my own color pipeline needs, which
includes managing Lookup Tables, Gamma/Gamut functions/matrices,
applying color transformations, etc. .

openlut is also a tool. Included soon will be a command line utility
letting you perform complex color transformations from the comfort of
your console. In all cases, interactive usage from a Python console is
easy.

I wanted it to cover this niche simply and consistently, something color
management often isn’t! Take a look; hopefully you’ll agree :) !

What About OpenColorIO? Why does this exist?
--------------------------------------------

OpenColorIO is a wonderful library, but seems geared towards managing
the complexity of many larger applications in a greater pipeline.
openlut is more simple; it doesn’t care about the big picture - you just
do consistent operations on images. openlut also has tools to deal with
these building blocks, unlike OCIO - resizing LUTs, etc. .

Indeed, OCIO is just a system these basic operations using LUTs - in
somewhat unintuitive ways, in my opinion. You could setup a similar
system using openlut’s toolkit.

Installation
------------

I’ll put it on pip eventually (when I figure out how!). For now, just
download the repository.

To run openlut.py, first make sure you have the *Dependencies*. To run
the test code at the bottom (make sure openlut is in the same directory
as testpath; it needs to load test.exr), you can then run:

``python3 main.py -t``

To use in your code, simply ``import`` the module at the top of your
file.

Dependencies
------------

There are some dependencies that you must get. Keep in mind that it’s
**Python 3.X** *only*; all dependencies must be their 3.X versions.

Getting python3 and pip3
~~~~~~~~~~~~~~~~~~~~~~~~

If you’re on a **Mac**, run this to get python3 and pip3:
``brew install python3; curl https://bootstrap.pypa.io/get-pip.py | python3``
If you’re on **Linux**, you should already have python3 and pip3 -
otherwise see your distribution repositories.

Dependency Installation
~~~~~~~~~~~~~~~~~~~~~~~

Run this to get all deps: ``sudo pip3 install numpy wand numba scipy``

Basic Library Usage
-------------------

To represent images, use a **ColMap** object. This handles IO to/from
all ImageMagick supported formats (**including EXR and DPX**), as well
as storing the image data.

Use any child of the **Transform** class to do a color transform on a
ColMap, using ColMap’s ``apply(Transform)`` method.

The **Transform** objects themselves have plenty of features - like LUT,
with ``open()``, ``save()``, and ``resize()`` methods, or TransMat with
auto-combining input matrices, or automatic spline-based interpolation
of very small 1D LUTs - to make them helpful in and of themselves!

The best way to demonstrate this, I think, is to see the test code.
(run python3 openlut.py -t to see it work)