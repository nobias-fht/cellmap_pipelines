# Data

> [!IMPORTANT]  
> Check out [DaCapo data specifications](https://janelia-cellmap.github.io/dacapo/data.html).

Here we provide an example on how to package data as:
```
data.zarr
├── train
│   ├── crop_01
│   │   ├── raw
│   │   └── labels
│   └── crop_02
│       ├── raw
│       └── labels
└── test
    └─ crop_03
    │   ├── raw
    │   └── labels
    └─ crop_04
        ├── raw
        └── labels
```

## Create toy data

```bash
python create_toy_data.py
```


## TODO

- [ ] Understand masking