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

. $IMPROVER_DIR/tests/lib/utils

@test "weighted-blending --linear coordinate input output y0val slope" {
  TEST_DIR=$(mktemp -d)
  improver_check_skip_acceptance

  # Run weighted blending with linear weights and suboptions: y0val and slope. Check it passes.
  run improver weighted-blending 'linear' 'time' --y0val 4.0 --slope -2.0 \
      "$IMPROVER_ACC_TEST_DIR/weighted_blending/basic_lin/multiple_probabilities_rain_*H.nc" \
      "$TEST_DIR/output.nc"
  [[ "$status" -eq 0 ]]

  # Run nccmp to compare the output and kgo.
  improver_compare_output "$TEST_DIR/output.nc" \
      "$IMPROVER_ACC_TEST_DIR/weighted_blending/options_lin/kgo.nc"
  rm "$TEST_DIR/output.nc"
  rmdir "$TEST_DIR"
}


@test "weighted-blending --linear coordinate input output y0val ynval" {
  TEST_DIR=$(mktemp -d)
  improver_check_skip_acceptance

  # Run weighted blending with linear weights and suboptions: y0val and ynval. Check it passes.
  run improver weighted-blending 'linear' 'time' --y0val 4.0 --ynval 0.0 \
      "$IMPROVER_ACC_TEST_DIR/weighted_blending/basic_lin/multiple_probabilities_rain_*H.nc" \
      "$TEST_DIR/output.nc"
  [[ "$status" -eq 0 ]]

  # Run nccmp to compare the output and kgo.
  improver_compare_output "$TEST_DIR/output.nc" \
      "$IMPROVER_ACC_TEST_DIR/weighted_blending/options_lin/kgo.nc"
  rm "$TEST_DIR/output.nc"
  rmdir "$TEST_DIR"
}
