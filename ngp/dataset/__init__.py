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

class ModelNet40:
    # https://modelnet.cs.princeton.edu/
    
    URL = "http://modelnet.cs.princeton.edu/ModelNet40.zip"



class ShapeNet:
    # https://shapenet.org/
    pass


class Redwood3DScan:
    # https://github.com/isl-org/redwood-3dscan
    pass


class ObjectNet3D:
    pass