/*
 * Data.cpp
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */

#include "Data.h"

Data::Data() {
    // create data
    for (int i=0; i<USER_NUM; ++i)
    {
        testNode tem;
        test_set.push_back(tem);
    }
}

void Data::addTrain(UidType uid, ItemType mid, RateType rate)
{
    rateNode tem = {mid, rate};
    train_set[uid].push_back(tem);
}

void Data::addPredict(UidType uid, ItemType mid)
{
    predictNode tem = {uid, mid};
    predict_set.push_back(tem);
}

void Data::addTest(UidType uid, ItemType mid, RateType rate)
{
    testNode tem = {uid, mid, rate};
    test_set.push_back(tem);
}

void Data::debug()
{
    show_status(".. Info of Data:");
    cout<<">> trainset size:\t"<<train_set.size()<<"\r"<<endl;
    cout<<">> test size:\t"<<test_set.size()<<"\r"<<endl;
    cout<<">> predict size:\t"<<predict_set.size()<<"\r"<<endl;
}


