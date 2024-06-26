import random, pygame
from .fw import fw as utils
def ChangeColor(color, change):
    return (color[0] + change[0], color[1] + change[1], color[2] + change[2])

def RoundColor(color):
    return (int(color[0]), int(color[1]), int(color[2]))
class Particle():
    def __init__(self, Velocity, Position, Type, obj):
        self.Velocity = Velocity
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
            self.color = [180, 180, 170]
            self.duration = 60
            self.colorDecay = [0.4, 0.4, 0.4]
            self.size = random.randint(10, 15)
            self.sizeDecay = -0.09
            self.shape = "Circle"
            self.randomizeVelocity = 0.6
            self.aerodynamics = True
        if self.Type == "Spark":
            self.alpha = 160
            self.alphaDecay = -3
            self.color = [180, 180, 60]
            self.duration = 30
            self.colorDecay = [-5, -5, -2]
            self.size = random.randint(6, 14)
            self.shape = "Circle"
            self.randomizeVelocity = 0.5
            self.aerodynamics = False
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
            self.Velocity[0] += random.uniform(-self.randomizeVelocity, self.randomizeVelocity)
            self.Velocity[1] += random.uniform(-self.randomizeVelocity, self.randomizeVelocity)
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
    if type == "Explosion":
        r = random.randint(5,15)
        c = 0
        #make the index refer to a body and spawn particles on an anchor point of a constraint
        while c < r:
            ParticlePosition = (-10000,0)
            ParticleVelocity = list((random.randint(-3,3), random.randint(-1,3)))
            if c < 6:
                obj.particles.append(Particle(ParticlePosition, ParticlePosition, "Spark", obj))
            else:
                obj.particles.append(Particle(ParticlePosition, ParticlePosition, "Dust", obj))
            c += 1
def RedFlame(obj, bodyindex, hasRotation, positionOffset, count):
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




