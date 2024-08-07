# CCF_translator
A tool for translating between common coordinate frameworks using deformation matrices. 
A longstanding problem in NeuroInformatics has been the inability to easily translate data between common coordinate frameworks. CCF_translator aims to solve this. By connecting each new space to an existing one, we can construct a graph of deformations. This means that as long as their is a route from one space to another, even if that is via multiple other spaces, you can translate your data. Now, when new templates for new modalities, strains, or ages are released, they will not subdivide users into unrelated spaces. As long as they are connected to a space which exists in our network they will be fully connected to all other spaces.  

CCF_translator can also interpolate between spaces and create a new intermediate space. This is primarily useful for development, where you can take the midpoint between day 5 and day 7 and use this as a post natal day 6 reference. It could also be useful for making references of disease progression.  
## Examples
**Transforming points**

To take a coordinate in one volume and find the equivalent coordinate in a second volume is quite simple in CCF_translator. 
```python
import numpy as np
import CCF_translator

points = np.array([(286,250,267), (414,247,452)])
pset = CCF_translator.pointset(points, 'demba_dev_mouse', voxel_size_micron=20, age_PND=56)
pset.transform(target_age=56, target_space='allen_mouse')
print(f"new points are {pset.values}")

```
```
new points are [[267 250 286] [452 247 414]]
 ```
**Transforming volumes**

Transforming a volume is equally simple, here we get the volume from the brainglobe api, but you can load it however you like. In the Demba space the valid ages are from 4 to 56, and all of these are valid targets for transformation. 
```python
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator


voxel_size_micron = 10
space_name = r"allen_mouse"
atlas = BrainGlobeAtlas("{space_name}_{voxel_size_micron}um")
source_age = 56
target_age= 32

CCFT_vol = CCF_translator.volume(
    values = atlas.reference,
    space = 'allen_mouse',
    voxel_size_micron=voxel_size_micron,
    segmentation_file=False,
    age_PND = source_age
)

CCFT_vol.transform(target_age, 'demba_dev_mouse')
CCFT_vol.save(rf"demo_data/P{target_age}_template_{voxel_size_micron}um.nii.gz")
```