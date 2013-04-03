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
public:
	svd(Data *data, uint max_step);
    float predict(uint uid, uint mid);
    float evaluate();
    ~svd();
};

};

#endif /* SVD_H_ */
