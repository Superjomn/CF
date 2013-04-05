/*
 * model.h
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */

#ifndef MODEL_H_
#define MODEL_H_

#include "common.h"
#include "Data.h"
/*
 * add as many methods to python core.
 */

class model {
protected:
	Data data;
public:
	model(Data& data);
    virtual float predict(uint uid, uint mid);
    // evaluate using testset and return final RMSE
    virtual float evaluate();
	// put predictions to file
	void output(string filename);
    virtual void onestep();
	virtual ~model();
};

#endif /* MODEL_H_ */
