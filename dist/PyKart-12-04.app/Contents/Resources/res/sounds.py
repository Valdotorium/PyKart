import pygame,random,pyglet.media  ,copy  
def setup(obj):
    obj.engineSoundsPlayer = None
    for part in obj.NewVehicle:
        if part!= None and obj.engineSoundsPlayer == None:
            if part["ActiveSounds"]!= None and part["Type"] == "Engine":
                Sound = obj.sounds[part["ActiveSounds"][0][0]]
                Vol = part["ActiveSounds"][0][1]
                player = pyglet.media.Player()
                player.volume = Vol
                player.loop = True
                player.queue(Sound)
      
               
                obj.engineSoundsPlayer = player

            else:
                print("No sound data for part:", part["name"])
    
def DrivingSounds(obj):
    c = 0
    #----------------------------------------------------------------SUSPENSION SOUNDS----------------------------------------------------------------
    while c < len(obj.PymunkJoints) and c < len(obj.NewVehicleJoints):
        if obj.PymunkJoints[c]!= None and obj.NewVehicleJoints[c] != None:
            JointImpulse = obj.PymunkJoints[c].impulse
            ImpulseLimit = obj.NewVehicleJoints[c]["JointData"]["BreakPoint"]

            if JointImpulse > ImpulseLimit:
                print("JointImpulse of joint ", c, "(", JointImpulse, ") was too high, it broke.")
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
                    Player = Sound.play()
                    #setting the players volume
                    if Sounds[r][1]*VolumeFactor > 0.99:
                        Player.volume = 1
                    else:
                        Player.volume = Sounds[r][1] * VolumeFactor

                    Player.play()
            elif JointImpulse > ImpulseLimit/2.8:
                if not obj.SoundInFrame:
                    VolumeFactor = (JointImpulse / ImpulseLimit) / 2
                    Sounds = copy.deepcopy(obj.NewVehicleJoints[c]["SoundData"])
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
                    Player = Sound.play()
                    #setting the players volume
                    if Sounds[r][1]*VolumeFactor > 0.99:
                        Player.volume = 1
                    else:
                        Player.volume = Sounds[r][1] * VolumeFactor
                    #playing the sound object
                    #print("latest played sound:", Sounds[r][0])
                    Player.play()
        c += 1
    #----------------------------------------------------------------ENGINE SOUNDS ----------------------------------------------------------------
    c = 0
    try:
        if obj.engineSoundsPlayer != None:
            obj.engineSoundsPlayer.play()
            pitch = round((1.25 + abs(obj.Throttle) / 260 + abs(obj.rpm / 10000)) * 32)
            obj.engineSoundsPlayer.pitch = pitch / 32
    except:
        print("INTERNAL ERROR: Could not play engine sounds")
        obj.engineSoundsPlayer = None

    #obj.engineSoundsPlayer.seek(0)
