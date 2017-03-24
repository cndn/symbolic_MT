import sys
import math
from collections import defaultdict

PHRASE_COUNT_THRESHOLD = 2
PHRASE_SCORE_THRESHOLD = 3

def quasiConsecutive(sortedList,j2i):
    for i in range(1,len(sortedList)):
        if sortedList[i] != sortedList[i-1] + 1 and len(j2i[i]) > 0:
            return False
    return True

f = open(sys.argv[1],'r')
e = open(sys.argv[2],'r')
a = open(sys.argv[3],'r')

res = defaultdict(lambda: defaultdict(lambda: 0))
for F in f.xreadlines():
    F = F.strip().split()
    E = e.readline().strip().split()
    A = a.readline().strip().split()
    BP = []
    i2j = defaultdict(lambda:[])
    j2i = defaultdict(lambda:[])
    for pair in A:
        pair = [int(i) for i in pair.split('-')]
        i2j[pair[0]].append(pair[1])
        j2i[pair[1]].append(pair[0])
    for i1 in range(len(E)):
        for i2 in range(i1,len(E)):
            TP = set()
            for i in range(i1, i2 + 1):
                for j in i2j[i]:
                    TP.add(j)
            TP = sorted(list(TP))
            
            if len(TP) > 0 and quasiConsecutive(TP,j2i):
                j1 = TP[0]
                j2 = TP[-1]
                SP = set()
                for j in range(j1, j2 + 1):
                    for i in j2i[j]:
                        SP.add(i)
                SP = sorted(list(SP))
                if SP[0] >= i1 and SP[-1] <= i2:
                    BP.append((E[i1:i2+1],F[j1:j2+1]))
                    while j1 > 0 and len(j2i[j1]) == 0:
                        jp = j2
                        while jp < len(F) and len(j2i[jp]) == 0:
                            BP.append((E[i1:i2+1],F[j1:jp+1]))
                            jp += 1
                        j1 -= 1
    for item in BP:
        if len(item[0]) > 3 or len(item[1]) > 3: continue
        phraseE = ' '.join(item[0])
        phraseF = ' '.join(item[1])
        res[phraseE][phraseF] += 1
f.close()
e.close()
a.close()

stopPhrase = ['.','?']
with open(sys.argv[4],'w') as outfile:
    for phraseE in res:
        sumCount = sum([res[phraseE][phraseF] for phraseF in res[phraseE]])
        for phraseF in res[phraseE]:
            # if phraseF in stopPhrase or phraseE in stopPhrase:
                # continue
            score = -math.log(1.0 * res[phraseE][phraseF] / sumCount)
            if sumCount < PHRASE_COUNT_THRESHOLD or score > PHRASE_SCORE_THRESHOLD:
                continue
            outfile.write(phraseF + '\t' + phraseE + '\t' + str(score))
            outfile.write('\n')







