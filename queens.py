#coding:utf-8
import random
def conflict(state,nextX):
    nextY = len(state)
    for i in range(nextY):
        if abs(nextX - state[i]) in (0,nextY - i):
            return True
    return False

def queens(num=8,state=()):
    for pos in range(num):
        if not conflict(state,pos):
            if len(state) == num - 1:
                yield (pos,)
            else:
                for result in queens(num,state+(pos,)):
                    yield result+(pos,)

solution = random.choice(list(queens()))

def prettyprint(solution):
    def line(pos,length=len(solution)):
        print ' . '*pos+' X '+' . '*(length - pos - 1)
    for pos in solution:
        line(pos)

if __name__ == '__main__':
    prettyprint(solution)