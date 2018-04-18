import vtk
from vtk.util.numpy_support import numpy_to_vtk
import numpy

def convert_to_vtk(X, 
    spacing=(0.708984375, 0.708984375, 1.0), 
    origin=(-194.568, -11.7, -335.94)):
    imgMyHead_NumPy = numpy.ravel(X, order='F')
    imgMyHead_VTK = vtk.vtkImageData()
    imgMyHead_VTK.SetSpacing(spacing)
    imgMyHead_VTK.SetOrigin(origin)
    imgMyHead_VTK.SetDimensions(X.shape)
    # imgMyHead_VTK.SetScalarType(convertTypeITKtoVTK(imgMyHead_SimpleITK.GetPixelID()), info_obj)
    imgMyHead_VTK.AllocateScalars(vtk.VTK_TYPE_UINT8, 1)
    # imgMyHead_VTK.SetNumberOfScalarComponents(imgMyHead_SimpleITK.GetNumberOfComponentsPerPixel())
    imgMyHead_NumPyToVTK = numpy_to_vtk(imgMyHead_NumPy, 
                                    deep=True, 
                                    array_type=vtk.VTK_TYPE_UINT8)

    imgMyHead_VTK.GetPointData().SetScalars(imgMyHead_NumPyToVTK)
    return imgMyHead_VTK
