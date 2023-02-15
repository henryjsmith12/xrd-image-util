"""Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

import databroker
import numpy as np
from prettytable import PrettyTable
import pyqtgraph as pg
import xrayutilities as xu

from xrdimageutil import utils
from xrdimageutil.gui import image_data_widget, line_data_widget


class Catalog:
    """Houses (i) a Bluesky catalog, already unpacked and (ii) a 
    dictionary of Scan objects that can be accessed.
    """
    
    bluesky_catalog = None # Bluesky dictionary-like catalog
    name = None # Local name for catalog
    scan_uid_dict = None # Dictionary of scans in catalog with UID as key

    def __init__(self, name) -> None:

        self.name = str(name)
        self.bluesky_catalog = databroker.catalog[self.name]

        # Currently only configured for beamline 6-ID-B
        utils._add_catalog_handler(catalog=self)

        # Creates a Scan object for every run in the catalog
        # Adds Scans to a dictionary
        self.scan_uid_dict = {}
        for scan_uid in list(self.bluesky_catalog):
            scan = Scan(catalog=self, uid=scan_uid)
            self.scan_uid_dict.update({scan_uid: scan})

    def _load_scans(self, uids: list):

        for uid in uids:
            try:
                self.scan_uid_dict[uid] = Scan(catalog=self, uid=uid)
            except:
                pass

    def search(self, proposal_id=None, user=None, sample=None, scan_id=None, plan_name=None):
        """Simplified version of the databroker.catalog search function."""

        query = {}

        if proposal_id:
            query.update({"proposal_id": proposal_id})
        if user:
            query.update({"user": user})
        if sample:
            query.update({"sample": sample})
        if scan_id:
            query.update({"scan_id": scan_id})
        if plan_name:
            query.update({"plan_name": plan_name})
        
        results = self.bluesky_catalog.search(query)
        
        return list(results)

    def get_scan(self, uid=None, scan_id=None):
        ...
 
    def view_line_data(self, uids: list) -> None:
        """Displays Scan line data for a list of scans in an interactive GUI."""
        
        self.load_scans(uids=uids)

        self.app = pg.mkQApp()
        self.window = line_data_widget.CatalogLineDataWidget(catalog=self)
        self.window.raise_()
        self.window.show()
        self.window.raise_()
        self.app.exec_()

        
class Scan:
    """Houses data and metadata for a single scan."""

    catalog = None # Parent Catalog
    uid = None # UID for scan; given by bluesky
    id = None

    raw_data = None
    rsm = None
    gridded_data = None
    gridded_data_coords = None

    def __init__(self, catalog: Catalog, uid: str) -> None:

        self.catalog = catalog
        self.uid = uid
        self.scan_id = catalog.bluesky_catalog[uid].metadata["start"]["scan_id"]
        if "primary" in catalog.bluesky_catalog[uid].keys():
            omega_values = catalog.bluesky_catalog[uid].primary.read()["fourc_omega"].values
            chi_values = catalog.bluesky_catalog[uid].primary.read()["fourc_chi"].values
            phi_values = catalog.bluesky_catalog[uid].primary.read()["fourc_phi"].values
            tth_values = catalog.bluesky_catalog[uid].primary.read()["fourc_tth"].values

    # Loading functions to help with initial Scan creation time
    def _load_raw_image_data(self) -> None:
        """Loads raw image data from bluesky catalog."""

        # Only loaded in once per scan
        if not self.raw_data:
            run = self.catalog.bluesky_catalog[self.uid]

            if "primary" not in run.keys():
                return
            
            # Reads through keys to find detector image key
            for key in list(run.primary.read().keys()):
                key_np_array = run.primary.read()[key].values
                if np.squeeze(key_np_array).ndim == 3:
                    raw_data_4d = key_np_array
                    raw_data_3d_unordered = np.squeeze(raw_data_4d)
                    self.raw_data = np.swapaxes(raw_data_3d_unordered, 1, 2)
                    break

    def _load_rsm(self) -> None:
        """Loads reciprocal space map from bluesky catalog values."""

        if not self.rsm:
            self.rsm = utils._get_rsm_for_scan(scan=self)

    def grid_data(
        self, h_count: int=250, k_count: int=250, l_count: int=250,
        h_min: float=None, h_max: float=None, 
        k_min: float=None, k_max: float=None,
        l_min: float=None, l_max: float=None
    ) -> None:
        """Constructs gridded 3D image from RSM coordinates and raw image data."""

        self._load_raw_image_data()
        self._load_rsm()

        if not self.raw_data:
            raise ValueError("Raw image data not found.")
        if not self.rsm:
            raise ValueError("RSM not found.")

        # Provided bounds
        user_provided_bounds = [h_min, h_max, k_min, k_max, l_min, l_max]
        # Bounds from RSM
        rsm_bounds = utils._get_rsm_bounds(scan=self)

        if h_min >= h_max or k_min >= k_max or l_min >= l_max:
            raise ValueError("Invalid gridding bounds provided.")

        grid_bounds = []
        for u, r in zip(user_provided_bounds, rsm_bounds):
            if u:
                grid_bounds.append(u)
            else:
                grid_bounds.append(r)

        h_map = self.rsm[:, :, :, 0]
        k_map = self.rsm[:, :, :, 1]
        l_map = self.rsm[:, :, :, 2]

        # Prepares gridder bounds/interpolation
        gridder = xu.Gridder3D(
            nx=h_count, 
            ny=k_count, 
            nz=l_count
        )
        gridder.KeepData(True)
        gridder.dataRange(*grid_bounds, fixed=True)

        # Grids raw data with bounds
        gridder(h_map, k_map, l_map, self.raw_data)
        self.gridded_data = gridder.data

        # Retrieves HKL coordinates for gridded data
        self.gridded_data_coords = [gridder.xaxis, gridder.yaxis, gridder.zaxis]

    def view_image_data(self) -> None:
        """Displays image data in an interactive GUI."""
        
        self._load_raw_image_data()

        if not self.raw_data:
            raise ValueError("Raw image data not found.")
        
        self.app = pg.mkQApp()
        self.window = image_data_widget.ScanImageDataWidget(scan=self)
        self.window.raise_()
        self.window.show()
        self.window.raise_()
        self.app.exec_()
    