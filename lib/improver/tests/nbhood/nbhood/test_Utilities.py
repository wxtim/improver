# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# (C) British Crown Copyright 2017 Met Office.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Unit tests for the nbhood.Utilities plugin."""


import unittest

import iris
from iris.exceptions import CoordinateNotFoundError
from iris.tests import IrisTest
from iris.cube import Cube
import numpy as np

from cf_units import Unit

from improver.nbhood.nbhood import Utilities
from improver.tests.ensemble_calibration.ensemble_calibration.helper_functions\
    import add_forecast_reference_time_and_forecast_period
from improver.tests.nbhood.nbhood.test_NeighbourhoodProcessing import (
    set_up_cube)


class Test__repr__(IrisTest):

    """Test the repr method."""

    def test_basic(self):
        """Test that the __repr__ returns the expected string."""
        result = str(Utilities())
        msg = '<Utilities>'
        self.assertEqual(result, msg)


class Test_find_required_lead_times(IrisTest):

    """Test determining of the lead times present within the input cube."""

    def test_basic(self):
        """Test that a numpy array is returned."""
        cube = add_forecast_reference_time_and_forecast_period(set_up_cube())
        result = Utilities.find_required_lead_times(cube)
        self.assertIsInstance(result, np.ndarray)

    def test_check_coordinate(self):
        """
        Test that the data within the numpy array is as expected, when
        the input cube has a forecast_period coordinate.
        """
        cube = add_forecast_reference_time_and_forecast_period(set_up_cube())
        expected_result = cube.coord("forecast_period").points
        result = Utilities.find_required_lead_times(cube)
        self.assertArrayAlmostEqual(result, expected_result)

    def test_check_coordinate_without_forecast_period(self):
        """
        Test that the data within the numpy array is as expected, when
        the input cube has a time coordinate and a forecast_reference_time
        coordinate.
        """
        cube = add_forecast_reference_time_and_forecast_period(set_up_cube())
        cube.remove_coord("forecast_period")
        expected_result = (
            cube.coord("time").points -
            cube.coord("forecast_reference_time").points)
        result = Utilities.find_required_lead_times(cube)
        self.assertArrayAlmostEqual(result, expected_result)

    def test_check_forecast_period_unit_conversion(self):
        """
        Test that the data within the numpy array is as expected, when
        the input cube has a forecast_period coordinate with units
        other than the desired units of hours.
        """
        cube = add_forecast_reference_time_and_forecast_period(set_up_cube())
        expected_result = cube.coord("forecast_period").points.copy()
        cube.coord("forecast_period").convert_units("seconds")
        result = Utilities.find_required_lead_times(cube)
        self.assertArrayAlmostEqual(result, expected_result)

    def test_check_time_unit_conversion(self):
        """
        Test that the data within the numpy array is as expected, when
        the input cube has a time coordinate with units
        other than the desired units of hours since 1970-01-01 00:00:00.
        """
        cube = add_forecast_reference_time_and_forecast_period(set_up_cube())
        expected_result = cube.coord("forecast_period").points.copy()
        cube.coord("time").convert_units("seconds since 1970-01-01 00:00:00")
        result = Utilities.find_required_lead_times(cube)
        self.assertArrayAlmostEqual(result, expected_result)

    def test_check_forecast_period_unit_conversion_exception(self):
        """
        Test that an exception is raised, when the input cube has a
        forecast_period coordinate with units that can not be converted
        into hours.
        """
        cube = add_forecast_reference_time_and_forecast_period(set_up_cube())
        cube.coord("forecast_period").units = Unit("Celsius")
        msg = "For forecast_period"
        with self.assertRaisesRegexp(ValueError, msg):
            Utilities.find_required_lead_times(cube)

    def test_check_forecast_reference_time_unit_conversion_exception(self):
        """
        Test that an exception is raised, when the input cube has a
        forecast_reference_time coordinate with units that can not be
        converted into hours.
        """
        cube = add_forecast_reference_time_and_forecast_period(set_up_cube())
        cube.remove_coord("forecast_period")
        cube.coord("forecast_reference_time").units = Unit("Celsius")
        msg = "For time/forecast_reference_time"
        with self.assertRaisesRegexp(ValueError, msg):
            Utilities.find_required_lead_times(cube)

    def test_exception_raised(self):
        """
        Test that a CoordinateNotFoundError exception is raised if the
        forecast_period, or the time and forecast_reference_time,
        are not present.
        """
        cube = set_up_cube()
        msg = "The forecast period coordinate is not available"
        with self.assertRaisesRegexp(CoordinateNotFoundError, msg):
            Utilities.find_required_lead_times(cube)


class Test_adjust_nsize_for_ens(IrisTest):

    """Test adjusting neighbourhood size according to ensemble size."""

    def test_basic_returns_float(self):
        """Test returns float."""
        result = Utilities().adjust_nsize_for_ens(1.0, 3.0, 20.0)
        self.assertIsInstance(result, float)

    def test_returns_unchanged_for_ens1(self):
        """Test returns unchanged value when num_ens = 1.0."""
        result = Utilities().adjust_nsize_for_ens(0.8, 1.0, 20.0)
        self.assertAlmostEqual(result, 20.0)

    def test_returns_adjusted_values(self):
        """Test returns the correct values."""
        result = Utilities().adjust_nsize_for_ens(0.8, 3.0, 20.0)
        self.assertAlmostEqual(result, 9.2376043070399998)


class Test_check_cube_coordinates(IrisTest):

    """Test check_cube_coordinates successfully promotes scalar coordinates to
    dimension coordinates in a new cube if they were dimension coordinates in
    the progenitor cube."""

    def test_basic(self):
        """Test returns iris.cube.Cube."""
        cube = set_up_cube()
        result = Utilities.check_cube_coordinates(cube, cube)
        self.assertIsInstance(result, Cube)

    def test_coord_promotion(self):
        """Test that scalar coordinates in new_cube are promoted to dimension
        coordinates to match the parent cube."""
        cube = set_up_cube()
        new_cube = iris.util.squeeze(cube)
        result = Utilities.check_cube_coordinates(cube, new_cube)
        self.assertEqual(result.dim_coords, cube.dim_coords)

    def test_coord_promotion_only_dim_coords_in_parent(self):
        """Test that only dimension coordinates in the parent cube are matched
        when promoting the scalar coordinates in new_cube. Here realization is
        made into a scalar coordinate on the parent, and so should remain a
        scalar in new_cube as well."""
        cube = set_up_cube()
        new_cube = iris.util.squeeze(cube)
        cube = cube[0]
        result = Utilities.check_cube_coordinates(cube, new_cube)
        self.assertEqual(result.dim_coords, cube.dim_coords)

    def test_coord_promotion_and_reordering(self):
        """Test case in which a scalar coordinate are promoted but the order
        must be corrected to match the progenitor cube."""
        cube = set_up_cube()
        new_cube = iris.util.squeeze(cube)
        cube.transpose(new_order=[1, 0, 2, 3])
        result = Utilities.check_cube_coordinates(cube, new_cube)
        self.assertEqual(result.dim_coords, cube.dim_coords)

    def test_coord_promotion_missing_scalar(self):
        """Test case in which a scalar coordinate has been lost from new_cube,
        meaning the cube undergoing checking ends up with different dimension
        coordinates to the progenitor cube. This raises an error."""
        cube = set_up_cube()
        new_cube = iris.util.squeeze(cube)
        new_cube.remove_coord('realization')
        msg = 'Returned cube dimension coordinates'
        with self.assertRaisesRegexp(iris.exceptions.CoordinateNotFoundError,
                                     msg):
            Utilities.check_cube_coordinates(cube, new_cube)


if __name__ == '__main__':
    unittest.main()
