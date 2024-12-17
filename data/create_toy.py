#!/usr/bin/env python3
import numpy as np
import tifffile
from tqdm import tqdm
from pathlib import Path
import json

# we create random spheres in 3D in two different classes
shape = (512, 512, 512)
array = np.zeros(shape, dtype=np.uint8)
labels = np.zeros((2,) + shape, dtype=np.uint8)
N_sphere = 100
radii = [20, 60]
p = [0.8, 0.2]
intensity = [150, 80]

metadata = {
    "pixel_nm": (4, 4, 4),
    "crops": {}
}

rng = np.random.default_rng(seed=42)
for _ in tqdm(range(N_sphere)):
    # choose class
    which_class = 0 if rng.random() < p[0] else 1
    radius = radii[which_class]

    # create sphere
    center = rng.integers(0, shape[0], size=3)
    x, y, z = np.ogrid[:shape[0], :shape[1], :shape[2]]
    mask = (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2 < radius**2
    array[mask] = intensity[which_class]
    labels[which_class, mask] = 1


# add poisson noise to array and enforce uint8
array = np.clip(rng.poisson(array), 0, 255).astype(np.uint8)

# create (128, 128, 128) crops
crop_shape = (256, 256, 256)

crops = []
crop_labels = []
for i in range(0, shape[0], crop_shape[0]):
    for j in range(0, shape[1], crop_shape[1]):
        for k in range(0, shape[2], crop_shape[2]):
            crops.append(array[i:i+crop_shape[0], j:j+crop_shape[1], k:k+crop_shape[2]])
            crop_labels.append(labels[:, i:i+crop_shape[0], j:j+crop_shape[1], k:k+crop_shape[2]])

            # update crop coordinate
            metadata["crops"][f"crop_{len(crops)-1:02d}"] = {
                "z": k,
                "y": j,
                "x": i,
            }

print(len(crops))

# save as "crop.tiff" and "labels.tiff" in different folders
root = Path(".").parent

for i, crop in enumerate(crops):
    path = root / f"crop_{i:02d}"
    path.mkdir(exist_ok=True, parents=True)

    tifffile.imwrite(path / "crop.tif", crop)
    tifffile.imwrite(path / "labels.tif", crop_labels[i])

# save metadata json
json.dump(metadata, open(root / "metadata.json", "w"), indent=4)

