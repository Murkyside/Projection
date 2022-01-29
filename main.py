from guizero import App, Drawing, PushButton
import math
import Presets
import Classes

w =  400
h = 400

app = App()
drawing = Drawing(app, width=w, height=h)


camera = Classes.Camera(0,3,0,0,-2,0,1,math.pi/2)

class Hand:
  def __init__(self, name, data, children=None):
    self.name = name
    self.data = data
    self.children = []
    if children is not None:
      for child in children:
        self.children.append(child)

def zoomIn(camera):
  camera.x = camera.x + camera.i
  camera.y = camera.y + camera.j
  camera.z = camera.z + camera.k

def zoomOut(camera):
  camera.x = camera.x - camera.i
  camera.y = camera.y - camera.j
  camera.z = camera.z - camera.k

def main():
  global w
  global h
  global camera
  print(camera.x,camera.y,camera.z)
  drawing.rectangle(0,0,w,h,color = "white")
  camera.updateCam()
  camera.resetEquation(-camera.x,-camera.y,-camera.z)
  drawing.when_mouse_dragged = camera.rotateCam
  drawing.when_left_button_released = camera.setStarter

  # Objecs section
  # Points:
  # square, betterBox, dynaBox(theta), blender
  points = Presets.square()
  # Lines:
  # axis, cuboid
  lines = Presets.axis()+Presets.cuboid()


  # handInstance = Hand('metacarpal',[0,0,0,'black'],
  # [Hand('thumb',[-0.5,1,0.5,'black']),Hand('index',[-0.35,1.5,0.75,'black']),Hand('middle',[-0.1,1.6,0.8,'black']),Hand('ring',[0.25,1.55,0.7,'black']),Hand('little',[0.5,1.5,0.6,'black'])])
  # def TreeProject(instance):
  #   for i in range(len(instance.children)):
  #     print(len(instance.children))
  #     projectLine(instance.data[0],instance.data[1],instance.data[2],instance.children[i].data[0],instance.children[i].data[1],instance.children[i].data[2],instance.children[i].data[3],camera)
  #     TreeProject(instance.children[i])
  # TreeProject(handInstance)
  
  for i in range(len(lines)):
    display = lines[i].projectPointPersp(camera)
    drawing.line(display[0],display[1],display[2],display[3],color = display[4],width = display[5])
  for i in range(len(points)):
    display = points[i].projectPointPersp(camera)
    drawing.rectangle(display[0],display[1],display[2],display[3],color = display[4])

zoomPlus = PushButton(app, command=zoomIn,args = [camera])
zoomMinus = PushButton(app, command=zoomOut,args = [camera])
drawing.repeat(100,main)
app.display()