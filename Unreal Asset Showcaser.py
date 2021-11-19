# Unreal Asset Showcaser


# The idea is to create a level with lights/fog/and some environment already created for asset showcase
# Random Ideas so far:
# 1.Generate Level
# 2.Add lights
# 3.Change light settings
# 4.Change fog settings
# 5.Add meshes for backdrop (maybe UE backdrop mesh, the curved one(exponentional looking one))
# 6.FIgure out how to render a video in Unreal that rotates the sun and showcases different lighting conditions
# 7.Maybe do different render passes too (Albedo,AO, Normal, Wireframe mode etc)


# PSEUDOCODE

# Imports

# Variables

# UE Class

    # function to create level
    # function to place selected assets in the new level
    # function to create lights
    # function to create fog
    # function to edit lights
    # function to edit fog
    # function to switch between rendering modes (if this works, if not, maybe create a material that showcases that ? ID AVOID THAT THO if an asset has 123121 materials that would be pretty sucky to assign each one of them)
    # function to render out each rendering pass
    # spit out video
    # Artstation integration for Upload (Does AS has an api ?)
    # Figuring out storing of passwords NOT in clear text (this is needed in case i want it to remember its user)
        # Maybe branch this out as a plugin to post to ArtStation directly ? However this might not be actually useful if artists are re-touching their renders in AE/APshop after.(Need to ask feedback from people)