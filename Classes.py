import math

def translate(x):
  return(x*50+200)

class Line:
  def __init__(self,a,b,c,x,y,z,colour):
    self.a = a
    self.b = b
    self.c = c
    self.x = x
    self.y = y
    self.z = z
    self.colour = colour

  def projectPoint(self,camera):
    tmp1 = projectToCamIso(self.a,self.b,self.c,camera)
    tmp2 = rotatePoints(camera.rotationMatrix,tmp1[0],tmp1[1],tmp1[2])
    tmp3 = translateToView(tmp2[0],tmp2[1],tmp2[2],camera.offset[0],camera.offset[1],camera.offset[2])
    tmp4 = rotatePoints2d(camera.angle,tmp3[0],tmp3[2])

    tmp21 = projectToCamIso(self.x,self.y,self.z,camera)
    tmp22 = rotatePoints(camera.rotationMatrix,tmp21[0],tmp21[1],tmp21[2])
    tmp23 = translateToView(tmp22[0],tmp22[1],tmp22[2],camera.offset[0],camera.offset[1],camera.offset[2])
    tmp24 = rotatePoints2d(camera.angle,tmp23[0],tmp23[2])
    return(round(translate(tmp4[0])),round(translate(tmp4[1])),round(translate(tmp24[0])),round(translate(tmp24[1])),self.colour,2)
    # main.drawing.line(round(translate(tmp4[0])),
    # round(translate(tmp4[1])),round(translate(tmp24[0])),round(translate(tmp24[1])),color = self.colour,width = 2)
  
  def projectPointPersp(self,camera):
    distance = ((self.a+camera.x)**2+(self.b+camera.y)**2+(self.c+camera.z)**2)*(1/2)
    distance = math.tanh(distance/30)
    #distance = (distance**2)/(distance**2+20)
    tmp1 = projectToCamIso(self.a,self.b,self.c,camera)
    tmp2 = rotatePoints(camera.rotationMatrix,tmp1[0],tmp1[1],tmp1[2])
    tmp3 = translateToView(tmp2[0],tmp2[1],tmp2[2],camera.offset[0],camera.offset[1],camera.offset[2])
    tmp4 = rotatePoints2d(camera.angle,tmp3[0],tmp3[2])
    tmp5 = [tmp4[0]*(1-distance),tmp4[1]*(1-distance)]

    distance2 = ((self.x+camera.x)**2+(self.y+camera.y)**2+(self.z+camera.z)**2)*(1/2)
    distance2 = math.tanh(distance2/30)
    #distance = (distance**2)/(distance**2+20)
    tmp21 = projectToCamIso(self.x,self.y,self.z,camera)
    tmp22 = rotatePoints(camera.rotationMatrix,tmp21[0],tmp21[1],tmp21[2])
    tmp23 = translateToView(tmp22[0],tmp22[1],tmp22[2],camera.offset[0],camera.offset[1],camera.offset[2])
    tmp24 = rotatePoints2d(camera.angle,tmp23[0],tmp23[2])
    tmp25 = [tmp24[0]*(1-distance2),tmp24[1]*(1-distance2)]
    return(round(translate(tmp5[0])),round(translate(tmp5[1])),round(translate(tmp25[0])),round(translate(tmp25[1])),self.colour,2)

class Camera:
  def __init__(self,x,y,z,i,j,k,fl,alpha):
    # focal length
    self.fl = fl
    # position vector 
    self.x = x
    self.y = y
    self.z = z
    # normal vector (as unit vector)
    self.resetEquation(-self.x,-self.y,-self.z)
    
    # rotation of the camera around its normal vector
    self.alpha = alpha

    # technical values
    self.rotationMatrix = [[0,0,0],
                           [0,0,0],
                           [0,0,0]]
    self.offset = 0
    self.angle = 0
    self._starterX = 200
    self._starterY = 200

  def resetEquation(self,i,j,k):
    if i == 0 and j == 0 and k == 0:
      return('ERROR 001: Camera cannot have 0 magnitude direction vector')
    magnitude = (i**2+j**2+k**2)**(1/2)
    self.i = i/magnitude
    self.j = j/magnitude
    self.k = k/magnitude

    self.d = (self.x+self.i*self.fl)*(self.i)+ (self.y+self.j*self.fl)*(self.j)+ (self.z+self.k*self.fl)*(self.k)
  
  def updateCam(self):
    self.rotationMatrix = rotateImagePlane(self.i,self.j,self.k)
    
    #code to figure out offset from alignment of plane
    # this fix could be avoided if rotateImagePlane made accomodations for camera.d or camera.ijk
    tmp1 = projectToCamIso(self.x+self.i,self.y+self.j,self.z+self.k,self)
    self.offset = rotatePoints(self.rotationMatrix,tmp1[0],tmp1[1],tmp1[2])

    #code to figure out risidual rotation from alignment of plane
    tmp1 = projectToCamIso(self.x+self.i,self.y+self.j,self.z+1+self.k,self)
    tmp2 = rotatePoints(self.rotationMatrix,tmp1[0],tmp1[1],tmp1[2])
    tmp3 = translateToView(tmp2[0],tmp2[1],tmp2[2],self.offset[0],self.offset[1],self.offset[2])
    # inverse tan is a pain hence these next lines
    if tmp3[0] < 0:
      self.angle = self.alpha - math.atan(tmp3[2]/tmp3[0])
    elif tmp3[0]>0:
      self.angle = self.alpha - math.atan(tmp3[2]/tmp3[0])+math.pi
    else:
      self.angle = self.alpha

  def rotateCam(self,event_data):
    global points
    try:
      #Y rotation
      alpha = (event_data.y - self._starterY)/180
      if self.k > 0:
        alpha = -(event_data.y - self._starterY)/180
      if self.k == 0:
        up = [self.i,self.j,1]
      else:
        up = [self.i,self.j,-(self.i**2+self.j**2)/self.k]
      perpendicular = [up[2]*self.j-up[1]*self.k,-(up[2]*self.i-self.k*up[0]),self.i*up[1]-self.j*up[0]]
      magnitude = (perpendicular[0]**2+perpendicular[1]**2+perpendicular[2]**2)**(1/2)
      axis = [perpendicular[0]/magnitude,perpendicular[1]/magnitude,perpendicular[2]/magnitude]
      repetition = (axis[0]*self.x+axis[1]*self.y+axis[2]*self.z)*(1-math.cos(alpha))
      vCompliment = [self.x*math.cos(alpha) + math.sin(alpha)*(axis[1]*self.z-axis[2]*self.y)+axis[0]*repetition, self.y*math.cos(alpha) - math.sin(alpha)*(axis[0]*self.z-axis[2]*self.x)+axis[1]*repetition, self.z*math.cos(alpha)+math.sin(alpha)*(axis[0]*self.y-axis[1]*self.x)+axis[2]*repetition]
      
      self.x = vCompliment[0]
      self.y = vCompliment[1]
      self.z = vCompliment[2]
      self.resetEquation(-self.x,-self.y,-self.z)

      #X rotation
      theta = -(event_data.x-self._starterX)/180
      camCoords = [self.x*math.cos(theta)-self.y*math.sin(theta),self.x*math.sin(theta)+self.y*math.cos(theta)]
      self.x = camCoords[0]
      self.y = camCoords[1]
      self.resetEquation(-self.x,-self.y,-self.z)
    except:
      pass
    finally:
      self.resetEquation(-self.x,-self.y,-self.z)
      self._starterX = event_data.x
      self._starterY = event_data.y

  def setStarter(self):
    self._starterX = None
    self._starterY = None

class Coordinate:
  def __init__(self,x,y,z,colour):
    self.i = x
    self.j = y
    self.k = z
    self.colour = colour

  # Isometric
  def projectPoint(self,camera):
    tmp1 = projectToCamIso(self.i,self.j,self.k,camera)
    tmp2 = rotatePoints(camera.rotationMatrix,tmp1[0],tmp1[1],tmp1[2])
    tmp3 = translateToView(tmp2[0],tmp2[1],tmp2[2],camera.offset[0],camera.offset[1],camera.offset[2])
    tmp4 = rotatePoints2d(camera.angle,tmp3[0],tmp3[2])
    return(round(translate(tmp4[0]))-3,round(translate(tmp4[1]))-3,round(translate(tmp4[0]))+3,round(translate(tmp4[1]))+3,self.colour)

    #main.drawing.rectangle(round(translate(tmp4[0]))-3,round(translate(tmp4[1]))-3,round(translate(tmp4[0]))+3,round(translate(tmp4[1]))+3,color = self.colour)

  #cheaty perspective
  def projectPointPersp(self,camera):
    distance = ((self.i+camera.x)**2+(self.j+camera.y)**2+(self.k+camera.z)**2)*(1/2)
    distance = math.tanh(distance/30)
    #distance = (distance**2)/(distance**2+20)
    tmp1 = projectToCamIso(self.i,self.j,self.k,camera)
    tmp2 = rotatePoints(camera.rotationMatrix,tmp1[0],tmp1[1],tmp1[2])
    tmp3 = translateToView(tmp2[0],tmp2[1],tmp2[2],camera.offset[0],camera.offset[1],camera.offset[2])
    tmp4 = rotatePoints2d(camera.angle,tmp3[0],tmp3[2])
    tmp5 = [tmp4[0]*(1-distance),tmp4[1]*(1-distance)]
    return(round(translate(tmp5[0]))-3,round(translate(tmp5[1]))-3,round(translate(tmp5[0]))+3,round(translate(tmp5[1]))+3,self.colour)
  
  def projectPointProper(self,camera):
    tmp1 = projectToCamPersp(-self.i,-self.j,-self.k,camera)
    tmp2 = rotatePoints(camera.rotationMatrix,tmp1[0],tmp1[1],tmp1[2])
    tmp3 = translateToView(tmp2[0],tmp2[1],tmp2[2],camera.offset[0],camera.offset[1],camera.offset[2])
    tmp4 = rotatePoints2d(camera.angle,tmp3[0],tmp3[2])
    return(round(translate(tmp4[0]))-3,round(translate(tmp4[1]))-3,round(translate(tmp4[0]))+3,round(translate(tmp4[1]))+3,self.colour)



#This finds the axis that is perpendicular to both the direction vector of the camera and the objective view (0,1,0). (cross product). it then rotate the points the appropriate amount around this axis so that they lie coplanar to the plane r.(0,1,0) = 0
def rotateImagePlane(x,y,z): #where xyz is the direction vector of the normal of the image plane
  if x == 0 and z == 0:
    if y == 0:
      return('ERROR 001: Camera cannot have 0 magnitude direction vector')
    elif y > 0:
      return([[1,0,0],[0,1,0],[0,0,1]])
    else:
      return([[-1,0,0],[0,-1,0],[0,0,1]])
  
  costheta = y/((x**2+y**2+z**2)**(1/2))
  bigCostheta = (1-costheta)
  biggerCostheta = ((1-costheta**2)**(1/2))
  ex = -z/(z**2+x**2)**(1/2)
  zed = x/(z**2+x**2)**(1/2)
  return([[(ex**2)*bigCostheta+costheta,-zed*biggerCostheta,ex*zed*bigCostheta],
          [zed*biggerCostheta,costheta,-ex*biggerCostheta],
          [zed*ex*bigCostheta,ex*biggerCostheta,zed**2*bigCostheta+costheta]])

def rotatePoints(matrix,a,b,c):#takes the rotation matrix and the point to be rotated and gives the rotated point
  return(matrix[0][0]*a+matrix[0][1]*b+matrix[0][2]*c,matrix[1][0]*a+matrix[1][1]*b+matrix[1][2]*c,matrix[2][0]*a+matrix[2][1]*b+matrix[2][2]*c)

def translateToView(x,y,z,i,j,k):#takes point xyz moves from image plane at ijk to view
  return(x-i,y-j,z-k)

def projectToCamPersp(x,y,z,camera): # x,y,z are coords of point to be projected
# this method projects a given point towards the image point and onto the image plane
  #mu = (camera.d-x)/(camera.x**2-camera.x*x)

  mu = (camera.d-camera.i*x-camera.j*y-camera.k*z)/(camera.i*(x-camera.x)+camera.j*(y-camera.y)+camera.k*(z-camera.z))
  line = [camera.x-x,camera.y-y,camera.z-z]
  return([line[0]*mu+x,line[1]*mu+y,line[2]*mu+z]) # returns the position vector of the point on the image plane

def projectToCamIso(i,j,k,camera):#takes normal vector of plane abc with plane scalar e and takes point coords ijk
  mu = (camera.d - camera.i* i - camera.j*j - camera.k*k)/(camera.i**2+camera.j**2+camera.k**2)
  return(i+camera.i*mu,j+camera.j*mu,k+camera.k*mu)

def projectToCamPersp2(x,y,z,camera): # x,y,z are coords of point to be projected
# this method projects a given point towards the image point and onto the image plane
  #mu = (camera.d-x)/(camera.x**2-camera.x*x)

  mu = (-camera.d+camera.i*x+camera.j*y+camera.k*z)/(-camera.i*(x+camera.x)-camera.j*(y+camera.y)-camera.k*(z+camera.z))
  line = [-camera.x-x,-camera.y-y,-camera.z-z]
  return([line[0]*mu+x,line[1]*mu+y,line[2]*mu+z]) # returns the position vector of the point on the image plane


def rotatePoints2d(angle,x,y):
  return(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle))
