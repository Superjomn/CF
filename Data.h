/*
 * Data.h
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */

#ifndef DATA_H_
#define DATA_H_
#include <iostream>
#include <vector>
#include "common.h"
using namespace std;

typedef vector < vector < rateNode> >::iterator TrainIter;
typedef vector<testNode>::iterator TestIter;
typedef vector<predictNode>::iterator PredictIter;

class Data {
public:
    vector<testNode> test_set;
    vector<predictNode> predict_set;
    vector < vector < rateNode> > train_set;
	Data();
    // add data
    void addTrain(uint uid, uint mid, short rate);
    void addPredict(uint uid, uint mid);
    void addTest(uint uid, uint mid, short rate);
	// Show the info of the content
	void debug();
};

#endif /* DATA_H_ */
