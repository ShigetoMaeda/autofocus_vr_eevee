import bpy, serial, bpy_extras, math, numpy as np

ob = bpy.context.object
me = ob.data
sc = bpy.context.scene
#bpy.ops.screen.animation_play()
dancing_cat = bpy.data.objects['dancing_cat']
obj_camera = bpy.data.objects['camera_head']
#left_camera = bpy.data.objects['Left'] #for 2 cameras
right_camera = bpy.data.objects['Right']
#camera_pos = obj_camera.location
obj_camera.rotation_mode = 'XYZ'
obj_camera.rotation_euler = [math.radians(90.0), 0.0, 0.0]

right_camera.rotation_mode = 'QUATERNION'

focal_point = bpy.context.scene.objects['Focal_point']
focal_point_pos = focal_point.location
#focus_point = bpy.context.scene.objects['Focus_point']
#focus_point_pos = focus_point.location
### add
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='EMPTY')
selection_names = []
for obj in bpy.context.selected_objects:
	selection_names.append(obj.name)
itemNum = len(selection_names)
objList = selection_names

bpy.ops.object.select_all(action='DESELECT')
#obj_camera.select_set(True)
right_camera.select_set(True)
### add --

class SERIAL_OT_arduino_read(bpy.types.Operator):
	bl_idname = "serial.arduino_read"
	bl_label = "Read From Arduino"
    rx = 0 #dancing_cat rot
	def execute(self, context):
		as_bytes = self.ser.readline()
		r = as_bytes.decode('utf-8').strip()
		#print(r)
		serDataArray = [float(x.strip()) for x in r.split(',')]
		if len(serDataArray)==4:
			#obj_camera.rotation_quaternion = serDataArray
			right_camera.rotation_quaternion = serDataArray

        dancing_cat.rotation_euler = [0, 0, math.radians(self.rx)]
        self.rx = self.rx + 2

		nearObjList = []
		distList = []

		for i in range(itemNum):
			obje = bpy.data.objects[selection_names[i]]
			pos = bpy_extras.object_utils.world_to_camera_view(sc, right_camera, obje.location)
#			if pos[2] > 0 and pos[0] > 0.4 and pos[0] < 0.6 and pos[1] > 0.4 and pos[1] < 0.6:
			if pos[2] > 0 and abs(pos[0]-0.5) < 0.1 and abs(pos[1]-0.5) < 0.1:
				nearObjList.append(obje.location)
			
		for vec in nearObjList:
			camera_pos = obj_camera.location
			#print(camera_pos)
			dist = math.sqrt((vec[0] - camera_pos[0])**2 + (vec[1] - camera_pos[1])**2 + (vec[2] - camera_pos[2])**2)
			distList.append(dist)
#   	print(distList)

		if len(distList)==0:
			right_camera.data.dof.focus_distance = 100.0

		else:
			right_camera.data.dof.focus_distance = min(distList)

		return {'FINISHED'}

	def modal(self, context, event):
		if event.type == 'TIMER':
			self.execute(context)
		elif event.type == 'LEFTMOUSE':  # Confirm
			self._finish()
			return {'FINISHED'}
		elif event.type in ('ESC'):  # Cancel
			self._finish()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		#self.ser = serial.Serial("/dev/cu.usbserial-1420", 9600)
		self.ser = serial.Serial("COM5", 230400)
		self.timer = context.window_manager.event_timer_add(0.01, window=context.window)
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

	def _finish(self):
		context.window_manager.event_timer_remove(self.timer)


bpy.utils.register_class(SERIAL_OT_arduino_read)

# test call
bpy.ops.serial.arduino_read('INVOKE_DEFAULT')
