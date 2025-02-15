


import socket
import json
import struct
import base64
from PIL import Image
from io import BytesIO
from sspace import Space, eq


def receive_json(sock):
    length_bytes = sock.recv(4)

    if len(length_bytes) < 4:
        raise ConnectionError("Failed to read message length")
    
    msg_length = struct.unpack("I", length_bytes)[0]
    json_bytes = sock.recv(msg_length)

    k = 0
    while len(json_bytes) < msg_length:
        json_bytes += sock.recv(msg_length - len(json_bytes))
        k += 1

    return json.loads(json_bytes.decode())


def send_json(sock, data):
    json_string = json.dumps(data)
    json_bytes = json_string.encode("utf-8")
    
    msg_length = len(json_bytes)
    length_header = struct.pack("I", msg_length) 

    sock.sendall(length_header + json_bytes)


class GodotSim:
    def __init__(self, host="127.0.0.1", port=12345):
        self.address = (host, port)
        self.socket = None
        self.observation_space = None

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)  # Connect to Godot

        self.lists = self.get_observation_space()
        self.observation_space = self.make_sample_space(self.lists)

    def __exit__(self, *args):
        self.socket.close()

    def make_sample_space(self, obs_space):
        """Make the observation spac we can sample from"""
        space = Space(backend='ConfigSpace')

        space.categorical("mesh_id", [anim["name"] for anim in obs_space["animations"]])
        
        anim_id = space.categorical("anim_id", obs_space["meshes"])

        for anim in obs_space["animations"]:
            anim_time = space.uniform("anim_time", lower=0, uper=anim["length"])
            anim_time.enable_if(eq(anim_id, anim["name"]))

        space.uniform("camera_rot", lower=0, upper=360)
        return space

    def get_observation_space(self):
        send_json(self.socket, {"action": "list"})
        return receive_json(self.socket)

    def sample_space(self):
        """Sample the observation space"""
        return self.observation_space.sample()

    def sample(self):
        """Send a request to the game to generate the sampled observation"""
        sampled_obs = self.sample_space()

        print(sampled_obs)

        send_json(self.socket, {
            "action": "input", 
            "mesh_id": self.lists["meshes"][0], 
            "anim_id": self.lists["animations"][1]["name"],
            "anim_time": 0.1, 
            "camera_rot": 45, 
        })

        return receive_json(self.socket)

    def __next__(self):
        return self.sample()



def display(obs):
    left_eye = base64.b64decode(obs["images"]["LeftEye"])
    image = Image.open(BytesIO(left_eye))  # Load as PIL Image
    image.show() 



with GodotSim() as sim:
    obs = next(sim)

display(obs)
