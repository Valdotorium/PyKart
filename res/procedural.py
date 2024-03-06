import random
def setup(obj):
    obj.Terrain = []
    x = 0
    while x < obj.CFG_Render_Distance * obj.CFG_Terrain_Detail:
        obj.Terrain.append(0)
        x += 1
    obj.Terrain_Height_Change = random.uniform(-obj.CFG_Terrain_Scale, obj.CFG_Terrain_Scale)

def generate_chunk(obj):
    x = 0
    TerrainDots = []
    """das erkläre ich später mal vielleicht."""
    while x < len(obj.Terrain) / obj.CFG_Terrain_Detail:
        obj.Terrain_Height_Change += random.uniform(-obj.CFG_Terrain_Scale / 5, obj.CFG_Terrain_Scale / 5)
        if obj.Terrain_Height_Change > obj.CFG_Terrain_Scale * 10: 
            obj.Terrain_Height_Change = obj.CFG_Terrain_Scale * 10
        if obj.Terrain_Height_Change < -obj.CFG_Terrain_Scale * 10:
            obj.Terrain_Height_Change = -obj.CFG_Terrain_Scale * 10
        TerrainDots.append(obj.Terrain_Height_Change)
        x += 1
    x = 0
    while x < len(TerrainDots):
        TerrainDots[x] *= 1000
        #rounding the numbers for readability
        TerrainDots[x] = round(obj.Terrain[x])

        x += 1
    obj.Terrain = TerrainDots

    print(obj.Terrain) 
def WritePolygonPositions(obj):
    obj.GroundPolygon = []
    x = 0
    PolygonPoints = []
    
    while x < len(obj.Terrain):
        Point = obj.Terrain[x]
        x += 1
