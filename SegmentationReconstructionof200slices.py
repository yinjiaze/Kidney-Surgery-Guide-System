import numpy
import SimpleITK
import matplotlib.pyplot as plt
from vtktest import gpu_render, shrink
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

pathDicom = "/home/yin/Documents/CT2/DICOMC/PA0/ST0/SE3"
labelkidney = 1

reader = SimpleITK.ImageSeriesReader()
filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
reader.SetFileNames(filenamesDICOM)
img0riginal = reader.Execute()
image1 = img0riginal[:,:,176]
myshow(image1)
image1 = SimpleITK.CurvatureFlow(image1=image1,
                                    timeStep=0.125,
                                    numberOfIterations=5)
myshow(image1)
#46 start, 35 175 over  //109  [(163,319),(160,326)],200,0)  //138  [(157,326),(182,315)],100,0  // 162  [(196,326)],100,0 // 175 [(207,335)],100,0

l = []
for i in range(46,109):
    img = img0riginal[:,:,i]
    array = kidneyseg(img,[(163,319),(160,326)],200,0)
    l.append(array)
for i in range(110,138):
    img = img0riginal[:,:,i]
    array = kidneyseg(img,[(157,326),(182,315)],100,0)
    l.append(array)
for i in range(139,162):
    img = img0riginal[:,:,i]
    array = kidneyseg(img,[(196,326)],100,0)
    l.append(array)
for i in range(163,175):
    img = img0riginal[:,:,i]
    array = kidneyseg(img,[(207,335)],100,0)
    l.append(array)
combine = numpy.array(l)

#h0, h1, w0, w1, d0, d1 = shrink(combine)

#combine = combine[h0: h1, w0: w1, d0: d1]

#print(combine.dtype, combine.shape,
      #numpy.max(combine),
      #numpy.min(combine),
      #numpy.mean(combine))

gpu_render(combine.astype(numpy.uint8))


'''verts, faces, normals, values = measure.marching_cubes_lewiner(combine, 0)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Fancy indexing: `verts[faces]` to generate a collection of triangles
mesh = Poly3DCollection(verts[faces])
#mesh.set_edgecolor()
ax.add_collection3d(mesh)
ax.set_xlim(0, 500)  # a = 6 (times two for 2nd ellipsoid)
ax.set_ylim(0, 512)  # b = 10
ax.set_zlim(0, 512)  # c = 16
plt.tight_layout()
plt.show()
'''


