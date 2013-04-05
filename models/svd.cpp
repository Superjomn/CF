/*
 * svd.cpp
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */

#include "svd.h"
namespace SVD{

float bu[USER_NUM+1] = {0};       
float bi[ITEM_NUM+1] = {0};      

int buNum[USER_NUM+1] = {0};       
int biNum[ITEM_NUM+1] = {0};      

float p[USER_NUM+1][K_NUM+1] = {0};   
float q[ITEM_NUM+1][K_NUM+1] = {0};  
float mean = 0;                      

svd::svd(Data &data) : model(data){
    this->max_step = 0;
    this->alpha1 = 0.0;
    this->alpha2 = 0.0;
    this->beta1 = 0.0;
    this->beta2 = 0.0;
    this->slow_rate = 1;
    this->preRMSE = 1000000.0;
    this->curRMSE = 999999;
}

void svd::init(uint max_step, float alpha1, float alpha2, float beta1, float beta2){
    this->max_step = max_step;
    this->alpha1 = alpha1;
    this->alpha2 = alpha2;
    this->beta1 = beta1;
    this->beta2 = beta2;
    this->slow_rate = 1;
    this->preRMSE = 1000000.0;
    this->curRMSE = 999999;
    initMean();
    initBias();
    initPQ();
}

float svd::predict(uint user, uint item)
{
    int RuNum = data.train_set[user].size(); //the num of items rated by user
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
    vector<testNode>::iterator iter = data.test_set.begin();
    uint testSize = data.test_set.size();
    float prate, err;
    float rmse = 0;
    for(;iter!=data.test_set.end(); ++iter)
    {
        prate = predict(iter->user, iter->item);
        err = prate - iter->rate;
        rmse += err*err;
    }
    rmse = sqrt( rmse/testSize);
    return rmse;
}

void svd::initMean(){
    //calculate the mean
    show_status(".. init mean");
    double sum = 0.0;
    uint num = 0;
    TrainIter train_iter ;
    for(train_iter = data.train_set.begin(); 
        train_iter!=data.train_set.end(); 
        ++train_iter)
    {
        vector<rateNode>::iterator iter;
        for(iter=train_iter->begin(); iter!=train_iter->end(); ++iter){
        	sum += iter->rate;
        	++num;
        }
    }
    mean = sum/num;
}

void svd::initBias(){
    show_status(".. init bias");
}

void svd::initPQ(){
    show_status(".. init PQ");
    for(uint i = 1; i < ITEM_NUM; ++i){
        setRand(q[i],K_NUM,0);   
    }
    
    for(uint i = 1; i < USER_NUM; ++i){
        setRand(p[i], K_NUM,0);
    }
}

void svd::onestep(){
    float pui = 0.0;
    uint n = 0;
    long double rmse = 0.0;
    // scan users
    TrainIter user_set_iter;
    UidType uid = 0;
    for(user_set_iter=data.train_set.begin(); \
        user_set_iter!=data.train_set.end(); \
        ++user_set_iter)
    {
        ++ uid;
        uint RuNum = user_set_iter->size();
        float sqrtRuNum = 0.0;
        if(RuNum>1) sqrtRuNum = (1.0/sqrt(RuNum));
        // scan the items that user rated
        vector<rateNode>::iterator item_set_iter;
        for(item_set_iter=user_set_iter->begin();\
            item_set_iter!=user_set_iter->end();\
            ++item_set_iter)
        {
            ItemType itemI = item_set_iter->item;
            RateType rui = item_set_iter->rate;
            float bui = mean + bu[uid] + bi[itemI];
            pui = predict(uid, itemI);
            float eui = rui - pui;
            rmse += eui * eui; ++n;
            updateBias(uid, itemI, eui);
            updatePQ(uid, itemI, eui);
        }// end item_set_iter
        curRMSE = sqrt( rmse / n );
    } // end uint uid
}

void inline svd::updateBias(UidType uid, ItemType itemI, float eui){
    bu[uid] += alpha1 * (eui - beta1 * bu[uid]);
    bi[itemI] += alpha1 * (eui - beta1 * bi[itemI]);
}

void inline svd::updatePQ(UidType uid, ItemType itemI, float eui){
    for(uint k=1; k< K_NUM+1; ++k) {
        p[uid][k] += \
            alpha2 * (eui*q[itemI][k] - beta2*p[uid][k]);
        q[itemI][k] += \
            alpha2 * (eui*p[uid][k] - beta2*q[itemI][k]);
    }
}

// no member functions


};// end namespace
