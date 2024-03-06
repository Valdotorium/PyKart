"""This script is responsible for transforming the Vehicle stored in obj.vehicle into the physics objects
for pymunk. It is called once the player presses the start button. It works as follows:

finding the properties of all parts in the vehicle and rewrite obj.vehicle for pymunk.
Then this list is used to setup the pymink physics simulation for the vehicle"""
def run(obj):
    print("Ha im not doin' anythin' aight? I'm just yo' placeholder!")
    print("Cya!")
    BuildVehicle = obj.Vehicle
    PhysicsVehicle = []
    obj.gm = "game"
    obj.Vehicle = PhysicsVehicle
