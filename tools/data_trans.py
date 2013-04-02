#!/usr/bin/python2.7
from __future__ import division
import env
from env import transed_path
from utils import get_line_num, trans_id, touch_file
"""
Extract Test Set from Train Set
"""
TRAIN_PATH = 'train.bm'
TEST_PATH = 'test.bm'
PREDICT_PATH = 'predict.bm'


# --------------------- test set ---------------------------
import random
class TestExtrator(object):
    """
    Ramdomly extract test set from trainset
    """
    def __init__(self, train_path, output_path, proportion):
        self.path = train_path
        self.output_path = output_path
        self.proportion = proportion
        self.res = []
        touch_file(self.output_path)
        self.out_f = open(self.output_path, 'a')
        self.tem_file_path = 'tem.tem'

    def extract_rand_line_no(self):
        env.show_status('.. extracted line nos')
        line_num = get_line_num(self.path)
        num = int(self.proportion * line_num)
        self.extracted_line_nos = set()
        while len(self.extracted_line_nos) < num:
            _num = random.randint(0, line_num-1)
            self.extracted_line_nos.add(_num)


    def extract(self):
        env.show_status('.. extracting test file')
        with open(self.path) as f:
            touch_file(self.tem_file_path)
            with open(self.tem_file_path, 'a') as tem_f:
                for i,l in enumerate(f.readlines()):
                    if i in self.extracted_line_nos:
                        self.out_f.write(l)
                    else:
                        tem_f.write(l)
    
    def update_trainset(self):
        env.show_status(".. update trainset")
        with open(self.tem_file_path) as tem_f:
            with open('_'+self.path, 'w') as train_f:
                train_f.write(tem_f.read())
                        

    def __call__(self):
        self.extract_rand_line_no()
        self.extract()
        self.update_trainset()
        env.show_status('.. test set created OK!')



if __name__ == '__main__':
    pass
