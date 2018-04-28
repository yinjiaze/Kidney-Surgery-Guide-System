from __future__ import print_function
import threading
import multiprocessing
import vtk
from vtk import (
    vtkJPEGReader, vtkImageCanvasSource2D, vtkImageActor, vtkPolyDataMapper,
    vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkSuperquadricSource,
    vtkActor, VTK_MAJOR_VERSION
)
from NatNetClient import NatNetClient

def receiveRigidBodyFrame( id, position, rotation, dataport ):
    # camera.UseExplicitProjectionTransformMatrix(True
    dataport[0] = position[0]
    dataport[1] = position[1]
    dataport[2] = position[2]
    print(position)

class setcamera():
    def __init__(self):
        self.timer_count = 0

    def execute(self, obj, event):
        camera.SetPosition(data[0]*10,data[1]*10,data[2]*10)
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1
        print("SetttingCameraRendering")

def stream1(data):
    streamingClient = NatNetClient()
    streamingClient.X = data
    streamingClient.rigidBodyListener = receiveRigidBodyFrame
    streamingClient.run()

if __name__ == '__main__':
    data = multiprocessing.Array('d',[0,0,0])
    p = multiprocessing.Process(target=stream1, args=(data,))
    p.start()

    source = vtk.vtkConeSource()
    source.SetCenter(0, 0, 0)
    source.SetRadius(1)
    source.SetHeight(1.61)
    source.SetResolution(128)
    source.Update

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    scene_renderer = vtkRenderer()
    render_window = vtkRenderWindow()

    render_window.AddRenderer(scene_renderer)
    render_window_interactor = vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    scene_renderer.AddActor(actor)

    camera = vtk.vtkCamera()
    scene_renderer.SetActiveCamera(camera)

    render_window.Render()
    render_window_interactor.Initialize()

    sc = setcamera()
    render_window_interactor.AddObserver('TimerEvent', sc.execute)
    render_window_interactor.CreateRepeatingTimer(1)
    render_window_interactor.Start()
