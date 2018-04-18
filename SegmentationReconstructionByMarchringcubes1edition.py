

import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
from skimage.draw import ellipsoid


def kidneyseg(img, lstSeeds, upthreshold, lowthreshold):
    imgkidney = SimpleITK.ConnectedThreshold(image1=img,
                                             seedList=lstSeeds,
                                             lower=lowthreshold,
                                             upper=upthreshold,
                                             replaceValue=1)
    imgkidney = SimpleITK.VotingBinaryHoleFilling(image1=imgkidney,
                                                              radius=[2] * 3,
                                                              majorityThreshold=1,
                                                              backgroundValue=0,
                                                              foregroundValue=1)
    return SimpleITK.GetArrayFromImage(imgkidney)


def myshow(img, title=None, margin=0.05, dpi=40):
    nda = SimpleITK.GetArrayFromImage(img)
    spacing = img.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    extent = (0, nda.shape[1] * spacing[1], nda.shape[0] * spacing[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])

    plt.set_cmap("gray")
    ax.imshow(nda, extent=extent, interpolation=None)

    if title:
        plt.title(title)

    plt.show()

pathDicom = "/home/yin/Documents/CT2/DICOMC/PA0/ST0/SE1"
labelkidney = 1

reader = SimpleITK.ImageSeriesReader()
filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
reader.SetFileNames(filenamesDICOM)
img0riginal = reader.Execute()
image1 = img0riginal[:,:,17]
myshow(image1)
#9,186,284,20,190,320;29,threshold 8;
kidarray = kidneyseg(image1,[(186,284)],90,20)
plt.imshow(kidarray)
plt.show()

l = []
for i in range(9,10):
    img = img0riginal[:,:,i]
    array = kidneyseg(img,[(186,284)],90,0)
    l.append(array)
for i in range(10,19):
    img = img0riginal[:,:,i]
    array = kidneyseg(img,[(186,284)],90,20)
    l.append(array)
for i in range(20,28):
    img = img0riginal[:,:,i]
    array = kidneyseg(img,[(168,308)],90,12)
    l.append(array)

combine = numpy.array(l)

verts, faces, normals, values = measure.marching_cubes_lewiner(combine, 0)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Fancy indexing: `verts[faces]` to generate a collection of triangles
mesh = Poly3DCollection(verts[faces])
#mesh.set_edgecolor()
ax.add_collection3d(mesh)
ax.set_xlim(0, 200)  # a = 6 (times two for 2nd ellipsoid)
ax.set_ylim(0, 512)  # b = 10
ax.set_zlim(0, 512)  # c = 16
plt.tight_layout()
#plt.show()
