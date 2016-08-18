# -*- coding: utf-8 -*-
"""
@author: pgrudzinski
"""
import numpy as np

A = np.array(
   [[-2.13534729,
     +3.18324720,
     -1.80143597,
     +0.71727204,
     +0.50344027,
     -0.61899395,
     -0.05332322,
     +0.28021362,
     +0.10715224,
     -0.29302865,
     +0.04459872,
     +0.11868632,
     -0.05248134]])

i_A = np.arange(A.size).reshape(A.shape)

B = np.array(
   [[0.183324722,
     0.240975303,
     0.209108771,
     0.190439972,
     0.142648498,
     0.077993465,
     0.012475611,
    -0.032267127,
    -0.075291522,
    -0.056470670,
     0.076201285,
     0.123893204,
    -0.029201193,
    -0.091173542,
     0.001317696,
     0.026025526]])

i_B = np.arange(B.size).reshape(B.shape)

C = np.array(
   [[2.78157254,
     1.64650916,
    -0.13714390,
    -0.00649767,
    -0.00234444,
     0.00511868,
     0.00187982,
    -0.00204472,
    -0.00046122,
     0.00045724]])

i_C = np.arange(C.size).reshape(C.shape)

D = np.array(
 [[439.9328540,
   472.4180200,
    37.6844940,
     7.4720180,
     2.9208280,
     0.0051840,
    -0.9638640,
    -0.1887320,
     0.1912030,
     0.0490250]])

i_D = np.arange(D.size).reshape(D.shape)


def W_r(T_90):
    T_90 = np.asarray(T_90)
    W_r = np.piecewise(
        T_90,
        [
            T_90 <= 273.16,
            T_90 > 273.16,
        ],
        [
            lambda T:
                np.exp(np.sum(
                    A*((np.log(np.expand_dims(T, -1)/273.16)+1.5)/1.5)**i_A,
                    axis=-1)),
            lambda T:
                np.sum(
                    C*((np.expand_dims(T, -1)-754.15)/481)**i_C,
                    axis=-1),
        ])
    if W_r.size == 1:
        return np.asscalar(W_r)
    else:
        return W_r


def T_90(W_r):
    W_r = np.asarray(W_r)
    T_90 = np.piecewise(
        W_r,
        [
            W_r <= 1,
            W_r > 1,
        ],
        [
            lambda W:
                273.16*np.sum(
                    B*((np.expand_dims(W, -1)**(1/6)-0.65)/0.35)**i_B,
                    axis=-1),
            lambda W:
                273.15+np.sum(
                    D*((np.expand_dims(W, -1)-2.64)/1.64)**i_D,
                    axis=-1),
        ])
    if T_90.size == 1:
        return np.asscalar(T_90)
    else:
        return T_90


class prt(object):

    def __init__(self,
                 R_TPW,
                 a4=0,
                 b4=0,
                 a=0,
                 b=0,
                 c=0,
                 d=0):
        self.R_TPW = R_TPW
        self.a4 = a4
        self.b4 = b4
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def delta_W(self, W):
        W = np.asarray(W)
        delta_W = np.piecewise(
            W,
            [
                W < 1,
                W >= 1,
            ],
            [
                lambda W:
                    self.a4*(W-1) +
                    self.b4*(W-1)*np.log(W),
                lambda W:
                    self.a*(W-1) +
                    self.b*(W-1)**2 +
                    self.c*(W-1)**3 +
                    self.d*(W-W_r(933.473)),  # W_r at Al FP in K
            ]
        )
        if delta_W.size == 1:
            return np.asscalar(delta_W)
        else:
            return delta_W

    def temperature(self, R_T90):
        return T_90(R_T90 / self.R_TPW - self.delta_W(R_T90 / self.R_TPW))

    def resistance(self, T_90):
        W_r_T_90 = W_r(T_90)
        delta_W = 0
        for i in range(3):
            delta_W = self.delta_W(W_r_T_90 + delta_W)
        return self.R_TPW * W_r_T_90 + delta_W
