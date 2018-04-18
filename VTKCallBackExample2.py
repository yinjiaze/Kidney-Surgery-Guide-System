from __future__ import print_function
import vtk

source = vtk.vtkSphereSource()
source.SetCenter(0,0,0)
source.SetRadius(1)
source.Update()

mapper = vtk.vtkOpenGLPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

ren = vtk.vtkRenderer()
ren.SetBackground(1,1,1)
ren.AddActor(actor)

renw = vtk.vtkRenderWindow()
renw.AddRenderer(ren)

reni = vtk.vtkRenderWindowInteractor()
reni.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
reni.SetRenderWindow(renw)

def DF1(obj,ev):
    print('B')

def DF2(obj,ev):
    print('A')

reni.RemoveObservers('LeftButtonPressEvent')
reni.AddObserver('LeftButtonPressEvent',DF1,1.0)
reni.AddObserver('LeftButtonPressEvent',DF2,-1.0)
reni.Initialize()
reni.Start()