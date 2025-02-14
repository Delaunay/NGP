import open3d as o3d
import numpy as np
import trimesh


# def load_mixamo_model(fbx_path):
#     # Load using trimesh (better FBX support)
#     mesh = trimesh.load(fbx_path, process=False)
    
#     # Convert to Open3D format
#     vertices = o3d.utility.Vector3dVector(mesh.vertices)
#     faces = o3d.utility.Vector3iVector(mesh.faces)

#     o3d_mesh = o3d.geometry.TriangleMesh(vertices, faces)
#     o3d_mesh.compute_vertex_normals()
#     return o3d_mesh

# def apply_pose(mesh, joint_positions):
#     """
#     Simulates applying a pose by translating the mesh.
#     joint_positions: Dict of joint names to new positions (not used yet).
#     """
#     pass

#     # transformation = np.eye(4)
#     # transformation[:3, 3] = np.array([0, 1, 0])  # Example translation
#     # mesh.transform(transformation)

# def visualize_mesh(mesh):
#     o3d.visualization.draw_geometries([mesh])

# # Load Mixamo character
# fbx_file = "G:/ngp/assets/YBot.glb"
# mesh = load_mixamo_model(fbx_file)

# # Apply pose (placeholder for later)
# apply_pose(mesh, {})

# # Visualize
# visualize_mesh(mesh)


mesh = o3d.io.read_triangle_mesh("G:/ngp/assets/YBot.glb")
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
