#!/usr/bin/env bats
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

@test "continuous-snowfall-level -h" {
  run improver continuous-snow-falling-level -h
  [[ "$status" -eq 0 ]]
  read -d '' expected <<'__HELP__' || true
usage: improver-continuous-snow-falling-level [-h]
                                              [--precison NEWTON_PRECISION]
                                              [--falling_level_threshold FALLING_LEVEL_THRESHOLD]
                                              TEMPERATURE RELATIVE_HUMIDITY
                                              PRESSURE OROGRAPHY OUTPUT_FILE

Calculate the continuous falling snow level

positional arguments:
  TEMPERATURE           File path to a cube of air temperatures at heights (m)
                        at the points for which the continuous falling snow
                        level is being calculated.
  RELATIVE_HUMIDITY     File path to a cube of relative_humidities at heights
                        (m) at the points for which the continuous falling
                        snow level is being calculated.
  PRESSURE              File path to a cube of air pressures at heights (m) at
                        the points for which the continuous falling snow level
                        is being calculated.
  OROGRAPHY             A path to an input NetCDF file containing a cube with
                        the orography in m of the terrain that the continuous
                        falling snow level is beingcalculated.
  OUTPUT_FILE           The output path for the processed NetCDF

optional arguments:
  -h, --help            show this help message and exit
  --precison NEWTON_PRECISION
                        Precision to which the wet bulb temperature is
                        required: This is used by the Newton iteration default
                        value is 0.0005
  --falling_level_threshold FALLING_LEVEL_THRESHOLD
                        Cutoff threshold for the wet-bulb integral used to
                        calculate the falling snow level. Default Value is
                        90.0

__HELP__
  [[ "$output" == "$expected" ]]
}