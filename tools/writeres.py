# write res to prediction
import env

class ResWriter(object):
    def __init__(self, datas, output):
        self.datas = datas
        self.bind_file(output)

    def bind_file(self, output):
        # predict file
        self._pfile = open(env.predict_path)
        self.output = open(output, 'a')

    def get_res_data(self, index):
        raise NotImplementedError

    def read_write(self):
        for i, line in enumerate(self._pfile.readlines()):
            ls = line.split()
            ls.append(str(self.get_res_data(i)))
            res = '\t'.join(ls) + '\r\n'
            self.output.write(res)

class MeanResWriter(ResWriter):
    def __init__(self, mean, output):
        ResWriter.__init__(self, mean, output)

    def get_res_data(self, index):
        return self.datas


class CSVDResWriter(ResWriter):
    def __init__(self, frompath, output):
        self.datas = []
        with open(frompath) as f:
            for line in f.readlines():
                ls = line.split()
                self.datas.append(float(ls[0]))
        self.bind_file(output)

    def bind_file(self, output):
        # predict file
        self._pfile = open(env.predict_path)
        self.output = open(output, 'a')

    def get_res_data(self, index):
        return self.datas[index]

    def read_write(self):
        for i, line in enumerate(self._pfile.readlines()):
            ls = line.split()
            ls.append(str(self.get_res_data(i)))
            res = '\t'.join(ls) + '\r\n'
            self.output.write(res)

    def __call__(self):
        self.read_write()

def writeCSVDRes():
    import os
    t = os.walk('res')
    for f in t:
        base = f[0]
        filelist = f[2]
        for f in filelist:
            frompath = os.path.join(base, f)
            c = CSVDResWriter(
                    frompath, frompath+'.txt')
            c()

if __name__ == '__main__':
    #reswriter = MeanResWriter(3.6775887, './mean_predict.txt')
    #reswriter.read_write()
    writeCSVDRes()
