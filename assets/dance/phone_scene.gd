extends Node3D


#
#	This is used with a trained model to extract the dancer's movement
#	and compare them to the teacher.
#
#	It uses the hardware camera to capture the dancer's movement
#	use a local model in inference for extraction
#

# NOTE: add android permission request
# <uses-permission android:name="android.permission.CAMERA"/>


#func _ready():
	#var camera_count = CameraServer.get_feed_count()
	#print("Number of cameras available:", camera_count)
	#
	#if camera_count > 0:
		#var feed = CameraServer.get_feed(0)  # Get the first camera
		#var viewport = $SubViewport  # Assign to a SubViewport
		#viewport.set_camera_feed(feed)
	
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
