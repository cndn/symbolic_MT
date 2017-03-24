import sys
import math
from collections import defaultdict

c_e = defaultdict(lambda: 0.0)
c_f = defaultdict(lambda: 0.0)
max_F = 0
totalWord_f = 0

# E
with open(sys.argv[1],'r') as infile:
    for line in infile:
        for val in line.strip().split():
            c_e[val] += 1
            
# F
with open(sys.argv[2],'r') as infile:
    for line in infile:
        words_f = line.strip().split()
        for val in words_f:
            c_f[val] += 1
            totalWord_f += 1
        max_F = max([max_F, len(words_f)])

epsilon = 1.0 / max_F
logEpsilon = math.log(epsilon)
theta_fe = defaultdict(lambda: 1.0 / len(c_f))

e = open(sys.argv[1],'r')
f = open(sys.argv[2],'r')
Mat_f = []
Mat_e = []
for sent_f in f.xreadlines():
    Mat_f.append(sent_f.strip().split())
    Mat_e.append(e.readline().strip().split())
f.close()
e.close()

for iterCount in range(10):
    c_ef = defaultdict(lambda: 0)
    c_e = defaultdict(lambda: 0)
    for sent_f,sent_e in zip(Mat_f,Mat_e):
        for word_f in sent_f:
            pList = [theta_fe[(word_f,word_e)] for word_e in sent_e]
            sum_p = sum(pList)
            pList = [i / sum_p for i in pList]
            for word_e, p in zip(sent_e, pList):
                c_ef[(word_e,word_f)] += p
                c_e[word_e] += p

    # update theta
    for word_e,word_f in c_ef:
        theta_fe[(word_f,word_e)] = c_ef[(word_e,word_f)] / c_e[word_e]

    # log likelihood
    total = 0
    for sent_f,sent_e in zip(Mat_f,Mat_e):
        currLog = logEpsilon - len(sent_f) * math.log(len(sent_e) + 1)
        for word_f in sent_f:
            p = sum([theta_fe[(word_f,word_e)] for word_e in sent_e])
            currLog += math.log(p)
        total += currLog
    print total / totalWord_f
    # print iterCount
    
# alignment
# with open(sys.argv[3],'w') as outfile:
#     for sent_f,sent_e in zip(Mat_f,Mat_e):
#         for j,word_f in enumerate(sent_f):
#             maxIndex,maxVal = 0,0
#             for t,word_e in enumerate(sent_e):
#                 if c_ef[(word_e,word_f)] > maxVal:
#                     maxVal, maxIndex = c_ef[(word_e,word_f)], t
#                 # if theta_fe[(word_f,word_e)] > maxVal:
#                 #     maxVal = theta_fe[word_f][word_e]
#                 #     maxIndex = t
#             outfile.write(str(maxIndex) + '-' + str(j) + ' ')
#         outfile.write('\n')
#     outfile.close()

# alignment inverse
with open(sys.argv[3],'w') as outfile:
    for sent_f,sent_e in zip(Mat_f,Mat_e):
        for j,word_e in enumerate(sent_e):
            maxIndex,maxVal = 0,0
            for t,word_f in enumerate(sent_f):
                if c_ef[(word_e,word_f)] > maxVal:
                    maxVal, maxIndex = c_ef[(word_e,word_f)], t
                # if theta_fe[(word_f,word_e)] > maxVal:
                #     maxVal = theta_fe[(word_f,word_e)]
                #     maxIndex = t
            outfile.write(str(maxIndex) + '-' + str(j) + ' ')
        outfile.write('\n')
    outfile.close()

    



