from Case import Case
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import main      # from 'fileName' import main
Case.main = main

def factory():
    global case
    while Case.ct < Case.limit:
        case = Case(t)
        res = case.run()
        if not res:
            break
    Case.status(case)

t = 0
Case.limit = 10000000
Case.prograssLimit = Case.limit // 10

Case.printStyle = " [{}] | {},'{}','{}'" if t else " [{}] | {},'{}','{}',{}" # .format(ct, t, m1, *args)
try:
    print()
    factory()
except KeyboardInterrupt:
    Case.failCase = case
    Case.err = 'Ctrl + C'
    Case.status(case)