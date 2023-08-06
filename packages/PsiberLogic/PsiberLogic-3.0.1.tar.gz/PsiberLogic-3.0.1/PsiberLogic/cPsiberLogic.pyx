# -*- coding: utf-8 -*-
"""
.pyx file for PsiberLogic
==================================================================================================
Copyright (C) 2017  Psibernetix Inc.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
==================================================================================================
Created by:  Dr. Nick Ernest, Psibernetix Inc. CEO

Current Version: 3.0.0

Dates:      Action taken:
6/2/2015    Created
7/13/2015   Modified and finalized Version 1.0.0
7/16/2015   Minor fixes making Version 1.0.1-1.1.2
7/23/2015   Replaced numpy Trapezoidal rule call with efficient cython code, removed len() calls
10/5/2015   Fixed major memory issue of Mamdani functions, speed optimization in
                Controller, and minor typos.  Released version 2.0.1.  Documentation fixes
				for version 2.0.2
10/26/2015  Fixed bug for one-input systems requiring calls to the FIS to be a confusing tuple of
                (InputValue, NullValue).
01/18/2017  Updated build with new Cython syntax, minor optimizations, version 3.0.0 - 3.0.1
"""

# Cython global compiler directives
#!python
#cython: Language_Level=3, boundscheck=False, wraparound=False, cdivision=True, initializedcheck=False

import cython
import numpy as np
cimport numpy as np

cdef extern from "math.h":
    double max (double x, double y)
    double min (double x, double y)

#==================================================================================================
# Fuzzy Controller
#==================================================================================================
# The Mamdani controller class.  See DEMOTipFIS as an example for creating
cdef class Controller(object):

    # Type all objects
    cdef:
        list _RuleBase
        np.ndarray _OutputRange, FuzzyOutput
        object _Defuzzify

    def __init__(self, np.ndarray[dtype=np.double_t, ndim = 1] OutputRange,
                 object Deffuzification):
        self._OutputRange = OutputRange
        self._RuleBase = []
        self._Defuzzify = Deffuzification

    # Add a rule to the RuleBase
    cpdef AddRule(self, tuple InRule):

        # Type variables
        cdef:
            object NewRule
            object InputMembershipFunctions
            object OutputMembershipFunctions

        InputMembershipFunctions, OutputMembershipFunctions = InRule
        NewRule = (InputMembershipFunctions, OutputMembershipFunctions(self._OutputRange))
        self._RuleBase.append(NewRule)

    # Evaluates one rule
    cdef EvaluateRule(self, tuple Rule, object InputVariables):

        # Type all objects
        cdef:
            int MembershipIndex
            list MembershipList = []
            object InputMembershipFunctions
            double Input
            object MembershipFunc
            np.ndarray[dtype=double, ndim=1] OutputMembershipFunctions
            double AndMembership = 0

        InputMembershipFunctions, OutputMembershipFunctions = Rule

        # If we're looking at multiple inputs (remember, must be input as tuple!)
        if isinstance(InputMembershipFunctions, tuple):
            # For each combination of input MFs and input variables, determine membership value
            for MembershipFunc, Input in zip(InputMembershipFunctions, InputVariables):
                if MembershipFunc is not None:
                    if type(Input) == float:
                        MembershipList.append(np.double(MembershipFunc(np.array([Input]))))
                    else:
                        MembershipList.append(np.double(MembershipFunc(Input)))

            # Calculate the combined "and" membership
            for MembershipIndex in range(len(MembershipList)-1):
                if MembershipIndex == 0:
                    AndMembership =  ZadehAnd(MembershipList[0], MembershipList[MembershipIndex+1])
                else:
                    AndMembership = ZadehAnd(AndMembership, MembershipList[MembershipIndex+1])

            # Returns membership value associated to the condition and the result of the implication
            if AndMembership == 0.0:
                return 0.0, np.array([0], dtype=np.double)
            else:
                return AndMembership, MamdaniImplication(AndMembership, OutputMembershipFunctions)

        # If this is a single-input system (re-use typed "AndMembership" for speed's sake)
        else:
            if type(InputVariables) == float:
                AndMembership = np.double(InputMembershipFunctions(np.array([InputVariables])))
            else:
                AndMembership = np.double(InputMembershipFunctions(InputVariables))

            if AndMembership == 0.0:
                return 0.0, np.array([0], dtype=np.double)
            else:
                return AndMembership, MamdaniImplication(AndMembership, OutputMembershipFunctions)

    # Evaluate all rules
    cdef EvaluateAll(self, object InputVariables):

        # Type all objects
        cdef:
            double Membership
            np.ndarray[dtype=double, ndim=1] FuzzyOutput
            np.ndarray[dtype=double, ndim=1] ImplicationResult
            tuple Rule

        # Initialize FuzzyOutput
        FuzzyOutput = np.zeros(self._OutputRange.shape[0],dtype=np.double)

        # For each rule
        for Rule in self._RuleBase:
            Membership, ImplicationResult = self.EvaluateRule(Rule, InputVariables)
            if Membership != 0.0:
                FuzzyOutput = MamdaniAglutination(FuzzyOutput, ImplicationResult)
        return FuzzyOutput

    def __call__(self, object InputVariables):
        FuzzyOutput = self.EvaluateAll(InputVariables)
        return self._Defuzzify(FuzzyOutput, self._OutputRange)

#==================================================================================================
# Membership Functions
#==================================================================================================
# Base membership function class that all specific functions extend
cdef class MembershipFunction(object):

    # Type all objects
    cdef object _Function

    def __init__(self, object Function):
        self._Function = np.vectorize(Function)

    def __call__(self, np.ndarray Input):
        return np.array(self._Function(Input))

# Effectively a triangular membership function with the midpoint = to the low endpoint
cdef class DecreasingRamp(MembershipFunction):

    # Type all objects
    cdef:
        double _LowEndpoint, _HighEndpoint, _DownSlope

    def __init__(self, double LowEndpoint, double HighEndpoint):
        self._LowEndpoint = LowEndpoint
        self._HighEndpoint = HighEndpoint
        self._DownSlope = 1.0 / (self._HighEndpoint - self._LowEndpoint)

    def __call__(self, np.ndarray[dtype=double, ndim = 1] Input):
        cdef:
            int InputIndex
            np.ndarray[dtype=double, ndim = 1] Membership = np.zeros(Input.shape[0],
                                                                     dtype=np.double)
        # for each input value, calculate membership value
        for InputIndex in range(Input.shape[0]):
            # for Input in
            if Input[InputIndex] < self._LowEndpoint:
                Membership[InputIndex] = 1.0
            elif Input[InputIndex] < self._HighEndpoint:
                Membership[InputIndex] = self._DownSlope * (self._HighEndpoint - Input[InputIndex])
            else:
                Membership[InputIndex] = 0.0

        return Membership

# Effectively a triangular membership function with the midpoint = to the high endpoint
cdef class IncreasingRamp(MembershipFunction):

    # Type all objects
    cdef double _LowEndpoint, _HighEndpoint, _UpSlope

    def __init__(self, double LowEndpoint, double HighEndpoint):
        self._LowEndpoint = LowEndpoint
        self._HighEndpoint = HighEndpoint
        self._UpSlope = 1.0 / (self._HighEndpoint - self._LowEndpoint)

    def __call__(self, np.ndarray[dtype=double, ndim = 1] Input):

        # Type all objects
        cdef:
            int InputIndex
            np.ndarray[dtype=double, ndim = 1] Membership = np.zeros(Input.shape[0],
                                                                           dtype=np.double)
        # for each input value, calculate membership value
        for InputIndex in range(Input.shape[0]):
            if Input[InputIndex] < self._LowEndpoint:
                Membership[InputIndex] = 0.0
            elif Input[InputIndex] < self._HighEndpoint:
                Membership[InputIndex] = self._UpSlope * (Input[InputIndex]- self._LowEndpoint)
            else:
                Membership[InputIndex] = 1.0

        return Membership

# Triangular membership function defined by 3 points
cdef class Triangle(MembershipFunction):

    # Type all objects
    cdef double _LowEndpoint, _Midpoint, _HighEndpoint, _DownSlope, _UpSlope

    def __init__(self, double LowEndpoint, double Midpoint, double HighEndpoint):
        self._LowEndpoint = LowEndpoint
        self._Midpoint = Midpoint
        self._HighEndpoint = HighEndpoint
        self._UpSlope = 1.0 / (self._Midpoint - self._LowEndpoint)
        self._DownSlope = 1.0 / (self._HighEndpoint - self._Midpoint)

    def __call__(self, np.ndarray[dtype=double, ndim = 1] Input):

        # Type all objects
        cdef:
            int InputIndex
            np.ndarray[dtype=double, ndim = 1] Membership = np.zeros(Input.shape[0],
                                                                     dtype=np.double)
        # for each input value, calculate membership value
        for InputIndex in range(Input.shape[0]):
            if Input[InputIndex] < self._LowEndpoint:
                Membership[InputIndex] = 0.0
            elif Input[InputIndex] < self._Midpoint:
                Membership[InputIndex] = self._UpSlope * (Input[InputIndex] - self._LowEndpoint)
            elif Input[InputIndex] < self._HighEndpoint:
                Membership[InputIndex] = self._DownSlope * (self._HighEndpoint - Input[InputIndex])
            else:
                Membership[InputIndex] = 0.0

        return Membership

#==================================================================================================
# Defuzzifcation Methods
#==================================================================================================
# Standard centroid defuzzification method using trapezoidal rule for areas
cpdef double Centroid(np.ndarray[dtype=double, ndim = 1] Memberships,
                      np.ndarray[dtype=double, ndim = 1] OutputArray):
    cdef:
        double AreaSum1 = 0
        double AreaSum2 = 0
        double OutputStep = OutputArray[1]-OutputArray[0]
        int Index

    for Index in range(Memberships.shape[0]-1):
        AreaSum1 += OutputStep * ((Memberships[Index] + Memberships[Index+1]) / 2)
        AreaSum2 += OutputStep * ((Memberships[Index] * OutputArray[Index] +
                                   Memberships[Index+1] * OutputArray[Index+1]) / 2)

    return AreaSum2 / AreaSum1

# Standard bisector defuzzification method using trapezoidal rule for areas
cpdef double Bisector(np.ndarray[dtype=double, ndim = 1] Memberships,
                      np.ndarray[dtype=double, ndim = 1] OutputArray):
    # Type all objects
    cdef:
        double DividedArea
        double OutputStep = OutputArray[1]-OutputArray[0]
        double HalfArea = 0
        int AreaIterator
        int Index

    # determines the area that the bisector should have
    for Index in range(Memberships.shape[0]-1):
        HalfArea += OutputStep * ((Memberships[Index] + Memberships[Index+1]) / 2)
    # Make HalfArea truly half the total area
    HalfArea /= 2

    AreaIterator = 0
    # current output's area
    DivdedArea = 0.0
    while DivdedArea < HalfArea:
        AreaIterator += 1
        DivdedArea += 0.5 * (Memberships[AreaIterator] + Memberships[AreaIterator-1])*OutputStep
    return OutputArray[AreaIterator]

# Standard smallest of maxima defuzzification method
cpdef double SmallestOfMaxima(np.ndarray[dtype=double, ndim = 1] Memberships,
                              np.ndarray[dtype=double, ndim = 1] OutputArray):

    return OutputArray[np.argmax(Memberships)]

#==================================================================================================
# Utilities
#==================================================================================================
# Zadeh "and" operator used throughout
cdef double ZadehAnd(double x, double y):
    return min(x, y)

# Mamdani implication operator used throughout
cdef np.ndarray[dtype=double, ndim=1] MamdaniImplication(double x,
                                                         np.ndarray[dtype=double, ndim=1] y):
    # Type all objects
    cdef:
        int Index
        # This indeed copies
        np.ndarray[dtype=double, ndim=1] Output = np.zeros((len(y)))

    # Equivalent to np.minimum
    for Index in range(y.shape[0]):
        Output[Index] = min(x, y[Index])

    return Output

# Mamdani aglutination operator used throughout
cdef np.ndarray[dtype=double,ndim=1] MamdaniAglutination(np.ndarray[dtype=double, ndim=1] x,
                                                         np.ndarray[dtype=double, ndim=1] y):
    # Type all objects
    cdef:
        int Index
        np.ndarray[dtype=double, ndim=1] Output = np.zeros((len(y)))

    # Equivalent to np.maximum
    for Index in range(y.shape[0]):
        Output[Index] = max(x[Index], y[Index])

    return Output
