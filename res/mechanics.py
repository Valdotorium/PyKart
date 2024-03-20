def Throttle(obj):
    if obj.Throttle < 0.5:
        obj.Throttle = 0
    if obj.Throttle > 100:
        obj.Throttle = 100
    else:
        obj.Throttle = obj.Throttle * 0.96
    print(obj.Throttle)

def GameMechanics(obj):
    Throttle(obj)