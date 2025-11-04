# export file for Blender, gets called when exporting to Unity

import sys
import bpy

test = sys.argv[-1]
print(f"last arg: {test}")
print("hello from exporter file")

print("------------")
for collections in bpy.data.collections:
    print(collections.name)

print("------------")
