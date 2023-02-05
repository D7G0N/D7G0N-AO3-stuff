import sampleFanfiction as ff
import matplotlib.pyplot as plt
import numpy as np
import time

kudos = []
hits = []
bookmarks = []

for each in range(10):
    try:
        h, k, b = ff.getSample(stat1= 'hits', stat2= 'kudos', stat3= 'bookmarks')
    except:
        continue
    kudos += k
    hits += h
    bookmarks += b
    time.sleep(10)


kudosPerHit = []
bookmarksPerHit = []
for each in range(len(hits)):
    try:
        kudosPerHit.append(kudos[each] / hits[each])
        bookmarksPerHit.append(bookmarks[each]/ hits[each])
    except:
        kudosPerHit.append(0)
        bookmarksPerHit.append(0)

file = open('kudos vs bookmaks all per hit.csv', 'w')
for line in range(len(hits)):
    file.write(str(kudosPerHit[line]) + ',' + str(bookmarksPerHit[line]) + '\n')

file.close()

'''plt.scatter(hits, kudosPerHit)
plt.xlabel('Hits')
plt.ylabel('Kudos Per Hit')

z = np.polyfit(hits, kudosPerHit, 3)
p = np.poly1d(z)
xseq = np.linspace(0, 40000, 100)
plt.plot(xseq, p(xseq), color="k", lw=2.5)


plt.show()'''