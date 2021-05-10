import bpy
import importlib
from bpy.utils import register_class, unregister_class
import sys
import os
import numpy as np
import re
from .evaluate_motion_vae import character_matrix
from .init_skeleton import init_skeleton, parent_skeleton


def main(context):
    for ob in context.scene.objects:
        print(ob)


class ButtonOperator(bpy.types.Operator):
    bl_idname = "random.1"
    bl_label = "Simple Object Operator"
    property = bpy.props.IntProperty()
    
    
    #Prende in input la matrice [60, 24, 3] fornita dalla rete e crea l'animazione muovendo gli empty.
    def animate_skeleton(self, matrix):
        for collection in bpy.data.collections:
            i = 0
            for obj in collection.all_objects:
                if re.search("^Empty.*", obj.name):
                    frame_number = 0
                    for coordinates in matrix:
                        x = coordinates[i][0]
                        y = coordinates[i][1]
                        z = coordinates[i][2]
                        bpy.context.scene.frame_set(frame_number)
                        obj.location = (x, y, z)
                        obj.keyframe_insert(data_path="location", index=-1)
                        frame_number += 10
                    i += 1
            
    #Scelta della funzione in base al valore "property" in input dopo la pressione di un pulsante sul pannello laterale
    def execute(self, context): 
        if self.property == -2:
            init_skeleton() #Chiama la funzione per generare lo scheletro in posizione neutra
        elif self.property == -1:
            parent_skeleton() #Imparenta lo scheletro con la mesh fornita dall'utente
        else:
            self.animate_skeleton(character_matrix(self.property))
        return {'FINISHED'}

#Pannello laterale con i pulsanti per generare lo scheletro e le animazioni fornite dalla rete
class CustomPanel(bpy.types.Panel):
    bl_label = "A2M Animation Panel"
    bl_idname = "OBJECT_PT_random"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Action to Motion"

    #Elenco dei pulsanti
    def draw(self, context):
        layout = self.layout
        obj = context.object
        column = layout.column()
        column.operator(ButtonOperator.bl_idname, text="Skeleton", icon='OUTLINER_OB_ARMATURE').property = -2 #Valore per chiamare la funzione che genera lo scheletro iniziale
        column.operator(ButtonOperator.bl_idname, text="Parent", icon='OUTLINER_OB_ARMATURE').property = -1 #Valore per chiamare la funzione che imparente lo scheletro alla mesh
        column.operator(ButtonOperator.bl_idname, text="warm_up", icon='SPHERE').property = 0 #Tutti i numeri da 0 a 11 corrispondono ad una animazione [i.e. jump, walk ... ]
        column.operator(ButtonOperator.bl_idname, text="walk", icon='SPHERE').property = 1
        column.operator(ButtonOperator.bl_idname, text="run", icon='SPHERE').property = 2
        column.operator(ButtonOperator.bl_idname, text="jump", icon='SPHERE').property = 3
        column.operator(ButtonOperator.bl_idname, text="drink", icon='SPHERE').property = 4
        column.operator(ButtonOperator.bl_idname, text="lift_dumbbell", icon='SPHERE').property = 5
        column.operator(ButtonOperator.bl_idname, text="sit", icon='SPHERE').property = 6
        column.operator(ButtonOperator.bl_idname, text="eat", icon='SPHERE').property = 7
        column.operator(ButtonOperator.bl_idname, text="turn steering wheel", icon='SPHERE').property = 8
        column.operator(ButtonOperator.bl_idname, text="phone", icon='SPHERE').property = 9
        column.operator(ButtonOperator.bl_idname, text="boxing", icon='SPHERE').property = 10
        column.operator(ButtonOperator.bl_idname, text="throw", icon='SPHERE').property = 11



_classes = [
    ButtonOperator,
    CustomPanel
]

def register():
    for cls in _classes:
        register_class(cls)


def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()

