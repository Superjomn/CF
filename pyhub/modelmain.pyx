# distutils: language = c++
# distutils: sources = ../common.cpp ../Data.cpp ../models/svd.cpp 

from util cimport *

cdef extern from "../common.h":
    float dot(float p[], float qLocal[],int dim)
    void setRand(float  p[], int dim, float base)

cdef extern from "../Data.h":
    cdef cppclass Data:
        Data()
        void addTrain(UidType uid, ItemType mid, RateType rate)
        void addPredict(UidType uid, ItemType mid)
        void addTest(UidType uid, ItemType mid, RateType rate)
        # Show the info of the content
        void debug()

cdef extern from "../models/svd.h" namespace "SVD":
    cdef cppclass svd:
        svd(Data &data)
        void init(uint max_step, float alpha1, float alpha2,  float beta1, float beta2)
        float predict(UidType uid, ItemType mid)
        float evaluate()
        void onestep()
