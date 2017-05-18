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
"""
Unit tests for the `ensemble_copula_coupling.ResamplePercentiles` class.
"""

class Test__add_bounds_to_percentiles_and_forecast_values(IrisTest):

    """
    Test the _add_bounds_to_percentiles_and_forecast_values method of the
    ResamplePercentiles plugin.
    """

    def setUp(self):
        data = np.tile(np.linspace(5, 10, 9), 3).reshape(3, 1, 3, 3)
        data[0] -= 1
        data[1] += 1
        data[2] += 3
        cube = set_up_cube(data, "air_temperature", "degreesC")
        self.realization_cube = (
            _add_forecast_reference_time_and_forecast_period(cube.copy()))
        cube.coord("realization").rename("percentile")
        cube.coord("percentile").points = np.array([0.1, 0.5, 0.9])
        self.percentile_cube = (
            _add_forecast_reference_time_and_forecast_period(cube))

    def test_basic(self):
        """Test that the plugin returns two numpy arrays."""
        cube = self.percentile_cube
        percentiles = cube.coord("percentile").points
        forecast_at_percentiles = cube.data.reshape(3, 9)
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._add_bounds_to_percentiles_and_forecast_at_percentiles(
            percentiles, forecast_at_percentiles, bounds_pairing)
        self.assertIsInstance(result[0], np.ndarray)
        self.assertIsInstance(result[1], np.ndarray)

    def test_bounds_of_percentiles(self):
        """
        Test that the plugin returns the expected results for the
        percentiles, where they've been padded with the values from
        the bounds_pairing.
        """
        cube = self.percentile_cube
        percentiles = cube.coord("percentile").points
        forecast_at_percentiles = cube.data.reshape(3, 9)
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._add_bounds_to_percentiles_and_forecast_at_percentiles(
            percentiles, forecast_at_percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result[0][0], bounds_pairing[0])
        self.assertArrayAlmostEqual(result[0][-1], bounds_pairing[1])

    def test_probability_data(self):
        """
        Test that the plugin returns the expected results for the
        probabilities, where they've been padded with zeros and ones to
        represent the extreme ends of the Cumulative Distribution Function.
        """
        cube = self.percentile_cube
        percentiles = cube.coord("percentile").points
        forecast_at_percentiles = cube.data.reshape(3, 9)
        zero_array = np.zeros(forecast_at_percentiles[:, 0].shape)
        one_array = np.ones(forecast_at_percentiles[:, 0].shape)
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._add_bounds_to_percentiles_and_forecast_at_percentiles(
            percentiles, forecast_at_percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result[1][:, 0], zero_array)
        self.assertArrayAlmostEqual(result[1][:, -1], one_array)

    def test_endpoints_of_distribution_exceeded(self):
        """
        Test that the plugin raises a ValueError when the constant
        end points of the distribution are exceeded by a threshold value
        used in the forecast.
        """
        forecast_at_percentiles = np.array([[0.05, 0.7, 0.95]])
        percentiles = np.array([8, 10, 60])
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        msg = "The end points added to the threshold values for"
        with self.assertRaisesRegexp(ValueError, msg):
            plugin._add_bounds_to_percentiles_and_forecast_at_percentiles(
                percentiles, forecast_at_percentiles, bounds_pairing)


class Test__sample_percentiles(IrisTest):

    """
    Test the _sample_percentiles method of the ResamplePercentiles plugin.
    """

    def setUp(self):
        data = np.tile(np.linspace(5, 10, 9), 3).reshape(3, 1, 3, 3)
        data[0] -= 1
        data[1] += 1
        data[2] += 3
        cube = set_up_cube(data, "air_temperature", "degreesC")
        self.realization_cube = (
            _add_forecast_reference_time_and_forecast_period(cube.copy()))
        cube.coord("realization").rename("percentile")
        self.percentile_cube = (
            _add_forecast_reference_time_and_forecast_period(cube))

    def test_basic(self):
        """Test that the plugin returns an Iris.cube.Cube."""
        cube = self.current_temperature_forecast_cube
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        self.assertIsInstance(result, Cube)

    def test_simple_check_data(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values for the percentiles.

        The input cube contains probabilities greater than a given threshold.
        """
        expected = np.array([8.15384615, 9.38461538, 11.6])
        expected = expected[:, np.newaxis, np.newaxis, np.newaxis]

        data = np.array([0.95, 0.3, 0.05])
        data = data[:, np.newaxis, np.newaxis, np.newaxis]

        self.current_temperature_forecast_cube = (
            _add_forecast_reference_time_and_forecast_period(
                set_up_cube(
                    data, "air_temperature", "1",
                    forecast_thresholds=[8, 10, 12], y_dimension_length=1,
                    x_dimension_length=1)))
        cube = self.current_temperature_forecast_cube
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result.data, expected)

    def test_probabilities_not_monotonically_increasing(self):
        """
        Test that the plugin raises a ValueError when the probabilities
        of the Cumulative Distribution Function are not monotonically
        increasing.
        """
        data = np.array([0.05, 0.7, 0.95])
        data = data[:, np.newaxis, np.newaxis, np.newaxis]

        self.current_temperature_forecast_cube = (
            _add_forecast_reference_time_and_forecast_period(
                set_up_cube(
                    data, "air_temperature", "1",
                    forecast_thresholds=[8, 10, 12], y_dimension_length=1,
                    x_dimension_length=1)))
        cube = self.current_temperature_forecast_cube
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        msg = "The probability values used to construct the"
        with self.assertRaisesRegexp(ValueError, msg):
            plugin._probabilities_to_percentiles(
                cube, percentiles, bounds_pairing)

    def test_result_cube_has_no_probability_above_threshold_coordinate(self):
        """
        Test that the plugin returns a cube with coordinates that
        do not include the probability_above_threshold coordinate.
        """
        cube = self.current_temperature_forecast_cube
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        for coord in result.coords():
            self.assertNotEqual(coord.name(), "probability_above_threshold")

    def test_check_data(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values for the percentiles.
        """
        data = np.array([[[[15.8, 31., 46.2],
                           [8., 10., 31.],
                           [10.4, 12., 42.4]]],
                         [[[-16., 10, 31.],
                           [8., 10., 11.6],
                           [-30.4, 8., 12.]]],
                         [[[-30.4, 8., 11.],
                           [-34., -10., 9],
                           [-35.2, -16., 3.2]]]])

        cube = self.current_temperature_forecast_cube
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result.data, data)

    def test_check_single_threshold(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values for the percentiles, if a single threshold is used for
        constructing the percentiles.
        """
        data = np.array([[[[12.2, 29., 45.8],
                           [8., 26.66666667, 45.33333333],
                           [12.2, 29., 45.8]]],
                         [[[-16., 23.75, 44.75],
                           [8., 26.66666667, 45.33333333],
                           [-30.4, 8., 41.6]]],
                         [[[-30.4, 8., 41.6],
                           [-34., -10., 29.],
                           [-35.2, -16., 3.2]]]])

        for acube in self.current_temperature_forecast_cube.slices_over(
                "probability_above_threshold"):
            cube = acube
            break
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result.data, data)

    def test_lots_of_probability_thresholds(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values for the percentiles, if there are lots of thresholds.
        """
        input_probs_1d = np.linspace(1, 0, 30)
        input_probs = np.tile(input_probs_1d, (3, 3, 1, 1)).T

        data = np.array([[[[2.9, 14.5, 26.1],
                           [2.9, 14.5, 26.1],
                           [2.9, 14.5, 26.1]]],
                         [[[2.9, 14.5, 26.1],
                           [2.9, 14.5, 26.1],
                           [2.9, 14.5, 26.1]]],
                         [[[2.9, 14.5, 26.1],
                           [2.9, 14.5, 26.1],
                           [2.9, 14.5, 26.1]]]])

        temperature_values = np.arange(0, 30)
        cube = (
            _add_forecast_reference_time_and_forecast_period(
                set_up_cube(input_probs, "air_temperature", "1",
                            forecast_thresholds=temperature_values)))
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result.data, data)

    def test_lots_of_percentiles(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values for the percentiles, if lots of percentile values are
        requested.
        """
        data = np.array([[[[13.9, 15.8, 17.7],
                           [19.6, 21.5, 23.4],
                           [25.3, 27.2, 29.1]]],
                         [[[31., 32.9, 34.8],
                           [36.7, 38.6, 40.5],
                           [42.4, 44.3, 46.2]]],
                         [[[48.1, -16., 8.],
                           [8.25, 8.5, 8.75],
                           [9., 9.25, 9.5]]],
                         [[[9.75, 10., 10.33333333],
                           [10.66666667, 11., 11.33333333],
                           [11.66666667, 12., 21.5]]],
                         [[[31., 40.5, 10.2],
                           [10.4, 10.6, 10.8],
                           [11., 11.2, 11.4]]],
                         [[[11.6, 11.8, 12.],
                           [15.8, 19.6, 23.4],
                           [27.2, 31., 34.8]]],
                         [[[38.6, 42.4, 46.2],
                           [-28., -16., -4.],
                           [8., 8.33333333, 8.66666667]]],
                         [[[9., 9.33333333, 9.66666667],
                           [10., 10.33333333, 10.66666667],
                           [11., 11.33333333, 11.66666667]]],
                         [[[12., 21.5, 31.],
                           [40.5, -16., 8.],
                           [8.25, 8.5, 8.75]]],
                         [[[9., 9.25, 9.5],
                           [9.75, 10., 10.2],
                           [10.4, 10.6, 10.8]]],
                         [[[11., 11.2, 11.4],
                           [11.6, 11.8, -35.2],
                           [-30.4, -25.6, -20.8]]],
                         [[[-16., -11.2, -6.4],
                           [-1.6, 3.2, 8.],
                           [8.5, 9., 9.5]]],
                         [[[10., 10.5, 11.],
                           [11.5, 12., 31.],
                           [-35.2, -30.4, -25.6]]],
                         [[[-20.8, -16., -11.2],
                           [-6.4, -1.6, 3.2],
                           [8., 8.33333333, 8.66666667]]],
                         [[[9., 9.33333333, 9.66666667],
                           [10., 10.5, 11.],
                           [11.5, -37., -34.]]],
                         [[[-31., -28., -25.],
                           [-22., -19., -16.],
                           [-13., -10., -7.]]],
                         [[[-4., -1., 2.],
                           [5., 8., 8.5],
                           [9., 9.5, -37.6]]],
                         [[[-35.2, -32.8, -30.4],
                           [-28., -25.6, -23.2],
                           [-20.8, -18.4, -16.]]],
                         [[[-13.6, -11.2, -8.8],
                           [-6.4, -4., -1.6],
                           [0.8, 3.2, 5.6]]]])
        cube = self.current_temperature_forecast_cube
        percentiles = np.arange(0.05, 1.0, 0.05)
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result.data, data)

    def test_check_data_spot_forecasts(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values for the percentiles for spot forecasts.
        """
        data = np.array([[[15.8, 31., 46.2,
                           8., 10., 31.,
                           10.4, 12., 42.4]],
                         [[-16., 10, 31.,
                           8., 10., 11.6,
                           -30.4, 8., 12.]],
                         [[-30.4, 8., 11.,
                           -34., -10., 9,
                           -35.2, -16., 3.2]]])
        cube = self.current_temperature_spot_forecast_cube
        percentiles = [0.1, 0.5, 0.9]
        bounds_pairing = (-40, 50)
        plugin = Plugin()
        result = plugin._probabilities_to_percentiles(
            cube, percentiles, bounds_pairing)
        self.assertArrayAlmostEqual(result.data, data)


class Test_process(IrisTest):

    """Test the process plugin of the Resample Percentiles plugin."""

    def setUp(self):
        data = np.tile(np.linspace(5, 10, 9), 3).reshape(3, 1, 3, 3)
        data[0] -= 1
        data[1] += 1
        data[2] += 3
        cube = set_up_cube(data, "air_temperature", "degreesC")
        self.realization_cube = (
            _add_forecast_reference_time_and_forecast_period(cube.copy()))
        cube.coord("realization").rename("percentile")
        self.percentile_cube = (
            _add_forecast_reference_time_and_forecast_period(cube))

    def test_check_data_specifying_percentiles(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values for a specific number of percentiles.
        """
        data = np.array([[[[21.5, 31., 40.5],
                           [8.75, 10., 11.66666667],
                           [11., 12., 31.]]],
                         [[[8.33333333, 10., 11.66666667],
                           [8.75, 10., 11.],
                           [-16., 8., 10.5]]],
                         [[[-16., 8., 9.66666667],
                           [-25., -10., 5.],
                           [-28., -16., -4.]]]])

        cube = self.percentile_cube
        percentiles = [0.25, 0.5, 0.75]
        plugin = Plugin()
        result = plugin.process(
            cube, no_of_percentiles=len(percentiles))
        self.assertArrayAlmostEqual(result.data, data)

    def test_check_data_not_specifying_percentiles(self):
        """
        Test that the plugin returns an Iris.cube.Cube with the expected
        data values without specifying the number of percentiles.
        """
        data = np.array([[[[21.5, 31., 40.5],
                           [8.75, 10., 11.66666667],
                           [11., 12., 31.]]],
                         [[[8.33333333, 10., 11.66666667],
                           [8.75, 10., 11.],
                           [-16., 8., 10.5]]],
                         [[[-16., 8., 9.66666667],
                           [-25., -10., 5.],
                           [-28., -16., -4.]]]])

        cube = self.percentile_cube
        plugin = Plugin()
        result = plugin.process(cube)
        self.assertArrayAlmostEqual(result.data, data)

