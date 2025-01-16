import os
from pathlib import PurePosixPath
import zipfile

import requests
import assimp_py
from tqdm import tqdm
import vtk

# https://github.com/timzhang642/3D-Machine-Learning/tree/master
# https://cvgl.stanford.edu/resources.html

class PrincetonShapeBenchmark:
    # 500 Internal server error

    URL = "https://shape.cs.princeton.edu/benchmark/download.cgi?file=download/psb_v1.zip"
    SIZE = 1_814
    FMT = ".off"
    TASKS = ("Classification",)

    def __init__(self):
        pass

    def download(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, index):
        pass


class IKEA3D:
    pass


class OpenSurfaces:
    # http://opensurfaces.cs.cornell.edu/
    # http://opensurfaces.cs.cornell.edu/publications/opensurfaces/#download
    pass

class Pascal3D:
    # https://cvgl.stanford.edu/projects/pascal3d.html
    # ftp://cs.stanford.edu/cs/cvgl/PASCAL3D+_release1.1.zip
    pass


class SUN3D:
    # https://sun3d.cs.princeton.edu/
    pass

class NYC3DCars:
    # http://nyc3d.cs.cornell.edu/
    pass


# https://github.com/IKEA/IKEA3DAssemblyDataset



class RGBD:
    # http://michaelfirman.co.uk/RGBDdatasets/index.html
    pass


# https://modelnet.cs.princeton.edu/#
class ModelNet10:
    # 127,915 CAD Models
    # 662 Object Categories
    # 10 Categories with Annotated Orientation 
        
    """Collected 3D CAD models belonging to each object category using online search engines by querying for each object category term. Then, we hired human workers on Amazon Mechanical Turk to manually decide whether each CAD model belongs to the specified cateogries, using our in-house designed tool with quality control. To obtain a very clean dataset, we choose 10 popular object categories, and manually deleted the models that did not belong to these categories. Furthermore, we manually aligned the orientation of the CAD models for this 10-class subset as well. We provide both the 10-class subset and the full dataset for download. """
    URL = "http://3dvision.princeton.edu/projects/2014/3DShapeNets/ModelNet10.zip"

    SIZE = 12_311
    FMT = ".off"
    TASKS = ("Classification",)

    def __init__(self):
        pass

    def download(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, index):
        # scene = assimp_py.ImportFile("models/planet/planet.obj", process_flags)
        pass


class ModelNet40:
    # FIXME: keep the zipfile and just load files directly from there
    """Collected 3D CAD models belonging to each object category using online search engines
    by querying for each object category term. Then, we hired human workers on 
    Amazon Mechanical Turk to manually decide whether each CAD model belongs to the specified cateogries, 
    using our in-house designed tool with quality control. To obtain a very clean dataset, 
    we choose 10 popular object categories, and manually deleted the models that did not belong to these categories.
    Furthermore, we manually aligned the orientation of the CAD models for this 10-class subset as well. 
    We provide both the 10-class subset and the full dataset for download. 
    
    """
    URL = "http://modelnet.cs.princeton.edu/ModelNet40.zip"

    SIZE = 12_311
    FMT = ".off"
    TASKS = ("Classification",)

    def __init__(self, folder, split=None):
        self.folder = folder
        self.process_flags = (
            assimp_py.Process_Triangulate | assimp_py.Process_CalcTangentSpace
        )

        files = []
        for path, _, filenames  in tqdm(os.walk(folder)):
            for filename in filenames:
                if filename.endswith(".off"):
                    files.append(str(PurePosixPath(os.path.join(path, filename))))
                else:
                    print(f"Ignoring file {filename}")

        files.sort()

        self.cls = {}
        self.files = []
        for filename in files:
            #                       -3    -2       -1
            # PATH/ModelNet40/CLASSNAME/split/FILENAME
            frags = filename.split("/")

            cls = frags[-3]
            csplit = frags[-2]
            
            if split is not None and csplit != split:
                continue

            self.files.append({
                "path": filename,
                "classname": cls,
                "split": csplit,
                "class":  self.cls.setdefault(cls, len(self.cls))
            })

    def download(self, force=False):
        if os.path.exists(self.folder):
            if not force:
                return
            
            import shutil
            shutil.rmtree(self.folder)

        # Download
        response = requests.get(self.URL, stream=True)
        response.raise_for_status()

        dest = os.path.join(self.folder, "tmp.zip")
        with open(dest, "wb") as file:
            for chunk in tqdm(response.iter_content(chunk_size=8192)):
                file.write(chunk)
        
        # Extract
        with zipfile.ZipFile(dest, 'r') as zip_ref:
            zip_ref.extractall(self.folder)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        sample = self.files[index]

        scene = assimp_py.ImportFile(sample["path"], self.process_flags)
        cls = sample["class"]
        
        return scene, cls


# https://ranahanocka.github.io/MeshCNN/
# COSEG segmentation dataset
# Human Segmentation dataset
# Cubes classification dataset
# Shrec classification dataset


class ShapeNet:
    # https://shapenet.org/
    pass


class Redwood3DScan:
    # https://github.com/isl-org/redwood-3dscan
    pass


class ObjectNet3D:
    pass



def view_trimesh(mesh):
    import trimesh
    vertices = np.array(mesh.vertices)
    faces = np.array(mesh.indices)

    # Create a Trimesh object and visualize it
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.show()





def visualize_scene_vtk(scene):
    vertices = []
    faces = []

    for mesh in scene.meshes:
        vertices.extend(mesh.vertices) # Points / Dots of the mesh
        faces.extend(mesh.indices)     # How points are connected to form faces
                                       # This allows indices to be reused 
                                       # i.e more memory efficient

        print(mesh.vertices)
        print(mesh.indices)

    # Create VTK Points
    points = vtk.vtkPoints()
    for vertex in vertices:
        points.InsertNextPoint(*vertex)

    # Create VTK Polygons
    polygons = vtk.vtkCellArray()
    for face in faces:
        polygon = vtk.vtkPolygon()
        polygon.GetPointIds().SetNumberOfIds(len(face))
        for i, idx in enumerate(face):
            polygon.GetPointIds().SetId(i, idx)
        polygons.InsertNextCell(polygon)

    # Create VTK PolyData
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(polygons)

    # Visualize
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    render_window.Render()
    render_window_interactor.Start()


if __name__ == "__main__":
    import numpy as np

    dataset = ModelNet40("G:/ngp/data/ModelNet40")

    sample = dataset[0]
    scene = sample[0]

    visualize_scene_vtk(scene)
