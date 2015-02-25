import yaml
import os.path

class Loader(yaml.Loader):

    def __init__(self, stream):

        self._root = os.path.split(stream.name)[0]

        super(Loader, self).__init__(stream)

    def include(self, node):

        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

Loader.add_constructor('!include', Loader.include)

'''
Now the files can be loaded using:

>>> with open('foo.yaml', 'r') as f:
>>>    data = yaml.load(f, Loader)
>>> data
{'a': 1, 'b': [1.43, 543.55], 'c': [3.6, [1, 2, 3]]}
'''
