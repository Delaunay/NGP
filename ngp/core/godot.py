


import socket
import json
import struct
import base64
from PIL import Image
import torch
from io import BytesIO
import numpy as np
from sspace import Space, eq
from dataclasses import dataclass
import torchvision.transforms as transforms


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
    def __init__(self, host="127.0.0.1", port=12345, n=1000):
        self.address = (host, port)
        self.socket = None
        self.observation_space = None
        self.count = 0
        self.n = n
        self.started = False

    # def __getstate__(self):
    #     d = {
    #         "address": self.address,
    #         "count": self.count,
    #         "n": self.n,
    #     }
    #     return d

    # def __setstate__(self, d):
    #     self.address = d["address"]
    #     self.count = d["count"]
    #     self.n = d["n"]

    #     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.socket.connect(self.address)
    #     print("New connection")

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)  # Connect to Godot
        self.lists = self.get_observation_space()
        self.observation_space = self.make_sample_space(self.lists)
        self.started = True
        return self

    def __exit__(self, *args):
        self.socket.close()
        self.started = False

    def make_sample_space(self, obs_space):
        """Make the observation spac we can sample from"""
        space = Space(backend='ConfigSpace')

        space.categorical("anim_id", [anim["name"] for anim in obs_space["animations"]])
        
        space.categorical("mesh_id", obs_space["meshes"])

        space.uniform("camera_rot", lower=0, upper=360)
        return space

    def get_observation_space(self):
        send_json(self.socket, {"action": "list"})
        return receive_json(self.socket)

    def sample_space(self, seed):
        """Sample the observation space"""

        obs = {}
        for k, v in self.observation_space.sample(seed=seed + self.count)[0].items():
            # ConfigSpace give us a np.str for some reason
            if isinstance(v, str):
                v = str(v)
    
            obs[k] = v
    
        for anim in self.lists["animations"]:
            if anim["name"] == obs["anim_id"]:
                break

        space = Space(backend='ConfigSpace')
        space.uniform("anim_time", 0, anim["length"])

        for k, v in space.sample(seed=seed + self.count)[0].items():
            obs[k] = v

        self.count += 1
        return obs
    
    def __getitem__(self, idx):
        self.__enter__()
        return self.sample(idx)

    def __len__(self):
        return self.n

    def sample(self, seed=0):
        """Send a request to the game to generate the sampled observation"""
        sampled_obs = self.sample_space(seed)

        msg = {
            "action": "input", 
            **sampled_obs
            # "mesh_id": self.lists["meshes"][0], 
            # "anim_id": self.lists["animations"][1]["name"],
            # "anim_time": 0.1, 
            # "camera_rot": 45, 
        }

        send_json(self.socket, msg)
        return receive_json(self.socket)

    def __next__(self):
        return self.sample()

    @dataclass
    class Batch:
        images: dict
        bones: dict

    @staticmethod
    def collate(data):
        # batch_size = len(data)
        images = []
        target = []
        
        img_transform = transforms.Compose([
            transforms.PILToTensor(),
            transforms.ConvertImageDtype(torch.float),
        ])

        ignored_bones = {
            'mixamorig_Left_arch2', 
            'mixamorig_Left_arch1', 
            'mixamorig_LeftEye', 
            'mixamorig_RightEye', 
            'mixamorig_arrow'
        }
    
        for obs in data:
            left_eye = base64.b64decode(obs["images"]["LeftEye"])
            left = img_transform(Image.open(BytesIO(left_eye)))

            # mid_eye = base64.b64decode(obs["images"]["MidEye"])
            # mid = Image.open(BytesIO(left_eye))

            right_eye = base64.b64decode(obs["images"]["RightEye"])
            right = img_transform(Image.open(BytesIO(right_eye)))

            # 3 x H x W
            images.append(torch.cat([left, right]))

            bones = obs["bones"]
            t = []

            for name, transform in sorted(bones.items(), key=lambda item: item[0]):
                if name in ignored_bones:
                    continue
        
                x = transform["X"]
                y = transform["Y"]
                z = transform["Z"]
                o = transform["O"]

                t.append(torch.tensor(x + y + z + o))

            target.append(torch.stack(t))

        return torch.stack(images), torch.stack(target)


def display(obs):
    left_eye = base64.b64decode(obs["images"]["LeftEye"])
    image = Image.open(BytesIO(left_eye))  # Load as PIL Image
    image.show() 



if __name__ == "__main__":
    with GodotSim() as sim:
        for i in range(100):
            obs = next(sim)


    display(obs)
