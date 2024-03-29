=======
RectROI
=======

:mod:`xrdimageutil.roi.RectROI`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: xrdimageutil.roi.RectROI

The ``RectROI`` class provides a 3D "box" region of interest that can be applied
to 3D datasets. Users can define the coordinate bounds for the region, define a
calculation to be carried out on the selected region, and then apply the ROI
to multple datasets. This tool is scriptable, and the region bounds/calculation 
can be modified at any point.

In the Image GUI widget (refer to the :doc:`../tutorials/viewing_image_data` tutorial),
there is a graphical version of the ``RectROI`` object that is built on the backend
class, but it does not provide the same scriptability, only being available for single
datasets at a time.

Tutorial: :doc:`../tutorials/using_rois`

Attributes
^^^^^^^^^^

.. py:attribute:: bounds
    :type: dict

    Coordinate bounds for the rectangular region. These can be defined by using the 
    ``set_bounds`` function.
    
.. py:attribute:: calculation
    :type: dict

    Output calculation and the dims to calculate across. This can be defined by using
    the ``set_calculation`` function.

.. py:attribute:: output
    :type: dict

    Output data and coordinates.

Functions
^^^^^^^^^

.. py:function:: __init__(self, dims: list=None)

    If ``dims`` is not specified, the dimensions of the ROI will default
    to "x", "y", and "z" respectively. Order matters.

.. py:function:: set_bounds(self, bounds: dict)

    Defines the ROI coordinate bounds.

.. py:function:: set_calculation(self, output: str, dims: list) 

    Defines the calculation to be applied.

.. py:function:: apply(self, data, coords)

    Applies the set calculation to a dataset and its defined coordinates.

.. py:function:: apply_to_scan(self, scan, data_type)

    Applies the set calculation to a dataset for a ``xiu.Scan`` object,
    defining the data type by either "raw" or "gridded".

.. py:function:: get_output(self)

    Returns the output data and coordinates.
    