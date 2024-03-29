====
Scan
====

:mod:`xrdimageutil.Scan`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: xrdimageutil.Scan

Attributes
^^^^^^^^^^

.. py:attribute:: catalog
    :type: xrdimageutil.Catalog

    Parent Catalog

.. py:attribute:: uid
    :type: str

    UID for scan; automatically generated in bluesky catalog

.. py:attribute:: bluesky_run
    :type: databroker.BlueskyRun

    Raw Bluesky run for scan

.. py:attribute:: scan_id
    :type: int

    Numerical ID for scan -- not always unique

.. py:attribute:: sample
    :type: str

    Experimental sample

.. py:attribute:: proposal_id
    :type: str

    Manually provided Proposal ID

.. py:attribute:: user
    :type: str

    Experimental user

.. py:attribute:: motors
    :type: list

    List of variable motors for scan
    
.. py:attribute:: rsm
    :type: numpy.ndarray

    Reciprocal space map for every point within a scan

.. py:attribute:: raw_data
    :type: numpy.ndarray

    Data and coordinates (t, x, y) for raw 2D detector images

.. py:attribute:: gridded_data
    :type: numpy.ndarray

    Data and coordinates (H, K, L) for a scan's mapped 3D volume

Functions
^^^^^^^^^

.. py:function:: __init__(self, catalog: Catalog, uid: str)

.. py:function:: grid_data(self, shape: tuple, bounds: dict=None)

.. py:function:: point_count(self)

.. py:function:: view_image_data(self)
