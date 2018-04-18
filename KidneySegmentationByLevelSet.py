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

def kidneysegLevelset(image,lstSeeds,factor,itnum):
    seg = SimpleITK.Image(image.GetSize(), SimpleITK.sitkUInt8)
    seg.CopyInformation(image)
    seg[lstSeeds] = 1
    seg = SimpleITK.BinaryDilate(seg,2)

    stats = SimpleITK.LabelStatisticsImageFilter()
    stats.Execute(image, seg)

    lower_threshold = stats.GetMean(1)-factor*stats.GetSigma(1)
    upper_threshold = stats.GetMean(1)+factor*stats.GetSigma(1)
    init_ls = SimpleITK.SignedMaurerDistanceMap(seg, insideIsPositive=True, useImageSpacing=True)
    lsFilter = SimpleITK.ThresholdSegmentationLevelSetImageFilter()
    lsFilter.SetLowerThreshold(lower_threshold)
    lsFilter.SetUpperThreshold(upper_threshold)
    lsFilter.SetMaximumRMSError(0.02)
    lsFilter.SetNumberOfIterations(itnum)
    lsFilter.SetCurvatureScaling(1)
    lsFilter.SetPropagationScaling(1)
    lsFilter.ReverseExpansionDirectionOn()
    imgkidney = lsFilter.Execute(init_ls, SimpleITK.Cast(image, SimpleITK.sitkFloat32))
    imgkidney = SimpleITK.Cast(imgkidney,SimpleITK.sitkUInt8)
    kidarray = SimpleITK.GetArrayFromImage(imgkidney)
    kidarray[kidarray == 2] = 1
    '''
    imgkidney = SimpleITK.VotingBinaryHoleFilling(image1=imgkidney,
                                                              radius=[2] * 3,
                                                              majorityThreshold=1,
                                                              backgroundValue=0,
                                                              foregroundValue=1,
                                                ) 
    '''
    return kidarray

pathDicom = "/home/yin/Documents/CT2/DICOMC/PA0/ST0/SE3"
labelkidney = 1

reader = SimpleITK.ImageSeriesReader()
filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
reader.SetFileNames(filenamesDICOM)
img0riginal = reader.Execute()
image1 = img0riginal[:,:,90]
myshow(image1)
kidarray = kidneysegLevelset(image=image1,
                           lstSeeds=(169,285),
                           factor=3,
                           itnum=300)
plt.imshow(kidarray)
plt.show()