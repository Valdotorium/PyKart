"""This script is responsible for transforming the Vehicle stored in obj.vehicle into the physics objects
for pymunk. It is called once the player presses the start button. It works as follows:

finding the properties of all parts in the vehicle and rewrite obj.vehicle for pymunk.
Then this list is used to setup the pymink physics simulation for the vehicle"""
import os
import json
def run(obj):
    #---------------------------------------------------------------- some basics
    BuildVehicle = obj.Vehicle
    PhysicsVehicle = []
    print("User started with Vehicle: ", obj.Vehicle)
    print("The Vehicles Joints are: ", obj.VehicleJoints)
    #storing the vehicle as json for readability
    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    with open(CurrentPath + "/assets/saves/latest_vehicle.json", "w") as outfile: 
        json.dump(obj.Vehicle, outfile)
    #store the vehicles joints
    with open(CurrentPath + "/assets/saves/latest_vehicle_joints.json", "w") as outfile: 
        json.dump(obj.VehicleJoints, outfile)
    #store the latest vehicles hitboxes
    with open(CurrentPath + "/assets/saves/latest_vehicle_hitboxes.json", "w") as outfile: 
        json.dump(obj.VehicleHitboxes, outfile)
    
    obj.Environment = obj.biomes[obj.SelectedEnvironment]
    
