/*
 * common.h
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */
#include <iostream>
#include <string>
#include <vector>
#include <math.h>
#include <ostream>
#include <sstream>
#include <algorithm>
#include <fstream>
#include <time.h>
using namespace std;
// 包含数据类型定义等
#ifndef COMMON_H_
#define COMMON_H_

// size of dataset
// TODO change the sizes
#define TRAIN_SIZE 10000
#define TEST_SIZE 10000
#define PREDICT_SIZE 1000

// size of other meta info
#define USER_NUM 9772
#define ITEM_NUM 7899

typedef unsigned int uint;
typedef unsigned short ushort;
typedef unsigned long ulong;

typedef struct Time{
    int day;
    int hour;
    int minute;
    int second;
}Time;

// for trainset ----------------------------------------
typedef struct rateNode
{
    ushort item;
    short rate;
} rateNode;

typedef struct testNode
{
    uint user;
    ushort item;
    short rate;
}testSetNode;

// for predictset
typedef struct predictNode{
    uint user;
    ushort item;
}predictNode;

// functions ------------------------------------------
void show_status(string info, uint cur=0, uint size=0);
float dot(float* p, float* qLocal,int dim);




#endif /* COMMON_H_ */
