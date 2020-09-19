"""from subprocess import call
call("./run.sh")"""

import os
from multiprocessing import Pool

processes = ('Producer.py', 'Consumer.py')


def run_process(process):
    os.system('python {}'.format(process))


pool = Pool(processes=2)
pool.map(run_process, processes)