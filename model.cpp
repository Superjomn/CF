/*
 * model.cpp
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */

#include "model.h"

model::model(Data &data) {
	// TODO Auto-generated constructor stub
	this->data = data;
}

void model::output(string fileName){
    cout<<".. predict data to "<<fileName<<endl;
    ofstream file;
    file.open(fileName.c_str());
    if(! file.is_open()){cout\
        <<".. can't open predict file: "\
        <<fileName<<endl; }
    //write data to file
    unsigned int curItem = -1;
    predictNode *cur;
    float prate;
    for(uint i=0; i<data.predict_set.size(); ++i)
    {
        cur = &(data.predict_set[i]);
        prate = predict(cur->user, cur->item);
        file<<prate<<endl;
    }
    //end write
    file.close();
}


