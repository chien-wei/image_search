import numpy as np
from math import floor

class BasicLSH:
    def __init__(self, dim, l, m, w):
        self.tables = [{} for _ in range(l)]

        self.dim = dim
        self.l = l
        self.m = m
        self.w = w
        self.a = [self._generate_uniform_planes()
                  for _ in range(self.l)]
        self.b = np.random.rand(self.l, self.m) * self.w
        self.hash_tables = [{} for _ in range(self.l)]

    def _generate_uniform_planes(self):
        """ Generate uniformly distributed hyperplanes and return it as a 2D
        numpy array.
        """
        return np.random.randn(self.m, self.dim)

    def insert(self, point, extra_data):
        """
        Insert input point to each hash tables. The hash keys are strings from self.input_to_hash.
        :param point: (list) input points
        :param extra_data: () any form of distinct data for each
        :return: None
        """
        hvs = self.input_to_hash(self.hash(point))
        for i, table in enumerate(self.hash_tables):
            hv = hvs[i]
            if hv not in table:
                table[hv] = []
            table[hv].append(extra_data)

    def input_to_hash(self, keys):
        """
        Return string version of keys. List is not good for being hashing key.
        """
        basic_keys = []
        for i, key in enumerate(keys):
            s = ''
            #print(max(key), min(key))
            for val in key:
                s += "{:04x}".format(val)
            basic_keys.append(s)
        return basic_keys

    def hash(self, point):
        """
        Hash input point into a list of numbers based on the setting.
        """
        hvs = []
        for i in range(self.l):
            s = []
            for j in range(self.m):
                hv = (np.array(point).dot(self.a[i][j]) + self.b[i][j]) / self.w
                s.append(floor(hv))
            hvs.append(s)
        return hvs

    def query(self, point):
        hvs = self.input_to_hash(self.hash(point))
        seen = set()
        for i, table in enumerate(self.hash_tables):
            if hvs[i] in table:
                for candidate in table[hvs[i]]:
                    seen.add(candidate)
        return list(seen)

"""
bs = BasicLSH(10, 7, 5, 5.0)
points = np.random.rand(10, 10) * 32.0

for i, p in enumerate(points):
    bs.insert(p, i)
    bs.insert(p, i+10)
for t in bs.hash_tables:
    print(t)

print(bs.query(points[3]))
"""
