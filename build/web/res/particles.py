import random, pygame
from .fw import fw as utils
def ChangeColor(color, change):
    return (color[0] + change[0], color[1] + change[1], color[2] + change[2])

def RoundColor(color):
    return (int(color[0]), int(color[1]), int(color[2]))
class Particle():
    def __init__(self, Velocity, Position, Type, obj):
        self.Velocity = list(Velocity)
        self.Position = list(utils.MultiplyTuple(Position, obj.GameZoom))
        self.Type = Type
        self.frame = 0
    
        if self.Type == "Smoke":
            self.color = [130, 100, 100]
            self.alpha = 55
            self.alphaDecay = -0.7
            self.duration = 60
            self.colorDecay = [0.7, 0.9, 0.9]
            self.size = random.randint(20, 30)
            self.shape = "Circle"
            self.randomizeVelocity = 0.6
            self.aerodynamics = True
        
        if self.Type == "Dust":
            self.alpha = 50
            self.alphaDecay = -0.8
            self.color = [120, 110, 90]
            self.duration = 30
            self.colorDecay = [0.4, 0.4, 0.4]
            self.size = random.randint(10, 15)
            self.sizeDecay = -0.3
            self.shape = "Circle"
            self.randomizeVelocity = 0.6
            self.aerodynamics = True
        
        if self.Type == "Spark":
            self.alpha = 160
            self.alphaDecay = -3
            self.color = [random.randint(185, 220), random.randint(150, 185), random.randint(65, 165)]
            self.duration = 10
            self.colorDecay = [-16, -14, -5]
            self.size = random.randint(6, 14)
            self.shape = "Circle"
            self.randomizeVelocity = 0.5
            self.aerodynamics = True
        
        if self.Type == "Red Flame":
            self.alpha = 190
            self.alphaDecay = -8
            self.color = [random.randint(180,190), random.randint(130,180), random.randint(50, 70)]
            self.duration = 20
            self.colorDecay = [-6, -5, -2.4]
            self.size = random.randint(22, 30)
            self.shape = "Square"
            self.randomizeVelocity = 0.5
            self.aerodynamics = False
        
        if self.Type == "Blue Flame":
            self.alpha = 220
            self.alphaDecay = -15
            self.color = [random.randint(170,190), random.randint(210,230), random.randint(230, 250)]
            self.duration = 12
            self.colorDecay = [-9, -10, -12]
            self.size = random.randint(20, 28)
            self.shape = "Square"
            self.randomizeVelocity = 0.25
            self.aerodynamics = False
        
        if self.Type == "Bubble":
            self.alpha = 200
            self.alphaDecay = -4
            self.color = [random.randint(100, 120), random.randint(180, 235), random.randint(195, 250)]
            self.duration = 48
            self.colorDecay = [-1, -4, -3]
            self.aerodynamics = False
            self.randomizeVelocity = False
            self.size = random.randint(4, 11)
            self.shape = "Circle"

        if self.Type == "Star":
            self.alpha = 150
            self.alphaDecay = -1
            self.color = [random.randint(230, 250), random.randint(225, 240), random.randint(190, 235)]
            self.duration = 145
            self.colorDecay = [-1, -1, -1]
            self.aerodynamics = False
            self.randomizeVelocity = False
            self.size = random.randint(1, 5)
            self.shape = "Circle"

        if self.shape == "Square":
            self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.surface, RoundColor(self.color), (0,0,self.size, self.size))
        
        if self.shape =="Circle":
            self.surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.surface, RoundColor(self.color), (self.size, self.size), self.size)
    def update(self,obj):
        self.Position[0] += self.Velocity[0]
        self.Position[1] += self.Velocity[1]
        #if randomizeVelocity, change the velocity by a very small amount, velocity is a tuple
        if self.randomizeVelocity != False:
            self.Velocity[0] += random.uniform(-self.randomizeVelocity, self.randomizeVelocity) / obj.fpsFactor
            self.Velocity[1] += random.uniform(-self.randomizeVelocity, self.randomizeVelocity) / obj.fpsFactor
        #size and color decay
        #color decay
        self.color = (self.color[0] + self.colorDecay[0], self.color[1] + self.colorDecay[1], self.color[2] + self.colorDecay[2])
        #alpha decay
        self.alpha += self.alphaDecay
        if self.alpha > 255:
            self.alpha = 255
        if self.alpha < 0:
            self.alpha = 0

        self.frame += 1
        if obj.PymunkBodies[0] != None and self.aerodynamics:
            self.Velocity = utils.AddTuples(self.Velocity, utils.MultiplyTuple(obj.PymunkBodies[0].velocity, -0.00025))
        self.Velocity = list(self.Velocity)
        #drawing the particle to the screen

        if self.shape == "Circle":

            self.surface.set_alpha(self.alpha)
            #blit surface to screen
            obj.screen.blit(self.surface, (self.Position[0] - self.size / 2, self.Position[1] - self.size / 2))
        if self.shape == "Square":

            self.surface.set_alpha(self.alpha)
            #blit surface to screen
            obj.screen.blit(self.surface, (self.Position[0] - self.size / 2, self.Position[1] - self.size / 2))

def ParticleEffect(obj, type, partindex):
    if type == "Exhaust":
        r = random.randint(0,1000)
        if r <= obj.Throttle + 35:
            ParticleVelocity = (0,0)
            ParticleVelocity = utils.AddTuples(ParticleVelocity, (-4,-1))
            ParticlePosition = obj.PymunkBodies[partindex].position
            ParticlePosition = utils.AddTuples(ParticlePosition,(-obj.X_Position, -obj.Y_Position))
            #make velocity and pos lists
            ParticleVelocity = list(ParticleVelocity)
            ParticlePosition = list(ParticlePosition)
            #print(obj.Throttle)
            obj.particles.append(Particle(ParticleVelocity, ParticlePosition, "Smoke", obj))
    if type == "Break":
        pass
def RedFlame(obj, bodyindex, hasRotation, positionOffset, count):
    c = 0
    while c < count:
        randomPositionOffset = (random.uniform(-5 - obj.VehicleSpeed / 10,5 + obj.VehicleSpeed / 10), random.uniform(-5 - obj.VehicleSpeed / 10,5 + obj.VehicleSpeed / 10))
        ParticlePosition = obj.PymunkBodies[bodyindex].position
        ParticlePosition = utils.AddTuples(ParticlePosition, (-obj.X_Position, -obj.Y_Position))
        ParticlePosition = utils.AddTuples(ParticlePosition, randomPositionOffset)
        ParticlePosition = list(utils.AddTuples(ParticlePosition, positionOffset))
        ParticleVelocity = utils.AddTuples(-obj.PymunkBodies[bodyindex].velocity , utils.RotateVector(-obj.PymunkBodies[bodyindex].velocity, utils.RadiansToDegrees(obj.PymunkBodies[bodyindex].angle)))
        #divide the tuple by obj.fps
        ParticleVelocity = list(utils.DivideTuple(ParticleVelocity, obj.fps))
        obj.particles.append(Particle(ParticleVelocity, ParticlePosition, "Red Flame", obj))
        c += 1
def BlueFlame(obj, bodyindex, hasRotation, positionOffset, count):
    c = 0
    while c < count:
        randomPositionOffset = (random.uniform(-5 - obj.VehicleSpeed / 10,5 + obj.VehicleSpeed / 10), random.uniform(-5 - obj.VehicleSpeed / 10,5 + obj.VehicleSpeed / 10))
        ParticlePosition = obj.PymunkBodies[bodyindex].position
        ParticlePosition = utils.AddTuples(ParticlePosition, (-obj.X_Position, -obj.Y_Position))
        ParticlePosition = utils.AddTuples(ParticlePosition, randomPositionOffset)
        ParticlePosition = list(utils.AddTuples(ParticlePosition, positionOffset))
        ParticleVelocity = utils.AddTuples(-obj.PymunkBodies[bodyindex].velocity, utils.RotateVector(-obj.PymunkBodies[bodyindex].velocity, utils.RadiansToDegrees(obj.PymunkBodies[bodyindex].angle)))
        #divide the tuple by obj.fps
        ParticleVelocity = list(utils.DivideTuple(ParticleVelocity, obj.fps))
        obj.particles.append(Particle(ParticleVelocity, ParticlePosition, "Blue Flame", obj))
        c += 1
def Bubbles(obj):
    ParticleVelocity = utils.DivideTuple(-obj.PymunkBodies[0].velocity, random.randint(20, 24))
    #place the particle on a random location on screen
    ParticlePosition = (random.randint(0, 1200), random.randint(0, 800))
    ParticlePosition = list(ParticlePosition)
    obj.particles.append(Particle(ParticleVelocity, ParticlePosition, "Bubble", obj))

def Stars(obj):
    #have a lower chance to appear
    if random.randint(0,10) <= 1:
        ParticleVelocity = (0,0)
        #place the particle on a random location on screen
        ParticlePosition = (random.randint(0, 1200), random.randint(0, 800))
        ParticlePosition = list(ParticlePosition)
        obj.particles.append(Particle(ParticleVelocity, ParticlePosition, "Star", obj))

def Explosion(obj, particlePosition, particleVelocity, strength):
    particlePosition = utils.AddTuples(particlePosition,(-obj.X_Position, -obj.Y_Position))
    if strength <= 17500:
        particleCount = random.randint(2, 5)
        while particleCount > 0:
            particleVelocity = utils.AddTuples(particleVelocity, (random.uniform(-3, 3), random.uniform(-3, 3)))
            particleCount -= 1
            #create a dust particle
            obj.particles.append(Particle(particleVelocity, particlePosition, "Dust", obj))
        #create 2 to 4 smoke particles
        particleCount = random.randint(2,4)
        while particleCount > 0:
            particleVelocity = utils.AddTuples(particleVelocity, (random.uniform(-1, 1), random.uniform(-1,1)))
            particleCount -= 1
            #create a dust particle
            obj.particles.append(Particle(particleVelocity, particlePosition, "Smoke", obj))

    else:
        particleCount = random.randint(5, 7)
        while particleCount > 0:
            particleVelocity = utils.AddTuples(particleVelocity, (random.uniform(-3, 3), random.uniform(-3, 3)))
            particleCount -= 1
            #create a dust particle
            obj.particles.append(Particle(particleVelocity, particlePosition, "Dust", obj))
        #create 2 to 4 smoke particles
        particleCount = random.randint(2, 4)
        while particleCount > 0:
            particleVelocity = utils.AddTuples(particleVelocity, (random.uniform(-2, 2), random.uniform(-2,2)))
            particleCount -= 1
            #create a dust particle
            obj.particles.append(Particle(particleVelocity, particlePosition, "Smoke", obj))
        #create 2 to 5 fire particles
        particleCount = random.randint(2,5)
        while particleCount > 0:
            particleVelocity = utils.AddTuples(particleVelocity, (random.uniform(-3, 3), random.uniform(-3,3)))
            particleCount -= 1
            #create a dust particle
            obj.particles.append(Particle(particleVelocity, particlePosition, "Red Flame", obj))
def crack(obj, particlePosition, particleVelocity):
    particlePosition = utils.AddTuples(particlePosition,(-obj.X_Position, -obj.Y_Position))
    #create 0 to 2 fire particles
    particleCount = random.randint(0,2)
    while particleCount > 0:
        particleVelocity = utils.AddTuples(particleVelocity, (random.uniform(-3, 3), random.uniform(-3,3)))
        particleCount -= 1
        #create a dust particle
        obj.particles.append(Particle(particleVelocity, particlePosition, "Red Flame", obj))
    particleCount = random.randint(2, 3)
    while particleCount > 0:
        particleVelocity = utils.AddTuples(particleVelocity, (random.uniform(-3, 3), random.uniform(-3, 3)))
        particleCount -= 1
        #create a dust particle
        obj.particles.append(Particle(particleVelocity, particlePosition, "Dust", obj))


        



