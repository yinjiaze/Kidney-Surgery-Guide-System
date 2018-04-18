import vtk
from numpy import *
import numpy as np

from vtkConvert import convert_to_vtk

def MCBRecons(X):

    img = convert_to_vtk(X)
    dmc = vtk.vtkDiscreteMarchingCubes()
    #dmc.SetInputConnection(dataImporter.GetOutputPort())
    dmc.SetInputData(img)
    dmc.GenerateValues(1, 1, 1)
    dmc.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(dmc.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1.0, 1.0, 1.0)

    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderInteractor = vtk.vtkRenderWindowInteractor()
    renderInteractor.SetRenderWindow(renderWin)

    renderWin.SetSize(1000, 1000)

    renderWin.AddObserver("AbortCheckEvent", exitCheck)

    renderInteractor.Initialize()
    renderWin.Render()
    renderInteractor.Start()

