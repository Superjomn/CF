/*
 * svd.h
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */
#ifndef SVD_H_
#define SVD_H_
#include "../common.h"
#include "../Data.h"
#define K_NUM 50

namespace SVD{

class svd {
private:
    uint max_step;
    double mean;
    float alpha1, alpha2, beta1, beta2;
    float slow_rate;
    float preRMSE, curRMSE;
    void initMean();
    void initBias();
    void initPQ();
    void inline updateBias(UidType uid, ItemType itemI, float eui);
    void inline updatePQ(UidType uid, ItemType itemI, float eui);
    Data data;

public:
    svd(Data &data);
    void init(uint max_step, float alpha1, \
              float alpha2,  float beta1, float beta2); 
    float predict(UidType uid, ItemType mid);
    float evaluate();
    void onestep();
    ~svd();
}; // end class svd

void initModel(uint max_step, float alpha1, float alpha2,  float beta1, float beta2);

};// end namespace svd

#endif /* SVD_H_ */
