import os

def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

mkdir("test")
os.rename('test', 'hello world')