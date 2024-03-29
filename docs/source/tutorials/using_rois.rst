===========
Using ROI's
===========

``xrd-image-util`` also provides ROI's to retrieve information from subsections of a 3D dataset. 
Currently, the only ROI class available is ``xiu.roi.RectROI``. The general workflow for an ROI
goes as follows:

#. Creating the ROI
#. Setting coordinate bounds for the ROI
#. Setting the output calculations for the ROI
#. Applying the ROI to a 3D dataset
#. Retreiving the output data and coordinates

A useful characteristic of ``xrd-image-util``'s ROI's is that they are data-independent, meaning 
that you can apply the same ROI to a series of 3D images. Here is a simple example of creating a rectangular ROI,
applying it to a set of ``Scan`` objects, and storing the output:

.. code-block:: python

    # Getting a list of scans to analyze
    catalog = xiu.Catalog("test-catalog")
    scans = catalog.get_scans([68, 69, 70])

    # Instantiating the rectangular ROI
    roi = xiu.roi.RectROI()

    # Bounding the region
    roi.set_bounds(
        bounds={
            "H": (-1, -0.9),
            "K": (None, None),
            "L": [3.4, 3.45]
        }
    )

    # Setting the output value
    # In this example, the data is being averaged across all 'K' values.
    # The output arrays will be 2D with axis labels 'H' and 'L'.
    roi.set_calculation(output="average", dims=["K"])

    scan_data = []
    for scan in scans:

        # Gridding scan image data
        scan.grid_data((50, 50, 50))

        # Applying ROI to scan
        roi.apply_to_scan(scan=scan, data_type="gridded")

        # Adding output to list
        scan_data.append(roi.get_output())

    print([s["data"].shape for s in scan_data])
    # Output: [(21, 21), (21, 21), (21, 21)]


