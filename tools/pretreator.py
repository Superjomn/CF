#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import env
import os.path as P
import numpy as np
from utils import *

# 将离散的movieID和userID转成连续序列
# 保存old id 和 new id之间的对应关系
# 将会重写数据集合

from sets import Set

class IdDetector(object):
    """
    取得离散的userid movieid列表并排序
    """
    def __init__(self):
        self.trainset_ph = env.training_path
        self.tag_path = env.movie_tag_path
        self.userids = Set()
        self.movieids = Set()
        self.tagids = Set()
        # output 
        self.userids_path = env.userids_path 
        self.movieids_path = env.movieids_path 
        self.tagids_path = env.tagids_path

    def __call__(self):
        self.detect_ids()
        env.show_status('.. finish detecting all ids')
        self.sort_ids()
        env.show_status('.. finish sorting')
        self.tofile()
        env.show_status('.. save data to file OK!')
        env.show_status('.. finish transid !')

    def detect_tags(self):
        env.show_status(".. detecting tag ids")
        with open(self.tag_path) as f:
            for l in f.readlines():
                ls = l.split()
                tagids = ls[1].split(',')
                for tid in tagids:
                    self.tagids.add(int(tid))

    def detect_ids(self):
        self.detect_tags()
        for i, line in enumerate(self.data):
            uid, mid, score = line.split()
            self.userids.add(int(uid))
            self.movieids.add(int(mid))
            self.show_status(i)

    def sort_ids(self):
        def sort(_set):
            _list = list(_set)
            _list.sort()
            return _list
        self.userids = sort(self.userids)
        self.movieids = sort(self.movieids)
        self.tagids = sort(self.tagids)

    def tofile(self):
        def tofile(_list, path):
            with open(path, 'w') as f:
                res = ''
                for l in [str(s) for s in _list]:
                    res += l + '\n'
                f.write(res)
        tofile(self.userids, self.userids_path)
        tofile(self.movieids, self.movieids_path)
        tofile(self.tagids, self.tagids_path)

    def show_status(self, index):
        env.show_status("detecting ", index, env.TRAINSET_LINE_NUM)

    @property
    def data(self):
        self.fp = open(self.trainset_ph)
        return self.fp.readlines()


class IdTransfer(object):
    """
    利用IdDetector的结果对数据集中id进行重写
    对
        trainset.txt
        predict.txt
    进行id重写
    """
    def __init__(self):
        self.out_trainset_path = env.transed_path('train')
        self.out_predict_path = env.transed_path('predict')
        self.out_user_history_path = env.transed_path('history')
        self.userids = None
        self.movieids = None
        self.tagids = None

    def __call__(self):
        self.loadids()
        env.show_status(".. finished load ids")
        self.trans()
        env.show_status(".. finished trans id")

    def loadids(self):
        def loadids(path):
            with open(path) as f:
                _list = [int(l.strip()) for l in f.readlines()]
                return np.asarray(_list)
                return _list
        self.userids = loadids(env.userids_path)
        self.movieids = loadids(env.movieids_path)
        self.tagids = loadids(env.tagids_path)

    def trans(self):
        def trans(inpath, outpath):
            res = []
            with open(inpath) as f:
                for l in f.readlines():
                    ls = l.split()
                    uid, mid = ls[:2]
                    uid = np.searchsorted(self.userids, int(uid))
                    mid = np.searchsorted(self.movieids, int(mid))
                    if len(ls) == 3:
                        # train_set
                        nline = '%d\t%d\t%s\r\n' % (uid, mid, ls[2])
                    else:
                        nline = '%d\t%d\r\n' % (uid, mid)
                    res.append(nline)
            res = ''.join(res)
            with open(outpath, 'w') as f:
                f.write(res)
        """
        trans(env.training_path, self.out_trainset_path)
        env.show_status("finished trans train_set")
        trans(env.predict_path, self.out_predict_path)
        env.show_status("finished trans predict")
        trans(env.user_history_path, self.out_user_history_path)
        env.show_status("finished trans userhistory")
        """
        
        def trans_tags(inpath, outpath, key1, key2):
            """
            trans user_social, movie_tags

            format:
                uid fid fid fid
            """
            id_dict = {
                'uid': self.userids,
                'mid': self.movieids,
                'tid': self.tagids,
            }
            touch_file(outpath)
            with open(outpath, 'a') as out_f:
                with open(inpath) as f:
                    for l in f.readlines():
                        _id, tags = l.split()
                        tags = tags.split(',')
                        _id = np.searchsorted(id_dict[key1], int(_id))
                        tags = [np.searchsorted(id_dict[key2], int(i)) for i in tags]
                        tags = [str(i) for i in tags]
                        tem = str(_id) + ' ' + ' '.join(tags) + '\n'
                        out_f.write(tem)

        env.show_status('.. trans user social')
        trans_tags(env.user_social_path, env.transed_path('social'), 'uid', 'uid')
        env.show_status('.. trans movie tags')
        trans_tags(env.movie_tag_path, env.transed_path('tag'), 'mid', 'tid')


def pretreator():
    if not P.exists(env.userids_path) and \
            P.exists(env.movieids_path) and P.exists(env.tagids_path):
        IdDetector()()
    idtransfer = IdTransfer()
    idtransfer()

if __name__ == '__main__':
    pretreator()
