import vtk
import math

def rotate_tranlate(x, y, z):
    camera_RT = vtk.vtkMatrix4x4()
    camera_RT.DeepCopy((1, 0, 0, x,
                        0, 1, 0, y,
                        0, 0, 1, z,
                        0, 0, 0, 1))
    return camera_RT


degree_per_rad = 57.29578
depth_min = 10
depth_max = 1000
nx = 1280
ny = 720
fx = 1433.983426156600900
fy = 1433.136938285791800
principal_point_x = 660.350070959324970
principal_point_y = 322.923447926088840

window_center_x = -2*(principal_point_x - (nx/2)) / nx
window_center_y = 2*(principal_point_y - (ny/2)) / ny

view_angle = degree_per_rad * (2.0 * math.atan2(ny/2.0, fy))

camera_RT = rotate_tranlate(0, 0, 1000)

colors = vtk.vtkNamedColors()

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

cube = vtk.vtkCubeSource()
cube.SetCenter(0, 0, 0)
cube.SetXLength(100)
cube.SetYLength(200)
cube.SetZLength(300)
cube.Update()

cubeMapper = vtk.vtkPolyDataMapper()
cubeMapper.SetInputData(cube.GetOutput())

cubeActor = vtk.vtkActor()
cubeActor.SetMapper(cubeMapper)
cubeActor.GetProperty().SetColor(colors.GetColor3d("Cornsilk"))

camera = vtk.vtkCamera()
camera.SetPosition(0, 0, 0)
camera.SetFocalPoint(0, 0, 1)
camera.SetViewUp(0, -1, 0)
camera.SetClippingRange(depth_min, depth_max)
camera.SetWindowCenter(window_center_x, window_center_y)
camera.SetViewAngle(view_angle)

camera.SetModelTransformMatrix(camera_RT)

ren.SetActiveCamera(camera)
ren.AddActor(cubeActor)

renWin.Render()
iren.Start()
