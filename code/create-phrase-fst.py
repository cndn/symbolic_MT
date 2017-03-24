import sys
from collections import defaultdict
prefixID = defaultdict(lambda: str(len(prefixID)))
x = prefixID['']
outfile = open(sys.argv[2],'w')
dup = set()
with open(sys.argv[1],'r') as infile:
    for count,line in enumerate(infile.xreadlines()):
        phraseF, phraseE, score = line.strip().split('\t')
        phraseF = phraseF.split(' ')
        phraseE = phraseE.split(' ')
        edges = []
        for f in phraseF:
            edges.append(f + ' <eps>')
        for e in phraseE:
            edges.append('<eps> ' + e)
        for i in range(len(edges) + 1):
            if ' '.join(edges[:len(edges) - i]) in prefixID:
                currPrefix = ' '.join(edges[:len(edges) - i])
                prevID = prefixID[currPrefix]
                for idx in range(len(edges) - i,len(edges)):
                    currPrefix = (currPrefix + ' ' + edges[idx]).strip()
                    currID = prefixID[currPrefix]
                    towrt = prevID + ' ' + currID + ' ' + edges[idx] + '\n'
                    if towrt not in dup:
                        outfile.write(towrt)
                        dup.add(towrt)
                    prevID = str(len(prefixID) - 1)
                outfile.write(prevID + ' 0 <eps> <eps> ' + score + '\n')
                break
    outfile.write('0 0 </s> </s>\n')
    outfile.write('0 0 <unk> <unk>\n')
    outfile.write('0\n')
        

            






