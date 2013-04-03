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
#include "../model.h"
#define K_NUM 50

namespace svd{

class svd : public model{
private:
    uint max_step;
    double mean;
    float alpha1, alpha2, beta1, beta2;
    float slow_rate;
    float preRMSE, curRMSE;
    void initMean();
    void initBias();
    void initPQ();
public:
	svd(Data *data, uint max_step);
    void init(float alpha1, float alpha2, \
              float beta1, float beta2);
    float predict(uint uid, uint mid);
    float evaluate();
    void onestep();
    void inline svd::updateBias(UidType uid, ItemType itemI, float eui);
    void inline svd::updatePQ(UidType uid, ItemType itemI, float eui);
    ~svd();
};

};

#endif /* SVD_H_ */
