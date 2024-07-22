import pygame,random,copy  
from .fw import fw as utils
def setup(obj):
    if not obj.isWeb:
        obj.engineSoundsPlayer = None
        for part in obj.NewVehicle:
            if part!= None and obj.engineSoundsPlayer == None:
                if part["ActiveSounds"]!= None and part["Type"] == "Engine" and obj.CFG_AllowEngineSounds:
                    Sound = obj.sounds[part["ActiveSounds"][0][0]]
                    Vol = part["ActiveSounds"][0][1]
                    
                    obj.engineSoundsPlayer = Sound
                    obj.engineSoundsPlayer.set_volume(Vol)

                else:
                    print("No sound data for part:", part["name"])

def DrivingSounds(obj):
    #TODO #22
    c = 0
    #----------------------------------------------------------------SUSPENSION SOUNDS----------------------------------------------------------------
    while c < len(obj.PymunkJoints) and c < len(obj.NewVehicleJoints):
        if obj.PymunkJoints[c]!= None and obj.NewVehicleJoints[c] != None:
            JointImpulse = obj.PymunkJoints[c].impulse
            ImpulseLimit = obj.NewVehicleJoints[c]["JointData"]["BreakPoint"]
            try:
                if JointImpulse > ImpulseLimit:
                    #print("JointImpulse of joint ", c, "(", JointImpulse, ") was too high, it broke.")
                    if not obj.SoundInFrame:
                        VolumeFactor = JointImpulse / ImpulseLimit
                        Sounds = copy.deepcopy(obj.NewVehicleJoints[c]["SoundData"])
                        #selecting a random sounds from a list of sounds
                        r = random.randint(0, len(Sounds) -1)
                        Sound = Sounds[r][0]
                        #get the sound object
                        Sound = obj.sounds[Sound]
                        #create a player for it
                        obj.SoundInFrame = True
                        #setting the players volume
                        if Sounds[r][1]*VolumeFactor > 0.99:
                            Sound.set_volume(1/1.5)
                        else:
                            Sound.set_volume(Sounds[r][1] * VolumeFactor/1.5)
                        Sound.play()

                elif JointImpulse > ImpulseLimit/1.8:
                    if not obj.SoundInFrame:
                        VolumeFactor = (JointImpulse / ImpulseLimit) -0.6
                        Sounds = copy.deepcopy(obj.NewVehicleJoints[c]["SoundData"])

                        #suspension sounds
                        Sounds.append(["suspension_1.ogg", 0.5])
                        Sounds.append(["suspension_2.ogg", 0.5])
                        Sounds.append(["suspension_3.ogg", 0.5])
                        Sounds.append(["suspension_4.ogg", 0.5])
                        Sounds.append(["suspension_5.ogg", 0.5])
                        #selecting a random sounds from a list of sounds
                        r = random.randint(0, len(Sounds) -1)
                        Sound = Sounds[r][0]
                        #get the sound object
                        Sound = obj.sounds[Sound]
                        #create a player for it
                        obj.SoundInFrame = True
                        #setting the players volume
                        if Sounds[r][1]*VolumeFactor > 0.99:
                            Sound.set_volume(1)
                        else:
                            Sound.set_volume(Sounds[r][1] * VolumeFactor)
                        Sound.play()

            except:
                print("INTERNAL ERROR: Could not play suspension sounds")
                obj.SoundInFrame = True
        c += 1
    #----------------------------------------------------------------ENGINE SOUNDS ----------------------------------------------------------------
    c = 0
    try:
        if obj.engineSoundsPlayer != None:
            obj.engineSoundsPlayer.play()

    except:
        print("INTERNAL ERROR: Could not play engine sounds")
        obj.engineSoundsPlayer = None

    #obj.engineSoundsPlayer.seek(0)
