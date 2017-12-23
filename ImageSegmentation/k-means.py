from PIL import Image, ImageStat
import numpy
from pathlib import Path
from os import listdir
from random import shuffle,random,randint



def checkConvergence(centroids, old_centroids,clusters):

    if len(clusters)>0:
        if MODE==1:
            sumDifCent=0
            for i in range(len(clusters)):
                for j in range(len(clusters[i])):
                        sumDifCent += abs(clusters[i][j] - centroids[i])

            sumDifOldCent = 0
            for i in range(len(clusters)):
                for j in range(len(clusters[i])):
                    sumDifOldCent += abs(clusters[i][j] - old_centroids[i])
        else: #MODE 0 & MODE 2
            sumDifCent=0
            for i in range(len(clusters)):
                for j in range(len(clusters[i])):
                    for k in range(len(centroids[0])):
                        sumDifCent+=abs(clusters[i][j][k]- centroids[i][k])

            sumDifOldCent = 0
            for i in range(len(clusters)):
                for j in range(len(clusters[i])):
                    for k in range(len(old_centroids[0])):
                        sumDifOldCent += abs(clusters[i][j][k] - old_centroids[i][k])


        if abs(sumDifCent - sumDifOldCent) < 1:
            return True
        else:
            return False
    else:
        return False



def getMin(pixel, centroids,px,py):
    minDist = 9999
    minIndex = 0
    for i in range(0, len(centroids)):
        if MODE==0:
         d = numpy.sqrt(int((centroids[i][0] - pixel[0])) ** 2 +
                        int((centroids[i][1] - pixel[1])) ** 2 +
                        int((centroids[i][2] - pixel[2])) ** 2)
        elif MODE==1:
            d = numpy.sqrt(int((centroids[i] - pixel)) ** 2)
        elif MODE==2:
            d = numpy.sqrt(int((centroids[i][0] - pixel[0])) ** 2 +
                           int((centroids[i][1] - pixel[1])) ** 2 +
                           int((centroids[i][2] - pixel[2])) ** 2 +
                           int((centroids[i][3] - px)) ** 2 +
                           int((centroids[i][4] - py)) ** 2 )

        if d < minDist:
            minDist = d
            minIndex = i

    return minIndex


def assignPixels(centroids):
    clusters = {}

    for x in range(0, img_width):
        for y in range(0, img_height):
            p = px[x, y]
            if MODE==2: # plus pixel location
                p=p+(x,y)
            minIndex = getMin(px[x, y], centroids,x,y)

            try:
                clusters[minIndex].append(p)
            except KeyError:
                clusters[minIndex] = [p]

    return clusters


def adjustCentroids(centroids, clusters):
    new_centroids = []

    for k in range(len(clusters)):
        n = numpy.mean(clusters[k], axis=0)
        if MODE==0:
            newCent = (int(n[0]), int(n[1]), int(n[2]))
        if MODE == 1:
            newCent = int(n)
        if MODE==2:
           newCent= (int(n[0]), int(n[1]), int(n[2]), int(n[3]), int(n[4]))

        print(str(k) + ": " + str(newCent))
        new_centroids.append(newCent)

    return new_centroids


def runKmeans(K):
    centroids = []
    old_centroids = []
    rgb_range = ImageStat.Stat(img).extrema
    i = 1
    # Initializes someK number of centroids for the clustering
    for k in range(0, K):
        x=numpy.random.randint(0, img_width)
        y=numpy.random.randint(0, img_height)
        cent = px[x,y]
        if MODE==2: # plus pixel location
            cent=cent+(x,y)
        centroids.append(cent)

    clusters=[]
    while not checkConvergence(centroids, old_centroids, clusters) :#and i <= 20:
        print("Iteration #" + str(i))
        i += 1
        old_centroids = centroids  # Make the current centroids into the old centroids
        clusters = assignPixels(centroids)  # Assign each pixel in the image to their respective centroids
        centroids = adjustCentroids(old_centroids,
                                    clusters)  # Adjust the centroids to the center of their assigned pixels

    print("-_--_--_--_--_--_--_--_--_--_-")
    print("Converged!")
    print(centroids)

    return centroids,clusters


def saveResults(result,fileName,k,mode):
    img = Image.new('RGB', (img_width, img_height), "white")
    p = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            RGB_value = result[getMin(px[x, y], result,x,y)]
            if MODE == 2:
                RGB_value = RGB_value[0:3]

            p[x, y] = RGB_value

    img.save('result_K'+str(k)+ '_M' +str(mode)+'_'+ fileName)


def calculateDif(datum,cluster):
    sum=0
    for value in cluster:
        sum+=abs(numpy.sqrt(int((datum[0]-value[0])) ** 2 +
                           int((datum[0] - value[1])) ** 2 +
                               int((datum[0] - value[2])) ** 2))
    return sum/len(cluster)


def silhouette(clusters):
    A=[]
    for k in range(len(clusters)):
        a=[]
        for i in range(len(clusters[k])):
            a.append(calculateDif(clusters[k][i],clusters[k]))
        A.append(a)

    B=[]
    for k in range(len(clusters)):
        for i in range(len(clusters[k])):
            b=[]
            for j in range(0,k):
                b.append(calculateDif(clusters[k][i],clusters[j]))
            for j in range(k+1, len(clusters)-1):
                b.append(calculateDif(clusters[k][i],clusters[j]))
            minAvgB=min(b)
            B.append(b)
    print("end")



MODE=1 # 0 default RGB , 1 Greyscale , 2 with location of pixels

kMax = 6
kMin=3
K=4

files = listdir("images/train")
shuffle(files)
for k in range(kMin,kMax):
    for i in range(10):
        fileName= files[i]
        img = Image.open("images/train/" + fileName)
        if MODE==1:
            img=img.convert('L')
        img_width, img_height = img.size
        px=img.load()
        result,clusters = runKmeans(k)
        #silhouette(clusters)
        saveResults(result,fileName,k,MODE)





