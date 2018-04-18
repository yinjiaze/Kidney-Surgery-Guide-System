from __future__ import print_function
import sys
from vtk.util import numpy_support
import vtk
from vtk import (
    vtkJPEGReader, vtkImageCanvasSource2D, vtkImageActor, vtkPolyDataMapper,
    vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkSuperquadricSource,
    vtkActor, VTK_MAJOR_VERSION
)
import cv2
from numpy2vtk import convert_to_vtk

class vtkTimerCallback():
    def __init__(self):
        self.timer_count = 0

    def execute(self, obj, event):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = convert_to_vtk(gray);
        image_actor = vtkImageActor()
        image_actor.SetInputData(img)
        background_renderer = vtkRenderer()
        background_renderer.SetLayer(0)
        render_window.AddRenderer(background_renderer)
        background_renderer.AddActor(image_actor)
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1

def changeBG(caller, ev):
    # Just do this to demonstrate who called callback and the event that triggered it.
    print(caller.GetClassName(), "Event Id:", ev)
    rerender()

def rerender():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = convert_to_vtk(gray);
    image_actor = vtkImageActor()
    image_actor.SetInputData(img)
    background_renderer = vtkRenderer()
    background_renderer.SetLayer(0)
    render_window.AddRenderer(background_renderer)
    background_renderer.AddActor(image_actor)
    render_window.Render()

cap  = cv2.VideoCapture(0)
superquadric_source = vtkSuperquadricSource()
superquadric_source.SetPhiRoundness(1.1)
superquadric_source.SetThetaRoundness(.4)
superquadric_mapper = vtkPolyDataMapper()
superquadric_mapper.SetInputConnection(superquadric_source.GetOutputPort())
superquadric_actor = vtkActor()
superquadric_actor.SetMapper(superquadric_mapper)
scene_renderer = vtkRenderer()
render_window = vtkRenderWindow()

scene_renderer.SetLayer(1)
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(scene_renderer)
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
scene_renderer.AddActor(superquadric_actor)

camera = vtk.vtkCamera()
camera.SetPosition(4.6,-2.0,3.8)
camera.SetFocalPoint(0.0,0.0,0.0)
camera.SetClippingRange(3.2,10.2)
camera.SetViewUp(0.3,1.0,0.13)
scene_renderer.SetActiveCamera(camera)

render_window.Render()
render_window_interactor.Initialize()

cb = vtkTimerCallback()
render_window_interactor.AddObserver('TimerEvent', cb.execute)
render_window_interactor.CreateRepeatingTimer(100)
render_window_interactor.Start()


