import numpy as np
import SimpleITK
import matplotlib.pyplot as plt

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

def kidneysegThreshold(img, lstSeeds, upthreshold, lowthreshold):
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

pathDicom = "/home/yin/Documents/CT2/DICOMC/PA0/ST0/SE3"

reader = SimpleITK.ImageSeriesReader()
filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
reader.SetFileNames(filenamesDICOM)
img0riginal = reader.Execute()
image1 = img0riginal[:,:,90]
myshow(image1)
kidarray = kidneysegThreshold(image=image1,
                           lstSeeds=(169,285),
                           upthreshold=100,
                           lowthreshold=0)
plt.imshow(kidarray)
plt.show()