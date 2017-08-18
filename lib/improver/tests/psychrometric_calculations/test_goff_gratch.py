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

"""Using the unit testing framework to look at the comparative performance of
three saturation vapour pressure algorithms against a precalculated data table"""

from iris.cube import Cube
from iris.tests import IrisTest
from iris.coords import DimCoord
from iris.coord_systems import GeogCS
from iris.fileformats.pp import EARTH_RADIUS
import numpy as np
from cf_units import Unit

DATA = np.array([0.966483e-02,0.984279e-02,0.100240e-01,0.102082e-01,0.103957e-01, 
0.105865e-01,0.107803e-01,0.109777e-01,0.111784e-01,0.113825e-01, 
0.115902e-01,0.118016e-01,0.120164e-01,0.122348e-01,0.124572e-01, 
0.126831e-01,0.129132e-01,0.131470e-01,0.133846e-01,0.136264e-01, 
0.138724e-01,0.141225e-01,0.143771e-01,0.146356e-01,0.148985e-01, 
0.151661e-01,0.154379e-01,0.157145e-01,0.159958e-01,0.162817e-01, 
0.165725e-01,0.168680e-01,0.171684e-01,0.174742e-01,0.177847e-01, 
0.181008e-01,0.184216e-01,0.187481e-01,0.190801e-01,0.194175e-01, 
0.197608e-01,0.201094e-01,0.204637e-01,0.208242e-01,0.211906e-01, 
0.215631e-01,0.219416e-01,0.223263e-01,0.227172e-01,0.231146e-01, 
0.235188e-01,0.239296e-01,0.243465e-01,0.247708e-01,0.252019e-01, 
0.256405e-01,0.260857e-01,0.265385e-01,0.269979e-01,0.274656e-01, 
0.279405e-01,0.284232e-01,0.289142e-01,0.294124e-01,0.299192e-01, 
0.304341e-01,0.309571e-01,0.314886e-01,0.320285e-01,0.325769e-01, 
0.331348e-01,0.337014e-01,0.342771e-01,0.348618e-01,0.354557e-01, 
0.360598e-01,0.366727e-01,0.372958e-01,0.379289e-01,0.385717e-01, 
0.392248e-01,0.398889e-01,0.405633e-01,0.412474e-01,0.419430e-01, 
0.426505e-01,0.433678e-01,0.440974e-01,0.448374e-01,0.455896e-01, 
0.463545e-01,0.471303e-01,0.479191e-01,0.487190e-01,0.495322e-01,
0.503591e-01,0.511977e-01,0.520490e-01,0.529145e-01,0.537931e-01, 
0.546854e-01,0.555924e-01,0.565119e-01,0.574467e-01,0.583959e-01, 
0.593592e-01,0.603387e-01,0.613316e-01,0.623409e-01,0.633655e-01, 
0.644053e-01,0.654624e-01,0.665358e-01,0.676233e-01,0.687302e-01, 
0.698524e-01,0.709929e-01,0.721490e-01,0.733238e-01,0.745180e-01, 
0.757281e-01,0.769578e-01,0.782061e-01,0.794728e-01,0.807583e-01, 
0.820647e-01,0.833905e-01,0.847358e-01,0.861028e-01,0.874882e-01, 
0.888957e-01,0.903243e-01,0.917736e-01,0.932464e-01,0.947407e-01, 
0.962571e-01,0.977955e-01,0.993584e-01,0.100942e+00,0.102551e+00, 
0.104186e+00,0.105842e+00,0.107524e+00,0.109231e+00,0.110963e+00, 
0.112722e+00,0.114506e+00,0.116317e+00,0.118153e+00,0.120019e+00, 
0.121911e+00,0.123831e+00,0.125778e+00,0.127755e+00,0.129761e+00, 
0.131796e+00,0.133863e+00,0.135956e+00,0.138082e+00,0.140241e+00, 
0.142428e+00,0.144649e+00,0.146902e+00,0.149190e+00,0.151506e+00, 
0.153859e+00,0.156245e+00,0.158669e+00,0.161126e+00,0.163618e+00, 
0.166145e+00,0.168711e+00,0.171313e+00,0.173951e+00,0.176626e+00, 
0.179342e+00,0.182096e+00,0.184893e+00,0.187724e+00,0.190600e+00, 
0.193518e+00,0.196473e+00,0.199474e+00,0.202516e+00,0.205604e+00, 
0.208730e+00,0.211905e+00,0.215127e+00,0.218389e+00,0.221701e+00,
0.225063e+00,0.228466e+00,0.231920e+00,0.235421e+00,0.238976e+00, 
0.242580e+00,0.246232e+00,0.249933e+00,0.253691e+00,0.257499e+00, 
0.261359e+00,0.265278e+00,0.269249e+00,0.273274e+00,0.277358e+00, 
0.281498e+00,0.285694e+00,0.289952e+00,0.294268e+00,0.298641e+00, 
0.303078e+00,0.307577e+00,0.312135e+00,0.316753e+00,0.321440e+00, 
0.326196e+00,0.331009e+00,0.335893e+00,0.340842e+00,0.345863e+00, 
0.350951e+00,0.356106e+00,0.361337e+00,0.366636e+00,0.372006e+00, 
0.377447e+00,0.382966e+00,0.388567e+00,0.394233e+00,0.399981e+00, 
0.405806e+00,0.411714e+00,0.417699e+00,0.423772e+00,0.429914e+00, 
0.436145e+00,0.442468e+00,0.448862e+00,0.455359e+00,0.461930e+00, 
0.468596e+00,0.475348e+00,0.482186e+00,0.489124e+00,0.496160e+00, 
0.503278e+00,0.510497e+00,0.517808e+00,0.525224e+00,0.532737e+00, 
0.540355e+00,0.548059e+00,0.555886e+00,0.563797e+00,0.571825e+00, 
0.579952e+00,0.588198e+00,0.596545e+00,0.605000e+00,0.613572e+00, 
0.622255e+00,0.631059e+00,0.639962e+00,0.649003e+00,0.658144e+00, 
0.667414e+00,0.676815e+00,0.686317e+00,0.695956e+00,0.705728e+00, 
0.715622e+00,0.725641e+00,0.735799e+00,0.746082e+00,0.756495e+00, 
0.767052e+00,0.777741e+00,0.788576e+00,0.799549e+00,0.810656e+00, 
0.821914e+00,0.833314e+00,0.844854e+00,0.856555e+00,0.868415e+00,
0.880404e+00,0.892575e+00,0.904877e+00,0.917350e+00,0.929974e+00, 
0.942771e+00,0.955724e+00,0.968837e+00,0.982127e+00,0.995600e+00, 
0.100921e+01,0.102304e+01,0.103700e+01,0.105116e+01,0.106549e+01, 
0.108002e+01,0.109471e+01,0.110962e+01,0.112469e+01,0.113995e+01, 
0.115542e+01,0.117107e+01,0.118693e+01,0.120298e+01,0.121923e+01, 
0.123569e+01,0.125234e+01,0.126923e+01,0.128631e+01,0.130362e+01, 
0.132114e+01,0.133887e+01,0.135683e+01,0.137500e+01,0.139342e+01, 
0.141205e+01,0.143091e+01,0.145000e+01,0.146933e+01,0.148892e+01, 
0.150874e+01,0.152881e+01,0.154912e+01,0.156970e+01,0.159049e+01, 
0.161159e+01,0.163293e+01,0.165452e+01,0.167640e+01,0.169852e+01, 
0.172091e+01,0.174359e+01,0.176653e+01,0.178977e+01,0.181332e+01, 
0.183709e+01,0.186119e+01,0.188559e+01,0.191028e+01,0.193524e+01, 
0.196054e+01,0.198616e+01,0.201208e+01,0.203829e+01,0.206485e+01, 
0.209170e+01,0.211885e+01,0.214637e+01,0.217424e+01,0.220242e+01, 
0.223092e+01,0.225979e+01,0.228899e+01,0.231855e+01,0.234845e+01, 
0.237874e+01,0.240937e+01,0.244040e+01,0.247176e+01,0.250349e+01, 
0.253560e+01,0.256814e+01,0.260099e+01,0.263431e+01,0.266800e+01, 
0.270207e+01,0.273656e+01,0.277145e+01,0.280671e+01,0.284248e+01, 
0.287859e+01,0.291516e+01,0.295219e+01,0.298962e+01,0.302746e+01,
0.306579e+01,0.310454e+01,0.314377e+01,0.318351e+01,0.322360e+01, 
0.326427e+01,0.330538e+01,0.334694e+01,0.338894e+01,0.343155e+01, 
0.347456e+01,0.351809e+01,0.356216e+01,0.360673e+01,0.365184e+01, 
0.369744e+01,0.374352e+01,0.379018e+01,0.383743e+01,0.388518e+01, 
0.393344e+01,0.398230e+01,0.403177e+01,0.408175e+01,0.413229e+01, 
0.418343e+01,0.423514e+01,0.428746e+01,0.434034e+01,0.439389e+01, 
0.444808e+01,0.450276e+01,0.455820e+01,0.461423e+01,0.467084e+01, 
0.472816e+01,0.478607e+01,0.484468e+01,0.490393e+01,0.496389e+01, 
0.502446e+01,0.508580e+01,0.514776e+01,0.521047e+01,0.527385e+01, 
0.533798e+01,0.540279e+01,0.546838e+01,0.553466e+01,0.560173e+01, 
0.566949e+01,0.573807e+01,0.580750e+01,0.587749e+01,0.594846e+01, 
0.602017e+01,0.609260e+01,0.616591e+01,0.623995e+01,0.631490e+01, 
0.639061e+01,0.646723e+01,0.654477e+01,0.662293e+01,0.670220e+01, 
0.678227e+01,0.686313e+01,0.694495e+01,0.702777e+01,0.711142e+01, 
0.719592e+01,0.728140e+01,0.736790e+01,0.745527e+01,0.754352e+01, 
0.763298e+01,0.772316e+01,0.781442e+01,0.790676e+01,0.800001e+01, 
0.809435e+01,0.818967e+01,0.828606e+01,0.838343e+01,0.848194e+01, 
0.858144e+01,0.868207e+01,0.878392e+01,0.888673e+01,0.899060e+01, 
0.909567e+01,0.920172e+01,0.930909e+01,0.941765e+01,0.952730e+01,
0.963821e+01,0.975022e+01,0.986352e+01,0.997793e+01,0.100937e+02, 
0.102105e+02,0.103287e+02,0.104481e+02,0.105688e+02,0.106909e+02, 
0.108143e+02,0.109387e+02,0.110647e+02,0.111921e+02,0.113207e+02, 
0.114508e+02,0.115821e+02,0.117149e+02,0.118490e+02,0.119847e+02, 
0.121216e+02,0.122601e+02,0.124002e+02,0.125416e+02,0.126846e+02, 
0.128290e+02,0.129747e+02,0.131224e+02,0.132712e+02,0.134220e+02, 
0.135742e+02,0.137278e+02,0.138831e+02,0.140403e+02,0.141989e+02, 
0.143589e+02,0.145211e+02,0.146845e+02,0.148501e+02,0.150172e+02, 
0.151858e+02,0.153564e+02,0.155288e+02,0.157029e+02,0.158786e+02, 
0.160562e+02,0.162358e+02,0.164174e+02,0.166004e+02,0.167858e+02, 
0.169728e+02,0.171620e+02,0.173528e+02,0.175455e+02,0.177406e+02, 
0.179372e+02,0.181363e+02,0.183372e+02,0.185400e+02,0.187453e+02, 
0.189523e+02,0.191613e+02,0.193728e+02,0.195866e+02,0.198024e+02, 
0.200200e+02,0.202401e+02,0.204626e+02,0.206871e+02,0.209140e+02, 
0.211430e+02,0.213744e+02,0.216085e+02,0.218446e+02,0.220828e+02, 
0.223241e+02,0.225671e+02,0.228132e+02,0.230615e+02,0.233120e+02, 
0.235651e+02,0.238211e+02,0.240794e+02,0.243404e+02,0.246042e+02, 
0.248704e+02,0.251390e+02,0.254109e+02,0.256847e+02,0.259620e+02, 
0.262418e+02,0.265240e+02,0.268092e+02,0.270975e+02,0.273883e+02,
0.276822e+02,0.279792e+02,0.282789e+02,0.285812e+02,0.288867e+02, 
0.291954e+02,0.295075e+02,0.298222e+02,0.301398e+02,0.304606e+02, 
0.307848e+02,0.311119e+02,0.314424e+02,0.317763e+02,0.321133e+02, 
0.324536e+02,0.327971e+02,0.331440e+02,0.334940e+02,0.338475e+02, 
0.342050e+02,0.345654e+02,0.349295e+02,0.352975e+02,0.356687e+02, 
0.360430e+02,0.364221e+02,0.368042e+02,0.371896e+02,0.375790e+02, 
0.379725e+02,0.383692e+02,0.387702e+02,0.391744e+02,0.395839e+02, 
0.399958e+02,0.404118e+02,0.408325e+02,0.412574e+02,0.416858e+02, 
0.421188e+02,0.425551e+02,0.429962e+02,0.434407e+02,0.438910e+02, 
0.443439e+02,0.448024e+02,0.452648e+02,0.457308e+02,0.462018e+02, 
0.466775e+02,0.471582e+02,0.476428e+02,0.481313e+02,0.486249e+02, 
0.491235e+02,0.496272e+02,0.501349e+02,0.506479e+02,0.511652e+02, 
0.516876e+02,0.522142e+02,0.527474e+02,0.532836e+02,0.538266e+02, 
0.543737e+02,0.549254e+02,0.554839e+02,0.560456e+02,0.566142e+02, 
0.571872e+02,0.577662e+02,0.583498e+02,0.589392e+02,0.595347e+02, 
0.601346e+02,0.607410e+02,0.613519e+02,0.619689e+02,0.625922e+02, 
0.632204e+02,0.638550e+02,0.644959e+02,0.651418e+02,0.657942e+02, 
0.664516e+02,0.671158e+02,0.677864e+02,0.684624e+02,0.691451e+02, 
0.698345e+02,0.705293e+02,0.712312e+02,0.719398e+02,0.726542e+02,
0.733754e+02,0.741022e+02,0.748363e+02,0.755777e+02,0.763247e+02, 
0.770791e+02,0.778394e+02,0.786088e+02,0.793824e+02,0.801653e+02, 
0.809542e+02,0.817509e+02,0.825536e+02,0.833643e+02,0.841828e+02, 
0.850076e+02,0.858405e+02,0.866797e+02,0.875289e+02,0.883827e+02, 
0.892467e+02,0.901172e+02,0.909962e+02,0.918818e+02,0.927760e+02, 
0.936790e+02,0.945887e+02,0.955071e+02,0.964346e+02,0.973689e+02, 
0.983123e+02,0.992648e+02,0.100224e+03,0.101193e+03,0.102169e+03, 
0.103155e+03,0.104150e+03,0.105152e+03,0.106164e+03,0.107186e+03, 
0.108217e+03,0.109256e+03,0.110303e+03,0.111362e+03,0.112429e+03, 
0.113503e+03,0.114588e+03,0.115684e+03,0.116789e+03,0.117903e+03, 
0.119028e+03,0.120160e+03,0.121306e+03,0.122460e+03,0.123623e+03, 
0.124796e+03,0.125981e+03,0.127174e+03,0.128381e+03,0.129594e+03, 
0.130822e+03,0.132058e+03,0.133306e+03,0.134563e+03,0.135828e+03, 
0.137109e+03,0.138402e+03,0.139700e+03,0.141017e+03,0.142338e+03, 
0.143676e+03,0.145025e+03,0.146382e+03,0.147753e+03,0.149133e+03, 
0.150529e+03,0.151935e+03,0.153351e+03,0.154783e+03,0.156222e+03, 
0.157678e+03,0.159148e+03,0.160624e+03,0.162117e+03,0.163621e+03, 
0.165142e+03,0.166674e+03,0.168212e+03,0.169772e+03,0.171340e+03, 
0.172921e+03,0.174522e+03,0.176129e+03,0.177755e+03,0.179388e+03,
0.181040e+03,0.182707e+03,0.184382e+03,0.186076e+03,0.187782e+03, 
0.189503e+03,0.191240e+03,0.192989e+03,0.194758e+03,0.196535e+03, 
0.198332e+03,0.200141e+03,0.201963e+03,0.203805e+03,0.205656e+03, 
0.207532e+03,0.209416e+03,0.211317e+03,0.213236e+03,0.215167e+03, 
0.217121e+03,0.219087e+03,0.221067e+03,0.223064e+03,0.225080e+03, 
0.227113e+03,0.229160e+03,0.231221e+03,0.233305e+03,0.235403e+03, 
0.237520e+03,0.239655e+03,0.241805e+03,0.243979e+03,0.246163e+03, 
0.248365e+03,0.250593e+03,0.252830e+03,0.255093e+03,0.257364e+03, 
0.259667e+03,0.261979e+03,0.264312e+03,0.266666e+03,0.269034e+03, 
0.271430e+03,0.273841e+03,0.276268e+03,0.278722e+03,0.281185e+03, 
0.283677e+03,0.286190e+03,0.288714e+03,0.291266e+03,0.293834e+03, 
0.296431e+03,0.299045e+03,0.301676e+03,0.304329e+03,0.307006e+03, 
0.309706e+03,0.312423e+03,0.315165e+03,0.317930e+03,0.320705e+03, 
0.323519e+03,0.326350e+03,0.329199e+03,0.332073e+03,0.334973e+03, 
0.337897e+03,0.340839e+03,0.343800e+03,0.346794e+03,0.349806e+03, 
0.352845e+03,0.355918e+03,0.358994e+03,0.362112e+03,0.365242e+03, 
0.368407e+03,0.371599e+03,0.374802e+03,0.378042e+03,0.381293e+03, 
0.384588e+03,0.387904e+03,0.391239e+03,0.394604e+03,0.397988e+03, 
0.401411e+03,0.404862e+03,0.408326e+03,0.411829e+03,0.415352e+03,
0.418906e+03,0.422490e+03,0.426095e+03,0.429740e+03,0.433398e+03, 
0.437097e+03,0.440827e+03,0.444570e+03,0.448354e+03,0.452160e+03, 
0.455999e+03,0.459870e+03,0.463765e+03,0.467702e+03,0.471652e+03, 
0.475646e+03,0.479674e+03,0.483715e+03,0.487811e+03,0.491911e+03, 
0.496065e+03,0.500244e+03,0.504448e+03,0.508698e+03,0.512961e+03, 
0.517282e+03,0.521617e+03,0.525989e+03,0.530397e+03,0.534831e+03, 
0.539313e+03,0.543821e+03,0.548355e+03,0.552938e+03,0.557549e+03, 
0.562197e+03,0.566884e+03,0.571598e+03,0.576351e+03,0.581131e+03, 
0.585963e+03,0.590835e+03,0.595722e+03,0.600663e+03,0.605631e+03, 
0.610641e+03,0.615151e+03,0.619625e+03,0.624140e+03,0.628671e+03, 
0.633243e+03,0.637845e+03,0.642465e+03,0.647126e+03,0.651806e+03, 
0.656527e+03,0.661279e+03,0.666049e+03,0.670861e+03,0.675692e+03, 
0.680566e+03,0.685471e+03,0.690396e+03,0.695363e+03,0.700350e+03, 
0.705381e+03,0.710444e+03,0.715527e+03,0.720654e+03,0.725801e+03, 
0.730994e+03,0.736219e+03,0.741465e+03,0.746756e+03,0.752068e+03, 
0.757426e+03,0.762819e+03,0.768231e+03,0.773692e+03,0.779172e+03, 
0.784701e+03,0.790265e+03,0.795849e+03,0.801483e+03,0.807137e+03, 
0.812842e+03,0.818582e+03,0.824343e+03,0.830153e+03,0.835987e+03, 
0.841871e+03,0.847791e+03,0.853733e+03,0.859727e+03,0.865743e+03,
0.871812e+03,0.877918e+03,0.884046e+03,0.890228e+03,0.896433e+03, 
0.902690e+03,0.908987e+03,0.915307e+03,0.921681e+03,0.928078e+03, 
0.934531e+03,0.941023e+03,0.947539e+03,0.954112e+03,0.960708e+03, 
0.967361e+03,0.974053e+03,0.980771e+03,0.987545e+03,0.994345e+03, 
0.100120e+04,0.100810e+04,0.101502e+04,0.102201e+04,0.102902e+04, 
0.103608e+04,0.104320e+04,0.105033e+04,0.105753e+04,0.106475e+04, 
0.107204e+04,0.107936e+04,0.108672e+04,0.109414e+04,0.110158e+04, 
0.110908e+04,0.111663e+04,0.112421e+04,0.113185e+04,0.113952e+04, 
0.114725e+04,0.115503e+04,0.116284e+04,0.117071e+04,0.117861e+04, 
0.118658e+04,0.119459e+04,0.120264e+04,0.121074e+04,0.121888e+04, 
0.122709e+04,0.123534e+04,0.124362e+04,0.125198e+04,0.126036e+04, 
0.126881e+04,0.127731e+04,0.128584e+04,0.129444e+04,0.130307e+04, 
0.131177e+04,0.132053e+04,0.132931e+04,0.133817e+04,0.134705e+04, 
0.135602e+04,0.136503e+04,0.137407e+04,0.138319e+04,0.139234e+04, 
0.140156e+04,0.141084e+04,0.142015e+04,0.142954e+04,0.143896e+04, 
0.144845e+04,0.145800e+04,0.146759e+04,0.147725e+04,0.148694e+04, 
0.149672e+04,0.150655e+04,0.151641e+04,0.152635e+04,0.153633e+04, 
0.154639e+04,0.155650e+04,0.156665e+04,0.157688e+04,0.158715e+04, 
0.159750e+04,0.160791e+04,0.161836e+04,0.162888e+04,0.163945e+04, 
0.165010e+04,0.166081e+04,0.167155e+04,0.168238e+04,0.169325e+04, 
0.170420e+04,0.171522e+04,0.172627e+04,0.173741e+04,0.174859e+04, 
0.175986e+04,0.177119e+04,0.178256e+04,0.179402e+04,0.180552e+04, 
0.181711e+04,0.182877e+04,0.184046e+04,0.185224e+04,0.186407e+04, 
0.187599e+04,0.188797e+04,0.190000e+04,0.191212e+04,0.192428e+04, 
0.193653e+04,0.194886e+04,0.196122e+04,0.197368e+04,0.198618e+04, 
0.199878e+04,0.201145e+04,0.202416e+04,0.203698e+04,0.204983e+04, 
0.206278e+04,0.207580e+04,0.208887e+04,0.210204e+04,0.211525e+04, 
0.212856e+04,0.214195e+04,0.215538e+04,0.216892e+04,0.218249e+04, 
0.219618e+04,0.220994e+04,0.222375e+04,0.223766e+04,0.225161e+04, 
0.226567e+04,0.227981e+04,0.229399e+04,0.230829e+04,0.232263e+04, 
0.233708e+04,0.235161e+04,0.236618e+04,0.238087e+04,0.239560e+04, 
0.241044e+04,0.242538e+04,0.244035e+04,0.245544e+04,0.247057e+04, 
0.248583e+04,0.250116e+04,0.251654e+04,0.253204e+04,0.254759e+04, 
0.256325e+04,0.257901e+04,0.259480e+04,0.261073e+04,0.262670e+04, 
0.264279e+04,0.265896e+04,0.267519e+04,0.269154e+04,0.270794e+04, 
0.272447e+04,0.274108e+04,0.275774e+04,0.277453e+04,0.279137e+04, 
0.280834e+04,0.282540e+04,0.284251e+04,0.285975e+04,0.287704e+04, 
0.289446e+04,0.291198e+04,0.292954e+04,0.294725e+04,0.296499e+04,  
0.298288e+04,0.300087e+04,0.301890e+04,0.303707e+04,0.305529e+04, 
0.307365e+04,0.309211e+04,0.311062e+04,0.312927e+04,0.314798e+04, 
0.316682e+04,0.318577e+04,0.320477e+04,0.322391e+04,0.324310e+04, 
0.326245e+04,0.328189e+04,0.330138e+04,0.332103e+04,0.334073e+04, 
0.336058e+04,0.338053e+04,0.340054e+04,0.342069e+04,0.344090e+04, 
0.346127e+04,0.348174e+04,0.350227e+04,0.352295e+04,0.354369e+04, 
0.356458e+04,0.358559e+04,0.360664e+04,0.362787e+04,0.364914e+04, 
0.367058e+04,0.369212e+04,0.371373e+04,0.373548e+04,0.375731e+04, 
0.377929e+04,0.380139e+04,0.382355e+04,0.384588e+04,0.386826e+04, 
0.389081e+04,0.391348e+04,0.393620e+04,0.395910e+04,0.398205e+04, 
0.400518e+04,0.402843e+04,0.405173e+04,0.407520e+04,0.409875e+04, 
0.412246e+04,0.414630e+04,0.417019e+04,0.419427e+04,0.421840e+04, 
0.424272e+04,0.426715e+04,0.429165e+04,0.431634e+04,0.434108e+04, 
0.436602e+04,0.439107e+04,0.441618e+04,0.444149e+04,0.446685e+04, 
0.449241e+04,0.451810e+04,0.454385e+04,0.456977e+04,0.459578e+04, 
0.462197e+04,0.464830e+04,0.467468e+04,0.470127e+04,0.472792e+04, 
0.475477e+04,0.478175e+04,0.480880e+04,0.483605e+04,0.486336e+04, 
0.489087e+04,0.491853e+04,0.494623e+04,0.497415e+04,0.500215e+04, 
0.503034e+04,0.505867e+04,0.508707e+04,0.511568e+04,0.514436e+04,   
0.517325e+04,0.520227e+04,0.523137e+04,0.526068e+04,0.529005e+04, 
0.531965e+04,0.534939e+04,0.537921e+04,0.540923e+04,0.543932e+04, 
0.546965e+04,0.550011e+04,0.553064e+04,0.556139e+04,0.559223e+04, 
0.562329e+04,0.565449e+04,0.568577e+04,0.571727e+04,0.574884e+04, 
0.578064e+04,0.581261e+04,0.584464e+04,0.587692e+04,0.590924e+04, 
0.594182e+04,0.597455e+04,0.600736e+04,0.604039e+04,0.607350e+04, 
0.610685e+04,0.614036e+04,0.617394e+04,0.620777e+04,0.624169e+04, 
0.627584e+04,0.631014e+04,0.634454e+04,0.637918e+04,0.641390e+04, 
0.644887e+04,0.648400e+04,0.651919e+04,0.655467e+04,0.659021e+04, 
0.662599e+04,0.666197e+04,0.669800e+04,0.673429e+04,0.677069e+04, 
0.680735e+04,0.684415e+04,0.688104e+04,0.691819e+04,0.695543e+04, 
0.699292e+04,0.703061e+04,0.706837e+04,0.710639e+04,0.714451e+04, 
0.718289e+04,0.722143e+04,0.726009e+04,0.729903e+04,0.733802e+04, 
0.737729e+04,0.741676e+04,0.745631e+04,0.749612e+04,0.753602e+04, 
0.757622e+04,0.761659e+04,0.765705e+04,0.769780e+04,0.773863e+04, 
0.777975e+04,0.782106e+04,0.786246e+04,0.790412e+04,0.794593e+04, 
0.798802e+04,0.803028e+04,0.807259e+04,0.811525e+04,0.815798e+04, 
0.820102e+04,0.824427e+04,0.828757e+04,0.833120e+04,0.837493e+04, 
0.841895e+04,0.846313e+04,0.850744e+04,0.855208e+04,0.859678e+04,
0.864179e+04,0.868705e+04,0.873237e+04,0.877800e+04,0.882374e+04, 
0.886979e+04,0.891603e+04,0.896237e+04,0.900904e+04,0.905579e+04, 
0.910288e+04,0.915018e+04,0.919758e+04,0.924529e+04,0.929310e+04, 
0.934122e+04,0.938959e+04,0.943804e+04,0.948687e+04,0.953575e+04, 
0.958494e+04,0.963442e+04,0.968395e+04,0.973384e+04,0.978383e+04, 
0.983412e+04,0.988468e+04,0.993534e+04,0.998630e+04,0.100374e+05, 
0.100888e+05,0.101406e+05,0.101923e+05,0.102444e+05,0.102966e+05, 
0.103492e+05,0.104020e+05,0.104550e+05,0.105082e+05,0.105616e+05, 
0.106153e+05,0.106693e+05,0.107234e+05,0.107779e+05,0.108325e+05, 
0.108874e+05,0.109425e+05,0.109978e+05,0.110535e+05,0.111092e+05, 
0.111653e+05,0.112217e+05,0.112782e+05,0.113350e+05,0.113920e+05, 
0.114493e+05,0.115070e+05,0.115646e+05,0.116228e+05,0.116809e+05, 
0.117396e+05,0.117984e+05,0.118574e+05,0.119167e+05,0.119762e+05, 
0.120360e+05,0.120962e+05,0.121564e+05,0.122170e+05,0.122778e+05, 
0.123389e+05,0.124004e+05,0.124619e+05,0.125238e+05,0.125859e+05, 
0.126484e+05,0.127111e+05,0.127739e+05,0.128372e+05,0.129006e+05, 
0.129644e+05,0.130285e+05,0.130927e+05,0.131573e+05,0.132220e+05, 
0.132872e+05,0.133526e+05,0.134182e+05,0.134842e+05,0.135503e+05, 
0.136168e+05,0.136836e+05,0.137505e+05,0.138180e+05,0.138854e+05,
0.139534e+05,0.140216e+05,0.140900e+05,0.141588e+05,0.142277e+05, 
0.142971e+05,0.143668e+05,0.144366e+05,0.145069e+05,0.145773e+05, 
0.146481e+05,0.147192e+05,0.147905e+05,0.148622e+05,0.149341e+05, 
0.150064e+05,0.150790e+05,0.151517e+05,0.152250e+05,0.152983e+05, 
0.153721e+05,0.154462e+05,0.155205e+05,0.155952e+05,0.156701e+05, 
0.157454e+05,0.158211e+05,0.158969e+05,0.159732e+05,0.160496e+05, 
0.161265e+05,0.162037e+05,0.162811e+05,0.163589e+05,0.164369e+05, 
0.165154e+05,0.165942e+05,0.166732e+05,0.167526e+05,0.168322e+05, 
0.169123e+05,0.169927e+05,0.170733e+05,0.171543e+05,0.172356e+05, 
0.173173e+05,0.173993e+05,0.174815e+05,0.175643e+05,0.176471e+05, 
0.177305e+05,0.178143e+05,0.178981e+05,0.179826e+05,0.180671e+05, 
0.181522e+05,0.182377e+05,0.183232e+05,0.184093e+05,0.184955e+05, 
0.185823e+05,0.186695e+05,0.187568e+05,0.188447e+05,0.189326e+05, 
0.190212e+05,0.191101e+05,0.191991e+05,0.192887e+05,0.193785e+05, 
0.194688e+05,0.195595e+05,0.196503e+05,0.197417e+05,0.198332e+05, 
0.199253e+05,0.200178e+05,0.201105e+05,0.202036e+05,0.202971e+05, 
0.203910e+05,0.204853e+05,0.205798e+05,0.206749e+05,0.207701e+05, 
0.208659e+05,0.209621e+05,0.210584e+05,0.211554e+05,0.212524e+05, 
0.213501e+05,0.214482e+05,0.215465e+05,0.216452e+05,0.217442e+05,
0.218439e+05,0.219439e+05,0.220440e+05,0.221449e+05,0.222457e+05, 
0.223473e+05,0.224494e+05,0.225514e+05,0.226542e+05,0.227571e+05, 
0.228606e+05,0.229646e+05,0.230687e+05,0.231734e+05,0.232783e+05, 
0.233839e+05,0.234898e+05,0.235960e+05,0.237027e+05,0.238097e+05, 
0.239173e+05,0.240254e+05,0.241335e+05,0.242424e+05,0.243514e+05, 
0.244611e+05,0.245712e+05,0.246814e+05,0.247923e+05,0.249034e+05, 
0.250152e+05,0.250152e+05])

from improver.psychrometric_calculations import (
    saturation_vapour_pressure_goff_gratch,
    saturation_vapour_pressure_ashrae,
    saturation_vapour_pressure_simple,
    )


def _make_test_cube(long_name, units, data=None):
    """
    Make a basic cube to run tests on
    """    
    gg_min = 183.05
    gg_max = 338.25
    cs = GeogCS(EARTH_RADIUS)
    if data is None:
        data = np.arange(gg_min, gg_max, 0.1)

    cube = Cube(data, long_name=long_name)
    x_coord = DimCoord(np.linspace(-45.0, 45.0, len(data)), 'latitude',
                       units='degrees', coord_system=cs)
    cube.add_dim_coord(x_coord, 0)
    cube.units = Unit(units)
    return cube


class Test_calculate_svp(IrisTest):
    """saturation_vapour_press == svp"""
    def test_basic(self):
        """test to check that the saturation_vapour_pressure
        method returns a cube with answers calculated to be correct
        """
        cube_in = _make_test_cube("temperature", "K")
        pressure = cube_in.copy(data=np.full(cube_in.shape, 1000.))
        pressure.units = Unit('hPa')
        print pressure
        resultgg = saturation_vapour_pressure_goff_gratch(cube_in, pressure)
        resultcx = saturation_vapour_pressure_ashrae(_make_test_cube("temperature", "K"))
        resultsi = saturation_vapour_pressure_simple(_make_test_cube("temperature", "K"))


        print "{:>7}  {:>12}  {:>12}  {:>12}  {:>12}".format("T (C)", "UM","Goff-Gratch","ASRAE","Simple")
        for i in range(0,1549,50):
            print "{:7} {:12.6f}  {:12.6f}  {:12.6f}  {:12.6f}".format(cube_in[i].data, DATA[i], resultgg.data[i], resultcx.data[i], resultsi.data[i])

        #data = data - result.data

        #self.assertAlmostEqual(result.data[0][0], expected_data, places=3)
        #self.assertEqual(result.units, Unit('Pa'))

  
