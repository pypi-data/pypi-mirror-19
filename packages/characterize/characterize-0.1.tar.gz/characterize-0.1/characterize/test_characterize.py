import os

from subprocess import call, check_output, Popen, PIPE

from shutil import rmtree
from time import sleep


def test_autotests():
    import characterize
    from sample_program.first.definitions import b
    from sample_program.second.definitions import a
    a(3,4)
    a(6,5)
    b(12,12)
    b(13,12)
    b(11,12)
    b(16,12)
    b(10,12)
    result = Popen(['py.test','autotests'],stdout=PIPE)
    result.wait()
    output = result.communicate()
    rmtree('autotests')
    assert 'passed' in output[0]
