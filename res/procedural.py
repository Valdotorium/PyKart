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
    """Generating the vertices for the ground polygon"""
    while x < len(obj.Terrain) / obj.CFG_Terrain_Detail:
        obj.Terrain_Height_Change += random.uniform(-obj.CFG_Terrain_Scale / 5, obj.CFG_Terrain_Scale / 5)
        if obj.Terrain_Height_Change > obj.CFG_Terrain_Scale * 10: 
            obj.Terrain_Height_Change = obj.CFG_Terrain_Scale * 10
        if obj.Terrain_Height_Change < -obj.CFG_Terrain_Scale * 10:
            obj.Terrain_Height_Change = -obj.CFG_Terrain_Scale * 10
        TerrainDots.append(obj.Terrain_Height_Change)
        x += 1
    x = 0
    #scaaling the coordinates up
    while x < len(TerrainDots):
        TerrainDots[x] *= 1000
        #remove that line below later!
        TerrainDots[x] += 500
        #rounding the numbers for readability
        TerrainDots[x] = round(TerrainDots[x])

        x += 1
    obj.Terrain = TerrainDots

    print(obj.Terrain) 
def WritePolygonPositions(obj):
    #making tuples (x,y) out of the y positions of the future polygon vertices stored in obj.Terrain
    obj.GroundPolygon = []
    x = 0
    PolygonPoints = []
    #Edge point
    PolygonPoints.append((0, 10000))
    while x < len(obj.Terrain):
        Point = obj.Terrain[x]
        PolygonPoints.append((x * obj.CFG_Terrain_X_Scale, Point))
        x += 1
    #edge point
    PolygonPoints.append(((x - 1) * obj.CFG_Terrain_X_Scale, 10000))
    obj.GroundPolygon = PolygonPoints
    #print("THE GROUND POLYGON IS AT:", PolygonPoints)
