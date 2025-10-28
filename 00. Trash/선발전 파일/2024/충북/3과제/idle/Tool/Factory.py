from Case import Case
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from release.main_perf2_2 import main      # from 'fileName' import main
from main import main      # from 'fileName' import main
Case.main = main

def factory():
    global case
    while Case.ct < Case.limit:
        case = Case(t)
        # case.info()         # temp
        res = case.run()
        if not res:
            break
    Case.status(case)

t = 2
Case.limit = 100000
Case.prograssLimit = 100

Case.printStyle = " [{}] | {},'{}','{}',{}" if t == 0 else " [{}] | {},'{}'"# .format(ct, t, m1, *args)
try:
    print()
    factory()
except KeyboardInterrupt:
    Case.failCase = case
    Case.err = 'Ctrl + C'
    Case.status(case)