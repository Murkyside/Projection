import Classes
def square():
  points = []
  points.append(Classes.Coordinate(1,0,0,"black"))
  points.append(Classes.Coordinate(0,1,0,"black"))
  points.append(Classes.Coordinate(1,1,0,"black"))
  points.append(Classes.Coordinate(0,0,0,"black"))
  points.append(Classes.Coordinate(1,0,1,"black"))
  points.append(Classes.Coordinate(0,1,1,"black"))
  points.append(Classes.Coordinate(1,1,1,"black"))
  points.append(Classes.Coordinate(0,0,1,"black"))
  return(points)

def blender():
  points = []
  points.append(Classes.Coordinate(0,0,0,"black"))
  points.append(Classes.Coordinate(1,0,0,"red"))
  points.append(Classes.Coordinate(0,1,0,"green"))
  points.append(Classes.Coordinate(0,0,1,"blue"))
  return(points)

def betterBox():
  points = []
  points.append(Classes.Coordinate(1,1,1,"black"))
  points.append(Classes.Coordinate(1,1,-1,"black"))
  points.append(Classes.Coordinate(1,-1,1,"black"))
  points.append(Classes.Coordinate(1,-1,-1,"black"))
  points.append(Classes.Coordinate(-1,1,1,"black"))
  points.append(Classes.Coordinate(-1,1,-1,"black"))
  points.append(Classes.Coordinate(-1,-1,1,"black"))
  points.append(Classes.Coordinate(-1,-1,-1,"black"))
  return(points)

def dynaBox(bruh):
  points = []
  points.append(Classes.Coordinate(1,11-bruh,1,"blue"))
  points.append(Classes.Coordinate(1,11-bruh,-1,"blue"))
  points.append(Classes.Coordinate(1,9-bruh,1,"blue"))
  points.append(Classes.Coordinate(1,9-bruh,-1,"blue"))
  points.append(Classes.Coordinate(-1,11-bruh,1,"blue"))
  points.append(Classes.Coordinate(-1,11-bruh,-1,"blue"))
  points.append(Classes.Coordinate(-1,9-bruh,1,"blue"))
  points.append(Classes.Coordinate(-1,9-bruh,-1,"blue"))
  return(points)
def axis():
  points = []
  points.append(Classes.Line(-10,0,0,10,0,0,'red'))
  points.append(Classes.Line(0,-10,0,0,10,0,'green'))
  points.append(Classes.Line(0,0,-10,0,0,10,'blue'))
  return(points)

def cuboid():
  points = []
  points.append(Classes.Line(0,0,0,1,0,0,'black'))
  points.append(Classes.Line(0,0,0,0,1,0,'black'))
  points.append(Classes.Line(0,0,0,0,0,1,'black'))
  points.append(Classes.Line(1,0,0,1,0,1,'black'))
  points.append(Classes.Line(1,0,0,1,1,0,'black'))
  points.append(Classes.Line(0,0,1,1,0,1,'black'))
  points.append(Classes.Line(0,1,0,0,1,1,'black'))
  points.append(Classes.Line(0,1,0,1,1,0,'black'))
  points.append(Classes.Line(0,1,1,0,0,1,'black'))
  points.append(Classes.Line(0,1,1,1,1,1,'black'))
  points.append(Classes.Line(1,1,0,1,1,1,'black'))
  points.append(Classes.Line(1,0,1,1,1,1,'black'))
  return(points)
