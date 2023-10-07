bl_info = {
    "name": "LightRatioSet",
    "author": "Cityofstarso_O",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "N_panel",
    "description": "Adds a new light group and work conveniently",
    "warning": "This addon is not perfect which is still being developed",
    "doc_url": "",
    "category": "Scene",
}

import bpy

# _OT_create MainLight and FillLight
class CreateLightOperator(bpy.types.Operator):
    bl_idname = "object.create_light"
    bl_label = "Create Lights"
    
    def execute(self, context):
        # create two point lights
        light_data1 = bpy.data.lights.new(name="MainLight", type='POINT')
        light_object1 = bpy.data.objects.new(name="MainLight", object_data=light_data1)
        
        light_data2 = bpy.data.lights.new(name="FillLight", type='POINT')
        light_object2 = bpy.data.objects.new(name="FillLight", object_data=light_data2)

        # add them to Scene
        scene = context.scene
        scene.collection.objects.link(light_object1)
        scene.collection.objects.link(light_object2)

        # set location
        light_object1.location = (-8, -10, 1)
        light_object2.location = (8, -10, 1)
        
        # set light energy
        light_data1.energy = 8000
        light_data2.energy = 2000
        
        # set MainLight to be active
        context.view_layer.objects.active = light_object1
        light_object1.select_set(True)
        
        return {'FINISHED'}

# _OT_change energy,ratio,distance,z_axis,reverse
class SetLightEnergyOperator(bpy.types.Operator):
    bl_idname = "object.set_light_energy"
    bl_label = "Set Light Energy"
    
    def execute(self, context):
        # get the active object
        light_object = context.active_object
        if light_object and light_object.type == 'LIGHT':
            # get the input value
            new_energy = context.scene.custom_light_energy
            new_ratio = context.scene.custom_light_ratio
            new_distance = context.scene.custom_light_distance
            new_z = context.scene.custom_light_z_axis
            # get existent MainLight and FillLight from Scene by searching the names
            light_object1 = bpy.data.objects.get("MainLight")
            light_object2 = bpy.data.objects.get("FillLight")
            # change the light energy according to custom_light_energy and custom_light_ratio
            new_energy2 = new_energy / new_ratio
            light_object2.data.energy = new_energy2
            light_object.data.energy = new_energy
            # change the distance of lights to (0,0,0)
            light_object1.location = new_distance*light_object1.location
            light_object2.location = new_distance*light_object2.location
            # change the z_axis, namely up and down
            light_object1.location.z = new_z
            light_object2.location.z = new_z
            # if you need the MainLight to be at the right side,then reverse
            if context.scene.custom_light_reverse == True:
                light_object1.location.x = -1*light_object1.location.x
                light_object2.location.x = -1*light_object2.location.x
        
        return {'FINISHED'}

# custom scene.RNAProperty
def myProperty():
    # custom_light_energy of FloatProperty
    bpy.types.Scene.custom_light_energy = bpy.props.FloatProperty(
        name="Light Energy",
        default=8000,
        min=0
    )
    # custom_light_ratio of FloatProperty
    bpy.types.Scene.custom_light_ratio = bpy.props.FloatProperty(
        name="Ratio",
        default=1,
        min=0.25,
        max=32
    )
    # custom_light_distance property of FloatProperty
    bpy.types.Scene.custom_light_distance = bpy.props.FloatProperty(
        name="Distance",
        default=1,
        min=0.01,
    )
    # custom_light_z_axis property of FloatProperty
    bpy.types.Scene.custom_light_z_axis = bpy.props.FloatProperty(
        name="Z_axis",
        default=0,
    )
    # custom_light_reverse of BoolProperty
    bpy.types.Scene.custom_light_reverse = bpy.props.BoolProperty(name="Reverse")
    
# _PT_
class CustomLightPanel(bpy.types.Panel):
    bl_label = "LightRatioSet"
    bl_idname = "OBJECT_PT_custom_light_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LightRatioSet' # press 'N' in the 3d view,and you will find it.

    def draw(self, context):
        layout = self.layout
        layout.label(text="Operate on MainLight:")
        col = layout.column()
        # energy
        col.prop(context.scene, "custom_light_energy",text="Energy")
        # ratio
        col.prop(context.scene, "custom_light_ratio", text="Ratio")
        # distance
        col.prop(context.scene, "custom_light_distance", text="Distance")
        # z_axis
        col.prop(context.scene, "custom_light_z_axis", text="Z_axis")
        # reverse
        col.prop(context.scene, "custom_light_reverse", text="Reverse")
        # create lights and update Buttons
        layout.operator("object.create_light", text="Create Light Group")
        layout.operator("object.set_light_energy", text="Update Lights")

def register():
    myProperty()

    bpy.utils.register_class(CreateLightOperator)
    bpy.utils.register_class(SetLightEnergyOperator)
    bpy.utils.register_class(CustomLightPanel)

def unregister():
    del bpy.types.Scene.custom_light_energy
    bpy.utils.unregister_class(CreateLightOperator)
    bpy.utils.unregister_class(SetLightEnergyOperator)
    bpy.utils.unregister_class(CustomLightPanel)

if __name__ == "__main__":
    register()