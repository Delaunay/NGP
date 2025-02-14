

SpaceMesh: A Continuous Representation for Learning Manifold Surface Meshes

=> Isotropic mesh refers to a mesh topology where the edges have consistent sizes, resulting in a uniform polygon distribution across the topology
=> geodesic distance: is a curve representing in some sense the locally[a] shortest[b] path (arc) between two points in a surface, or more generally in a Riemannian manifold.
=> half edge: edge a bi directional, half edge is one direction
=? hyperbolic embedding
=? we leverage spacetime embeddings 
=? soften permutation matrix
    - Sinkhorn's theorem states that every square matrix with positive entries can be written in a certain standard form.


# Write a 1-2 paragraph summary of the paper.

        The paper presents a model to output a mesh with its connectivity from a point cloud.
        It uses a first model to encode the point cloud into a latent vector that is later used by a diffusion model to generate the vertices.
        Finally, the last transformer model takes the generated vertices and creates a connectivity matrix.


* New mesh representation to learn to directly generate a polygon meshes
* Our key innovation is to define a continuous latent connectivity space at each mesh vertex
* This representation is well-suited to machine learning and stochastic optimization, without restriction on connectivity or topology.
* fit distributions of meshes from large datasets.
* well-suited for learning and optimization, which guarantees manifold output and supports complex polygonal connectivity.
* First paper that seems to NOT require a tesselated mesh
* Weare especially concerned with generating meshes which are not just a soup of faces, but which have coherent and consistent neighborhood connectivity.

1. constructing a set of edges and halfedges
2. then constructing the so-called next relationship among those halfedges to implicitly de fine the faces of the mesh. 


* loss
    - Distance using cross entropy loss
    - Learn the truth permutation


 In particular, here we allocate a latent code for each mesh, and
 optimize those latent codes as well as the parameters of a simple
 transformer model [Vaswani et al. 2017] that decodes each latent
 code into the mesh, in the form of per-vertex positions and con
nectivity embeddings of our representation. 


Model:

    - a point cloud encoding network for processing geometry information
    - a vertex diffusion model to generate 3D locations for vertices,
    - a connectivity prediction network to predict per-vertex embeddings


Point Could encoder => Conditioning information / Latent vector => Vertex position Generator (diffusion transformer based)

# Write down questions you have regarding the paper and that you want me to explain in class


# Write down points that you found unclear (things the authors don't do a good job of explaining)


# Think about possible caveats in the method - what are its limitations, where is it lacking? 

* The model is limited to a known object from the dataset.

* Our model learns to fit distributions of meshes; the tessellation pattern and element shapes of generated meshes will mimic the training population.

# What are alternatives to this approach that you can think of? Why haven’t they been taken?

