import bpy
import numpy as np
from scipy.spatial.transform import Rotation as R

#Matrice utilizzata per generare lo scheletro nella posizione iniziale
m = np.array([[ -0.010841 , 0.002811 , 0.028103], #0
                    [ 0.105901 , 0.121741 , -0.005529], #1
                    [-0.132185  , 0.104118 , -0.007274], #2
                    [-0.010978 , -0.120025,  0.032688], #3
                    [ 0.134176 , 0.49215 , 0.048489], #4
                    [-0.163664  , 0.494735, 0.058614], #5
                    [-0.015607, -0.238504 , 0.022986], #6
                    [ 0.152129  , 0.878982,  0.062379], #7
                    [-0.161359 , 0.858109,  0.041475], #8
                    [ -0.017097, -0.290573 , 0.004399], #9 
                    [ 0.146699 , 0.936878 ,  -0.133373], #10
                    [-0.155459 , 0.944007 , -0.147979], #11
                    [-0.009789 , -0.530204, 0.055524], #12
                    [ 0.044454 , -0.407191, 0.009422], #13
                    [-0.08757 , -0.398985, 0.009978], #14
                    [-0.006842 , -0.65604 , 0.05962], #15
                    [ 0.131745 , -0.412095, 0.030674], #16
                    [-0.167645 , -0.403084 ,0.01388], #17
                    [ 0.409465 , -0.380316, 0.0421], #18
                    [-0.43785 , -0.383385 , 0.041222], #19
                    [ 0.631352 ,-0.371362 ,0.000769], #20
                    [-0.651008, -0.384044 , 0.008252], #21
                    [ 0.816788 ,-0.370554 , 0.000242], #22
                    [ -0.836719 ,-0.382075, -0.000779]]) #23 (inizia con 0)

#m = mo #Faccio una copia per poi ruotarla

#Inizio Rotazione degli assi
rotation_degrees = -90
rotation_radians = np.radians(rotation_degrees)
rotation_axis = np.array([1, 0, 0])
rotation_vector = rotation_radians * rotation_axis
rotation = R.from_rotvec(rotation_vector)

for i, vec in enumerate(m):

    rotated_vec = rotation.apply(vec)
    #rotated_vec[2]=rotated_vec[2]+1
    m[i] = rotated_vec
    #Fine Rotazione degli assi

#Funzione che esegue il Link dei bones con la mesh del character
def parent_skeleton():
    bpy.ops.object.mode_set(mode='OBJECT') #Entra in Object mode
    bpy.ops.object.select_all(action='SELECT') #Seleziona tutto
    #De-selaziona tutti gli empty
    bpy.data.objects["Empty"].select_set(False)
    bpy.data.objects["Empty.001"].select_set(False)
    bpy.data.objects["Empty.002"].select_set(False)
    bpy.data.objects["Empty.003"].select_set(False)
    bpy.data.objects["Empty.004"].select_set(False)
    bpy.data.objects["Empty.005"].select_set(False)
    bpy.data.objects["Empty.006"].select_set(False)
    bpy.data.objects["Empty.007"].select_set(False)
    bpy.data.objects["Empty.008"].select_set(False)
    bpy.data.objects["Empty.009"].select_set(False)
    bpy.data.objects["Empty.010"].select_set(False)
    bpy.data.objects["Empty.011"].select_set(False)
    bpy.data.objects["Empty.012"].select_set(False)
    bpy.data.objects["Empty.013"].select_set(False)
    bpy.data.objects["Empty.014"].select_set(False)
    bpy.data.objects["Empty.015"].select_set(False)
    bpy.data.objects["Empty.016"].select_set(False)
    bpy.data.objects["Empty.017"].select_set(False)
    bpy.data.objects["Empty.018"].select_set(False)
    bpy.data.objects["Empty.019"].select_set(False)
    bpy.data.objects["Empty.020"].select_set(False)
    bpy.data.objects["Empty.021"].select_set(False)
    bpy.data.objects["Empty.022"].select_set(False)
    bpy.data.objects["Empty.023"].select_set(False)

    scheletro = bpy.data.objects['Armature']
    bpy.context.view_layer.objects.active = scheletro # Rende lo scheletro un oggetto attivo

    bpy.ops.object.parent_set(type='ARMATURE_AUTO') #Link dei bones con la mesh del character

def init_skeleton():

        bpy.context.scene.cursor.location = (m[0,0], m[0,1], m[0,2]) #Muovo il cursore 3D

        # Generazione delle scheletro in posizione iniziale con le coordinate dalla matrice "m"
        bpy.ops.object.armature_add(radius=0.01, enter_editmode=False, align='CURSOR', location=(m[0,0], m[0,1], m[0,2]), scale=(0.1, 0.1, 0.11))   
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        obArm = bpy.context.active_object #Get the armature object
        
        # Inizio generazione dei bones assegnando le coordinate della testa e coda di ciascuno con le coordinate della matrice "m"
        ebs = obArm.data.edit_bones
        ebs[0].head = (m[3,0], m[3,1], m[3,2])
        eb = ebs.new("BoneName") #L'assegnazione del nome è importante per poi poter assegnare i vincoli con gli "empty"
     
        eb.head = (m[0,0], m[0,1], m[0,2]) 
        eb.tail = (m[1,0], m[1,1], m[1,2])
                  
        eb1 = ebs.new("BoneName1")
        eb1.head = (m[0,0], m[0,1], m[0,2]) 
        eb1.tail = (m[2,0], m[2,1], m[2,2])
     
        eb2 = ebs.new("BoneName2")
        eb2.head = eb.tail 
        eb2.tail = (m[4,0], m[4,1], m[4,2])

        eb3 = ebs.new("BoneName3")
        eb3.head = eb1.tail 
        eb3.tail = (m[5,0], m[5,1], m[5,2])

        eb4 = ebs.new("BoneName4")
        eb4.head = (m[6,0], m[6,1], m[6,2])
        eb4.tail = ebs[0].head
        
        eb5 = ebs.new("BoneName5")
        eb5.head = eb2.tail
        eb5.tail = (m[7,0], m[7,1], m[7,2])
        
        
        eb6 = ebs.new("BoneName6")
        eb6.head = eb3.tail
        eb6.tail = (m[8,0], m[8,1], m[8,2])
        
        eb7 = ebs.new("BoneName7")
        eb7.head =(m[9,0], m[9,1], m[9,2]) 
        eb7.tail = eb4.head
        
        eb8 = ebs.new("BoneName8")
        eb8.head = eb5.tail
        eb8.tail = (m[10,0], m[10,1], m[10,2]) 
        
        
        eb9 = ebs.new("BoneName9")
        eb9.head = eb6.tail
        eb9.tail = (m[11,0], m[11,1], m[11,2])
        
        eb10 = ebs.new("BoneName10")
        eb10.head = (m[12,0], m[12,1], m[12,2])
        eb10.tail = eb7.head
   
        eb11 = ebs.new("BoneName11")
        eb11.head = eb4.head
        eb11.tail = (m[13,0], m[13,1], m[13,2])
 
        eb12 = ebs.new("BoneName12")
        eb12.head = eb4.head
        eb12.tail = (m[14,0], m[14,1], m[14,2])
        
        eb13 = ebs.new("BoneName13")
        eb13.head = (m[15,0], m[15,1], m[15,2])
        eb13.tail = eb10.head

        eb14 = ebs.new("BoneName14")
        eb14.head = eb11.tail
        eb14.tail = (m[16,0], m[16,1], m[16,2])
        
        eb15 = ebs.new("BoneName15")
        eb15.head = eb12.tail
        eb15.tail = (m[17,0], m[17,1], m[17,2])
        
        eb16 = ebs.new("BoneName16")
        eb16.head = eb14.tail
        eb16.tail = (m[18,0], m[18,1], m[18,2])
        
        eb17 = ebs.new("BoneName17")
        eb17.head =  eb15.tail
        eb17.tail = (m[19,0], m[19,1], m[19,2])
        
        eb18 = ebs.new("BoneName18")
        eb18.head = eb16.tail
        eb18.tail = (m[20,0], m[20,1], m[20,2])
        
        eb19 = ebs.new("BoneName19")
        eb19.head = eb17.tail
        eb19.tail = (m[21,0], m[21,1], m[21,2])
        
        eb20 = ebs.new("BoneName20")
        eb20.head = eb18.tail
        eb20.tail = (m[22,0], m[22,1], m[22,2])
     
        eb21 = ebs.new("BoneName21")
        eb21.head = eb19.tail
        eb21.tail = (m[23,0], m[23,1], m[23,2])
        bpy.ops.armature.parent_set(type='CONNECTED')
        #Fine generazione dei vari bones

        #Generazione di tutti i vari "empty" nelle posizioni definite dalla matrice "m"
        bpy.ops.object.mode_set(mode='OBJECT')
        for e in range(len(m)):
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(m[e, 0], m[e, 1], m[e, 2]), scale=(1, 1, 1), radius=0.1)


        #Vincolo dei bones con gli "empty" (Qui viene sfruttato il nome dei bones assegnati precedentemente)
        ob = bpy.data.objects["Armature"]      
        bpy.ops.object.select_all(action='DESELECT') #De-seleziona tutto
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.mode_set(mode='POSE') #Passa alla modalità POSE
        
        
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['Bone'].bone #Seleziona il primo bone chiamato "Bone"
        bpy.ops.pose.constraint_add(type='COPY_LOCATION') #Attiva il primo vincolo: "COPY_LOCATION"
        bpy.context.object.pose.bones["Bone"].constraints["Copy Location"].target = bpy.data.objects["Empty.003"] #Assegna il target del vincolo. La testa del bone segue l'empty asseganto.
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK') #Attiva il secondo vincolo: "DAMPED_TRACK"
        bpy.context.object.pose.bones["Bone"].constraints["Damped Track"].target = bpy.data.objects["Empty"] #Assegna il target del vincolo. La coda del bone punta verso l'empty assegnato.
        bpy.ops.pose.constraint_add(type='STRETCH_TO') #Attiva il terzo ed ultimo vincolo: "STRETCH_TO"
        bpy.context.object.pose.bones["Bone"].constraints["Stretch To"].target = bpy.data.objects["Empty"] #Assegna il target del vincolo. Stretch del bone verso l'empty assegnato.
        
        bpy.ops.pose.select_all(action='DESELECT') #De-seleziona tutto. Il seguente codice è analogo al precedente ma lavora sul resto dei bones.
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName4'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName4"].constraints["Copy Location"].target = bpy.data.objects["Empty.006"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName4"].constraints["Damped Track"].target = bpy.data.objects["Empty.003"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName4"].constraints["Stretch To"].target = bpy.data.objects["Empty.003"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName7'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName7"].constraints["Copy Location"].target = bpy.data.objects["Empty.009"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName7"].constraints["Damped Track"].target = bpy.data.objects["Empty.006"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName7"].constraints["Stretch To"].target = bpy.data.objects["Empty.006"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName10'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName10"].constraints["Copy Location"].target = bpy.data.objects["Empty.012"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName10"].constraints["Damped Track"].target = bpy.data.objects["Empty.009"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName10"].constraints["Stretch To"].target = bpy.data.objects["Empty.009"] 
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName13'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName13"].constraints["Copy Location"].target = bpy.data.objects["Empty.015"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName13"].constraints["Damped Track"].target = bpy.data.objects["Empty.012"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName13"].constraints["Stretch To"].target = bpy.data.objects["Empty.012"] 
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName11'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName11"].constraints["Copy Location"].target = bpy.data.objects["Empty.006"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName11"].constraints["Damped Track"].target = bpy.data.objects["Empty.013"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName11"].constraints["Stretch To"].target = bpy.data.objects["Empty.013"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName14'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName14"].constraints["Copy Location"].target = bpy.data.objects["Empty.013"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName14"].constraints["Damped Track"].target = bpy.data.objects["Empty.016"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName14"].constraints["Stretch To"].target = bpy.data.objects["Empty.016"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName16'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName16"].constraints["Copy Location"].target = bpy.data.objects["Empty.016"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName16"].constraints["Damped Track"].target = bpy.data.objects["Empty.018"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName16"].constraints["Stretch To"].target = bpy.data.objects["Empty.018"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName18'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName18"].constraints["Copy Location"].target = bpy.data.objects["Empty.018"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName18"].constraints["Damped Track"].target = bpy.data.objects["Empty.020"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName18"].constraints["Stretch To"].target = bpy.data.objects["Empty.020"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName20'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName20"].constraints["Copy Location"].target = bpy.data.objects["Empty.020"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName20"].constraints["Damped Track"].target = bpy.data.objects["Empty.022"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName20"].constraints["Stretch To"].target = bpy.data.objects["Empty.022"]
    
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName12'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName12"].constraints["Copy Location"].target = bpy.data.objects["Empty.006"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName12"].constraints["Damped Track"].target = bpy.data.objects["Empty.014"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName12"].constraints["Stretch To"].target = bpy.data.objects["Empty.014"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName15'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName15"].constraints["Copy Location"].target = bpy.data.objects["Empty.014"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName15"].constraints["Damped Track"].target = bpy.data.objects["Empty.017"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName15"].constraints["Stretch To"].target = bpy.data.objects["Empty.017"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName17'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName17"].constraints["Copy Location"].target = bpy.data.objects["Empty.017"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName17"].constraints["Damped Track"].target = bpy.data.objects["Empty.019"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName17"].constraints["Stretch To"].target = bpy.data.objects["Empty.019"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName19'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName19"].constraints["Copy Location"].target = bpy.data.objects["Empty.019"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName19"].constraints["Damped Track"].target = bpy.data.objects["Empty.021"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName19"].constraints["Stretch To"].target = bpy.data.objects["Empty.021"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName21'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName21"].constraints["Copy Location"].target = bpy.data.objects["Empty.021"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName21"].constraints["Damped Track"].target = bpy.data.objects["Empty.023"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName21"].constraints["Stretch To"].target = bpy.data.objects["Empty.023"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName"].constraints["Copy Location"].target = bpy.data.objects["Empty"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName"].constraints["Damped Track"].target = bpy.data.objects["Empty.001"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName"].constraints["Stretch To"].target = bpy.data.objects["Empty.001"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName2'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName2"].constraints["Copy Location"].target = bpy.data.objects["Empty.001"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName2"].constraints["Damped Track"].target = bpy.data.objects["Empty.004"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName2"].constraints["Stretch To"].target = bpy.data.objects["Empty.004"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName5'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName5"].constraints["Copy Location"].target = bpy.data.objects["Empty.004"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName5"].constraints["Damped Track"].target = bpy.data.objects["Empty.007"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName5"].constraints["Stretch To"].target = bpy.data.objects["Empty.007"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName8'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName8"].constraints["Copy Location"].target = bpy.data.objects["Empty.007"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName8"].constraints["Damped Track"].target = bpy.data.objects["Empty.010"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName8"].constraints["Stretch To"].target = bpy.data.objects["Empty.010"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName1'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName1"].constraints["Copy Location"].target = bpy.data.objects["Empty"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName1"].constraints["Damped Track"].target = bpy.data.objects["Empty.002"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName1"].constraints["Stretch To"].target = bpy.data.objects["Empty.002"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName3'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName3"].constraints["Copy Location"].target = bpy.data.objects["Empty.002"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName3"].constraints["Damped Track"].target = bpy.data.objects["Empty.005"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName3"].constraints["Stretch To"].target = bpy.data.objects["Empty.005"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName6'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName6"].constraints["Copy Location"].target = bpy.data.objects["Empty.005"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName6"].constraints["Damped Track"].target = bpy.data.objects["Empty.008"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName6"].constraints["Stretch To"].target = bpy.data.objects["Empty.008"]
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects["Armature"].data.bones.active = bpy.data.objects["Armature"].pose.bones['BoneName9'].bone
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bpy.context.object.pose.bones["BoneName9"].constraints["Copy Location"].target = bpy.data.objects["Empty.008"]
        bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
        bpy.context.object.pose.bones["BoneName9"].constraints["Damped Track"].target = bpy.data.objects["Empty.011"]
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.context.object.pose.bones["BoneName9"].constraints["Stretch To"].target = bpy.data.objects["Empty.011"]
        
        bpy.ops.object.mode_set(mode='OBJECT') #Entra in object mode

        bpy.context.scene.cursor.location = (0, 0, 0) #Rimetto il cursore 3D a posto