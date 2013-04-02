import env
import os

def get_line_num(path):
    with open(path) as f:
        for i, l in enumerate(f.readlines()):
            pass
        return i+1


def trans_id(key, index):
    trans_base = {
        'user-1': 0,    # uid increase from 0
        'movie-2': env.USER_NUM,    # mid increase form USER_NUM
        'history-3': env.USER_NUM+env.MOVIE_NUM,
        'social-3': env.USER_NUM+env.MOVIE_NUM,
        'tag-3': env.USER_NUM+env.MOVIE_NUM,
    }
    return trans_base[key] + index


def touch_file(path):
    """
    delete the file if file exists
    """
    if os.path.exists(path):
        os.remove(path)
