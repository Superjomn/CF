/*
 * common.cpp
 *
 *  Created on: 2013-4-2
 *      Author: chunwei
 */
#include "common.h"

Time inline curtime(){
    const time_t t = time(NULL);
    /*本地时间：日期，时间 年月日，星期，时分秒*/
    struct tm* current_time = localtime(&t);
    Time time = {
                current_time->tm_mday,
                current_time->tm_hour,
                current_time->tm_min,
                current_time->tm_sec};
    return time;
}

void show_status(string info, uint cur, uint size)
{
    if (size == 0){
        cout<<info<<endl;
        return;
    }
    uint gap = size/10;
    if (cur%gap == 0){
        Time time = curtime();
        cout<<info<<"\t"<<float(cur)/size<<"\t"\
            <<time.hour<<" "\
            <<time.minute<<" "\
            <<time.second<<"\r"<<endl;
    }
}

