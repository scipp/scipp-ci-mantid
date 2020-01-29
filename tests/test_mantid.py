# Tests in this file work only with a working Mantid installation available in
# PYTHONPATH.
import unittest
import pytest

import scipp as sc
from scipp import neutron
import numpy as np

from mantid_data_helper import MantidDataHelper


def mantid_is_available():
    try:
        import mantid  # noqa: F401
        return True
    except ImportError:
        return False


def check_monitors(dataset, shape):
    for name, val in dataset.attrs.items():
        if "monitor" in name:
            assert isinstance(val.value, sc.DataArray)
            assert val.value.shape == [shape]


@pytest.mark.skipif(not mantid_is_available(),
                    reason='Mantid framework is unavailable')
class TestMantidConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import mantid.simpleapi as mantid
        # This is from the Mantid system-test data
        filename = "CNCS_51936_event.nxs"
        # This needs OutputWorkspace specified, as it doesn't
        # pick up the name from the class variable name
        cls.base_event_ws = mantid.LoadEventNexus(
            MantidDataHelper.find_file(filename),
            OutputWorkspace="test_ws{}".format(__file__))

    def test_Workspace2D(self):
        import mantid.simpleapi as mantid
        eventWS = mantid.CloneWorkspace(self.base_event_ws)
        ws = mantid.Rebin(eventWS, 10000, PreserveEvents=False)
        d = sc.neutron.from_mantid(ws)
        self.assertEqual(
            d.attrs["run"].value.getProperty("run_start").value,
            "2012-05-21T15:14:56.279289666",
        )

    def test_EventWorkspace(self):
        import mantid.simpleapi as mantid
        eventWS = mantid.CloneWorkspace(self.base_event_ws)
        ws = mantid.Rebin(eventWS, 10000, PreserveEvents=False)

        binned_mantid = sc.neutron.from_mantid(ws)

        target_tof = binned_mantid.coords[sc.Dim.Tof]
        d = sc.neutron.from_mantid(eventWS)
        binned = sc.histogram(d, target_tof)

        delta = sc.sum(binned_mantid - binned, sc.Dim.Spectrum)
        delta = sc.sum(delta, sc.Dim.Tof)
        self.assertLess(np.abs(delta.value), 1e-5)

    def test_unit_conversion(self):
        import mantid.simpleapi as mantid
        eventWS = mantid.CloneWorkspace(self.base_event_ws)
        ws = mantid.Rebin(eventWS, 10000, PreserveEvents=False)
        tmp = sc.neutron.from_mantid(ws)
        target_tof = tmp.coords[sc.Dim.Tof]
        ws = mantid.ConvertUnits(InputWorkspace=ws,
                                 Target="Wavelength",
                                 EMode="Elastic")
        converted_mantid = sc.neutron.from_mantid(ws)

        da = sc.neutron.from_mantid(eventWS)
        da = sc.histogram(da, target_tof)
        d = sc.Dataset(da)
        converted = sc.neutron.convert(d, sc.Dim.Tof, sc.Dim.Wavelength)

        self.assertTrue(
            np.all(np.isclose(converted_mantid.values, converted[""].values)))
        self.assertTrue(
            np.all(
                np.isclose(
                    converted_mantid.coords[sc.Dim.Wavelength].values,
                    converted.coords[sc.Dim.Wavelength].values,
                )))
        # delta = sc.sum(converted_mantid - converted, sc.Dim.Spectrum)

    @staticmethod
    def _mask_bins_and_spectra(ws, xmin, xmax, num_spectra):
        import mantid.simpleapi as mantid
        masked_ws = mantid.MaskBins(ws, XMin=xmin, XMax=xmax)

        # mask the first 3 spectra
        for i in range(num_spectra):
            masked_ws.spectrumInfo().setMasked(i, True)

        return masked_ws

    def test_Workspace2D_common_bins_masks(self):
        import mantid.simpleapi as mantid
        eventWS = mantid.CloneWorkspace(self.base_event_ws)
        ws = mantid.Rebin(eventWS, 10000, PreserveEvents=False)
        ws_x = ws.readX(0)

        # mask the first 3 bins, range is taken as [XMin, XMax)
        masked_ws = self._mask_bins_and_spectra(ws,
                                                xmin=ws_x[0],
                                                xmax=ws_x[3],
                                                num_spectra=3)

        self.assertTrue(masked_ws.isCommonBins())

        ds = sc.neutron.from_mantid(masked_ws)

        np.testing.assert_array_equal(
            ds.masks["bin"].values[0:3],
            [True, True, True])

        np.testing.assert_array_equal(
            ds.masks["spectrum"].values[0:3],
            [True, True, True])

    def test_Workspace2D_not_common_bins_masks(self):
        import mantid.simpleapi as mantid
        eventWS = mantid.CloneWorkspace(self.base_event_ws)
        ws = mantid.Rebin(eventWS, 10000, PreserveEvents=False)
        ws = mantid.ConvertUnits(ws, "Wavelength",
                                 EMode="Direct",
                                 EFixed=0.1231)

        # these X values will mask different number of bins
        masked_ws = self._mask_bins_and_spectra(ws, -214, -192, num_spectra=3)

        self.assertFalse(masked_ws.isCommonBins())

        ds = sc.neutron.from_mantid(masked_ws)

        # bin with 3 masks
        np.testing.assert_array_equal(
            ds.masks["bin"].values[0],
            [True, True, False, False, False])

        # bin with only 2
        np.testing.assert_array_equal(
            ds.masks["bin"].values[31],
            [True, True, True, False, False])

        np.testing.assert_array_equal(
            ds.masks["spectrum"].values[0:3],
            [True, True, True])

#    def test_Workspace2D_with_separate_monitors(self):
#        filename = MantidDataHelper.find_file("WISH00016748.raw")
#        ds = sc.neutron.load(filename,
#                               mantid_args={"LoadMonitors": "Separate"})
#        check_monitors(ds, 4471)

#    def test_Workspace2D_with_include_monitors(self):
#        filename = MantidDataHelper.find_file("WISH00016748.raw")
#        ds = sc.neutron.load(filename,
#                               mantid_args={"LoadMonitors": "Include"})
#        check_monitors(ds, 4471)

    def test_EventWorkspace_with_monitors(self):
        filename = MantidDataHelper.find_file("CNCS_51936_event.nxs")
        ds = sc.neutron.load(filename, mantid_args={"LoadMonitors": True})
        check_monitors(ds, 200001)

    def test_Workspace2D_with_specific_axis_units(self):
        filename = MantidDataHelper.find_file("iris26176_graphite002_sqw.nxs")
        ds = sc.neutron.load(filename)
        assert ds.shape == [23, 200]
        assert ds.dims == [sc.Dim.Q, sc.Dim.EnergyTransfer]


if __name__ == "__main__":
    unittest.main()
