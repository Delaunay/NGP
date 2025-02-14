extends Node3D


@onready
var Camera = $MovableCamera

@onready
var RightEye = $MovableCamera/RightEye

@onready
var MidEye = $MovableCamera/MiddleEye

@onready
var LeftEye = $MovableCamera/LeftEye

@onready
var PersonAnim = $Person/AnimationPlayer

@onready
var PersonSkel = $Person/Skeleton3D

var Rotation = 2
var cnt = 0
var mx = 20


func capture_camera_image(viewport, filename: String):
	# viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	await get_tree().process_frame
	
	var image = viewport.get_texture().get_image()  # Capture the image
	# image.flip_y()  								  # Flip it (Godot’s Y-axis is inverted)
	image.save_png("user://%s.png" % filename)  	  # Save the image


func get_skeleton_transforms(skeleton: Skeleton3D) -> Dictionary:
	var bone_transforms = {}

	for i in range(skeleton.get_bone_count()):
		var bone_name = skeleton.get_bone_name(i)
		var bone_transform = skeleton.get_bone_global_pose(i)  # Get global transformation
		bone_transforms[bone_name] = bone_transform

	return bone_transforms


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	MidEye.current = true
	
	# HERE select which animation to play
	# Open a wire to configure the input and send back information
	PersonAnim.play("Z2")
	
	capture_camera_image(RightEye.get_viewport(), "right_%d" % (cnt))
	capture_camera_image(MidEye.get_viewport(), "mid_%d" % (cnt))
	capture_camera_image(LeftEye.get_viewport(), "left_%d" % (cnt))
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	Camera.rotate_y(delta * Rotation)
	
	if PersonAnim.is_playing():
		# Here extract the features
		#	and send them back through the wire
		cnt += 1
		capture_camera_image(RightEye.get_viewport(), "right_%d" % (cnt))
		capture_camera_image(MidEye.get_viewport(), "mid_%d" % (cnt))
		capture_camera_image(LeftEye.get_viewport(), "left_%d" % (cnt))
		
		print(get_skeleton_transforms(PersonSkel))
