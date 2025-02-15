extends Node3D

#
#	This is used to train the model to extract posture from a 2D/3D image
#

@onready
var Camera = $MovableCamera

@onready
var RightEye: Camera3D = $MovableCamera/RightEye

@onready
var MidEye: Camera3D = $MovableCamera/MiddleEye

@onready
var LeftEye: Camera3D = $MovableCamera/LeftEye

@onready
var PersonAnim: AnimationPlayer = $Person/AnimationPlayer

@onready
var PersonSkel = $Person/Skeleton3D

@onready
var animationLib: AnimationLibrary = load("res://animations/AnimationLibrary.tres")

var meshes = [
	"res://s_archer.glb",
	"res://s_ybot.glb",
]

var Rotation = 2
var cnt = 0
var mx = 20
var port = 12345
var host = "127.0.0.1"

var server := TCPServer.new()
var client := StreamPeerTCP.new()
var next_action = null
var mesh = null
var current_mesh_id = null

func arguments():
	var args = OS.get_cmdline_args()


func prepare_mesh(mesh_id):
	if current_mesh_id == mesh_id:
		return 

	if mesh and is_instance_valid(mesh):
		mesh.queue_free()

	# Spawn the mesh to test
	var glb_scene = load(mesh_id)
	var instance = glb_scene.instantiate()
	instance.transform.origin = Vector3(0, 0, 0)
	instance.scale = Vector3(1, 1, 1)
	instance.visible = true
	self.add_child(instance)
	
	PersonAnim = instance.get_node("AnimationPlayer")
	PersonSkel = instance.get_node("Skeleton3D")
	PersonAnim.remove_animation_library("")
	PersonAnim.add_animation_library("", animationLib)
	
	mesh = instance
	current_mesh_id = mesh_id


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	server.listen(port)
	MidEye.current = true
	
	#var animation_names = PersonAnim.get_animation_list()
	#var anim_list = []
	#for anim_name in animation_names:
		#var animation = PersonAnim.get_animation(anim_name)
		#animationLib.add_animation(anim_name, animation)
	#
	#ResourceSaver.save(animationLib, "res://animations/AnimationLibrary.tres")
	# print(animationLib.get_animation_list())

func capture_camera_image(viewport, filename: String):
	await get_tree().process_frame
	var image = viewport.get_texture().get_image()  # Capture the image
	image.save_png("user://%s.png" % filename)  	  # Save the image


func get_skeleton_transforms(skeleton: Skeleton3D) -> Dictionary:
	var bone_transforms = {}

	for i in range(skeleton.get_bone_count()):
		var bone_name = skeleton.get_bone_name(i)
		var bone_transform = skeleton.get_bone_global_pose(i)  # Get global transformation
		bone_transforms[bone_name] = bone_transform

	return bone_transforms


func send_json(client: StreamPeerTCP, data: Dictionary):
	var json_string = JSON.stringify(data)
	var bytes = json_string.to_utf8_buffer()
	var length: int = bytes.size()

	# Ensure the endianess match
	# note that this is for training so might not be that useful
	var buffer = StreamPeerBuffer.new()
	buffer.set_big_endian(false)
	buffer.put_u32(length)
	buffer.put_data(bytes)
	
	client.put_data(buffer.data_array)


func receive_json(client: StreamPeerTCP):
	var length = client.get_u32()

	#var data: String = client.get_data(length)
	#while data.size() < length:
		#data += client.get_data(length - data.size())
	#var json = JSON.new()
	#var parse_result = json.parse(PackedByteArray(data).get_string_from_utf8())
	
	var data: String = client.get_utf8_string(length)
	while data.length() < length:
		data += client.get_utf8_string(length - data.length())
	var json = JSON.new()
	var parse_result = json.parse(data)
	if parse_result == OK:
		return json.get_data()
	else:
		print("could not parse json")
		return null


func b64_encoded_img(camera):
	var image = camera.get_viewport().get_texture().get_image()
	var buffer = image.save_png_to_buffer()
	return Marshalls.raw_to_base64(buffer)


func extract_anim_list(AnimPlayer: AnimationPlayer):
	var animation_names = animationLib.get_animation_list()
	var anim_list = []
	
	for anim_name in animation_names:
		var animation = animationLib.get_animation(anim_name)
		anim_list.append({"name": anim_name, "length": animation.length})

	return anim_list


func reply_message(client, action):
	match action:
		# Send a list of animation+meshes available
		"list":
			send_json(client, {"action": "list", "animations": extract_anim_list(PersonAnim), "meshes": meshes})
			
		# Send the input for training the network
		"input":
			send_json(client, {
				"action": "input", 
				"images": {
					"LeftEye": b64_encoded_img(LeftEye),
					"MidEye": b64_encoded_img(MidEye),
					"RightEye": b64_encoded_img(RightEye),
				}, 
				"bones": get_skeleton_transforms(PersonSkel)
			})

		"ok":
			send_json(client, {"action": "ok"})


func handle_message(client, msg):
	match msg["action"]:
		"list":
			reply_message(client, "list")

		"input":
			# Configure the environment
			set_env(msg)
			await get_tree().process_frame
			#  send back the resulting info
			reply_message(client, "input")


func set_env(msg):
	# Change the skeleton
	# ...
	prepare_mesh(msg["mesh_id"])
	
	# Change the camera distance ?
	#LeftEye.transform.origin
	#MidEye.transform.origin
	#RightEye.transform.origin

	# Add camera rot noise ?	
	PersonAnim.play(msg["anim_id"])
	
	# Set animation Time ?
	PersonAnim.seek(msg["anim_time"], true)
	PersonAnim.pause()

	# Set camera rotation ?
	Camera.rotation_degrees = Vector3(0, msg["camera_rot"], 0) 

	#var quat = Quaternion(Vector3.UP, deg_to_rad(90))  # Rotate 90° around Y-axis
	#camera.basis = Basis(quat)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if server.is_connection_available():
		client = server.take_connection()
	
	if client.get_status() == client.Status.STATUS_CONNECTED and client.get_available_bytes() > 0:
		handle_message(client, receive_json(client))
