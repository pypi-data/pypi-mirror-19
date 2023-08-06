import os
import pickle

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = BASE_DIR + "/autotests/data"
AUTOTESTS_DIR = BASE_DIR + "/autotests"
try:
    os.mkdir(AUTOTESTS_DIR)
    os.mkdir(DATA_DIR)
except OSError:
    pass


def autotest(func):
    imports = "import pickle\nfrom {func.__module__} import {func.__name__}\n\n".format(func=func)
    TEST_TEMPLATE = """
def test_{func.__name__}_{count}():
    args, kwargs,result = pickle.load(open('{BASE_DIR}/autotests/data/{func.__name__}_{count}.pickle'))
    assert {func.__name__}(*args,**kwargs) == result

"""
    d = dict(count=0, testfile=imports)
    def func_wrapper(*args, **kwargs):
        if not "py._io.saferepr" in func.__module__:
            d['count'] += 1
            result = func(*args, **kwargs)
            context = dict(func=func, count=d['count'], BASE_DIR=BASE_DIR)
            with open(DATA_DIR + '/{func.__name__}_{count}.pickle'.format(**context), mode='w') as test_data_handle:
                pickle.dump((args, kwargs, result), test_data_handle)
            new_test = TEST_TEMPLATE.format(**context)
            d['testfile'] += new_test
            with open(AUTOTESTS_DIR + "/test_{func.__name__}.py".format(**context), 'w') as test_file_handle:
                test_file_handle.write(d['testfile'])
            return result
        else:
            return func(*args,**kwargs)
    return func_wrapper

import modulehacker


class AutoTester(modulehacker.Hacker):
    def hack(self, module):
        for name, val in module.__dict__.iteritems():  # iterate through every module's attributes
            if callable(val):  # check if callable (normally functions)
                module.__dict__[name] = autotest(val)
        return module


modulehacker.register(AutoTester())

