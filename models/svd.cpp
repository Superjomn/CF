/*
 * svd.cpp
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */

#include "svd.h"
namespace svd{

float bu[USER_NUM+1] = {0};       
float bi[ITEM_NUM+1] = {0};      

int buNum[USER_NUM+1] = {0};       
int biNum[ITEM_NUM+1] = {0};      

float p[USER_NUM+1][K_NUM+1] = {0};   
float q[ITEM_NUM+1][K_NUM+1] = {0};  
float mean = 0;                      

svd::svd(Data *data, uint max_step) : model(data){
    this->max_step = max_step;
}

float svd::predict(uint user, uint item)
{
    int RuNum = data->train_set[user].size(); //the num of items rated by user
    float ret; 
    if(RuNum > 1) {
        ret = mean + bu[user] + bi[item] +  dot(p[user],q[item],K_NUM);
    }
    else ret  = mean+bu[user] + bi[item];
    if(ret < 1.0) ret = 1;
    if(ret > 5.0) ret = 5;
    return ret;
}

float svd::evaluate(){
    vector<testNode>::iterator iter = data->test_set.begin();
    uint testSize = data->test_set.size();
    float prate, err;
    float rmse = 0;
    for(;iter!=data->test_set.end(); ++iter)
    {
        prate = predict(iter->user, iter->item);
        err = prate - iter->rate;
        rmse += err*err;
    }
    rmse = sqrt( rmse/testSize);
    return rmse;
}


};
