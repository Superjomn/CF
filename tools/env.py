# -*- coding: utf-8 -*-
from __future__ import division
import os 
import time

TRAINSET_LINE_NUM = 1262741
# train_set 数据
TRAINSET_LINES = 1262741
USER_NUM = 9722
MOVIE_NUM = 7899
TAG_NUM = 1129
MEAN = 3.6775887

K_NUM = 64

def Path(path):
    base_path = r'../datasets/'
    return os.path.join(base_path, path)

training_path = Path('training_set.txt')
predict_path = Path('predict.txt')
movie_tag_path = Path('movie_tag.txt')
user_history_path = Path('user_history.txt')
user_social_path = Path('user_social.txt')

# new id 和 old id 的对应关系
userids_path = Path('userids_corrs.txt')
movieids_path = Path('movieids_corrs.txt')
tagids_path = Path('tagids_corrs.txt')


def show_status(info, cur=None, total=None):
    """
    args:
        info: show info
        cur: if cur is None, then only show info

    usage:
        show_status('status: ', 1, 10)
        show_status('finish parser!')
    """
    if cur is None:
        print "%s\t%s\r" % (str(info), str(time.ctime()))
        return
    step = int(total / 10)
    if cur % step == 0:
        status = cur/total
        print "%s\t%s\t%s\r" % (info, status, time.ctime())

def transed_path(key):
    def trans(path):
        basename = os.path.splitext(path)
        return basename[0] + '_new.txt'
    dic = {
        'train': training_path,
        'predict': predict_path,
        'tag': movie_tag_path,
        'history': user_history_path,
        'social': user_social_path,
    }
    return trans(dic[key])
