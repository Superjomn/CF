from __future__ import division
from copy import deepcopy
from utils import cal_entropy, cal_mutual_entropy

class Tree(object):
    class Node(object):
        def __init__(self):
            """
            children[value]
            conditions : 
                to embed property's conditions to node
                list of lambda bool functions
            """
            self.parent = None
            self.children = {}
            self.conditions = []
            self.type = None

        def is_root(self):
            return self.parent is None

class Data(object):
    def __init__(self):
        self.data = []
        self.types = {}

    def get_class(self, v, data=None):
        index = self.types['class']['index']

        if data is None:
            data = self.data
        return filter(lambda x: x[index] == v, data)


    def cal_cps(self, _type, data=None):
        """ cal possibility
        _type: attribute
            format: {index, values..}
        """
        index, values = _type
        if data is None:
            data = self.data
        data_length = len(data)

        _ps = []
        for v in values:
            temdata = filter(lambda x: x[index]==v, data)
            # p(X=i)
            _p = len(temdata) / data_length
            _cps = []
            # cal p(Y=j|X=i)
            class_index, class_values = self.types['class']

            for cv in class_values:
                _cdata = self.get_class(cv, temdata)
                _cps.append(len(_cdata) / len(temdata))
            _ps.append( (_p, _cps) )
        return _ps
    
    def cal_ps(self, data):
        """ cal class's entropy
        """
        class_type = self.types['class']
        cvalues = class_type['values']
        ps = []
        for cv in cvalues:
            cdata = self.get_class(cv, data)
            ps.append(len(cdata)/len(data))
        return ps

    def filter_data(self, conditions=[], data=None):
        """ filter data from original data

        conditions: list of lambda bool functions
            to filter current data
        """
        if data is None:
            data = self.data

        for c in conditions:
            data = filter(c, data)
        return data

    def fromfile(self, path):
        """
        read data from file
        format:
            class   property_name1  property_name2  ...
            0       1               2               ...
            1       2               3               ...
        """
        with open(path) as f:
            l = f.readline()
            _types = l.split()
            for i,_type in enumerate(_types):
                self.types[_type] = {}
                self.types[_type]['index'] = i
                self.types[_type]['values'] = set()
            
            for l in f.readlines():
                self.datas.append([int(i) for i in l.split()])
            # build type
            for key,value in self.types.items():
                index, values = value
                for data in self.datas:
                    values.add(data[index])


class Trainer(object):
    def __init__(self, types, datas):
        """
        types:
            { 'property_name': [index, 0, 1, 2,], ...  }
        datas:
            (
                [class, property1, property2...],)
        """
        self.types, self.datas = types, datas
        self.root = Tree.Node()

    def build(self, parent_node=None, p_property=None, types=None):
        """ iteratively del parent's properties from types to 
        build the tree

        parent_node : object of Tree.Node
        conditions : lambda bool functions
                to filter data items from parent's data
        types : 
            { 'property_name': [index, 0, 1, 2,], ...  }
            type from which current node can build from

        Attention: types should be deepcopied 
        """
        if parent_node is None:
            if types is None:
                raise Exception, "root Node, types shouldn't be None"
            parent_node = self.root
            types = deepcopy(self.types)
            types.pop('class')

        mutual_entropys = {}
        # filter data from parent's data
        conditions = deepcopy(parent_node.conditions) 
        p_type = parent_node.type
        condition = lambda x: x[p_type['index']] == p_property
        conditions.append(condition)
        data = self.filter_data(conditions)

        # iterate each item to find the max mutual entropy
        for key, _type in types.items:
            cps = self.cal_cps(_type, data)
            ps = self.cal_ps(data)
            # cal mutual entropy
            _mutual_entropy = cal_mutual_entropy(cps, ps)
            mutual_entropys[key] = _mutual_entropy
        
        # find max entropy
        max_entropy = max(mutual_entropys.values())
        for key, value in mutual_entropys.items():
            if value == max_entropy:
                max_entropy = {key:value}
                break
        # create a node
        child_node = Tree.Node()
        child_node.conditions = conditions
        child_node.type = types
        parent_node[p_property] = child_node

        types.pop(max_entropy.keys()[0])

        if not types:
            return 
        # build tree from each branch
        for v in child_node.types['values']:
            self.build(child_node, v, types)
