import random
def setup(obj):
    obj.Terrain = []
    x = 0
    while x < obj.CFG_Render_Distance * obj.CFG_Terrain_Detail:
        obj.Terrain.append(0)
        x += 1

def generate_chunk(obj):
    """das erkläre ich später mal vielleicht."""
    obj.Terrain_Height_Change += random.uniform(-obj.CFG_Terrain_Scale, obj.CFG_Terrain_Scale)
    if obj.Terrain_Height_Change > obj.CFG_Terrain_Scale * 10: 
        obj.Terrain_Height_Change = obj.CFG_Terrain_Scale * 10
    if obj.Terrain_Height_Change < -obj.CFG_Terrain_Scale * 10:
        obj.Terrain_Height_Change = -obj.CFG_Terrain_Scale * 10
