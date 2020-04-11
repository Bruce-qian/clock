class Context(object):
    def __init__(self):
        print("实例化一个对象")
    def __enter__(self):
        print("获取该对象")
    def __exit__(self):
        print("退出该对象")
temp = Context()

with temp:
    print("执行体")