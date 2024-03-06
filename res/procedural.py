def setup(obj):
    obj.Terrain = []
    x = 0
    while x < obj.CFG_Chunk_Size * obj.CFG_Chunk_Detail * obj.CFG_Render_Distance_Chunks:
        obj.terrain.append(0)
        x += 1

    print("generated Terrain:" + obj.Terrain)