import vtk
from vtk.util.numpy_support import numpy_to_vtk
import numpy

def convert_to_vtk(X):
    img_NumPy = numpy.ravel(X, order='F')
    img_VTK = vtk.vtkImageData()
    a,b = X.shape
    img_VTK.SetDimensions(a,b,1)
    #img_VTK.SetScalarType(convertTypeITKtoVTK(imgM_SimpleITK.GetPixelID()), info_obj)
    img_VTK.AllocateScalars(vtk.VTK_TYPE_UINT8, 1)
    #img_VTK.SetNumberOfScalarComponents(imgMyHead_SimpleITK.GetNumberOfComponentsPerPixel())
    img_NumPyToVTK = numpy_to_vtk(img_NumPy,
                                    deep=True,
                                    array_type=vtk.VTK_TYPE_UINT8)

    img_VTK.GetPointData().SetScalars(img_NumPyToVTK)
    return img_VTK
