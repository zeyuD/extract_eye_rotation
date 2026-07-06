# Extract_Eye_Rotation

## Install MPGazeII

### Tested on python=3.10

```
# Packages to install manually
pip install dlib mediapipe
```

Install MPIIFaceGaze package after making changes
```
python setup.py install
```

### Run MPIIFaceGaze demo
```
python ptgaze --config ptgaze/data/configs/mpiifacegaze.yaml
```


## Code modifications
np.float, np.int

### Modify code for torchvision new version
```
        if pretrained_name:
            # state_dict = torch.hub.load_state_dict_from_url(
            #     torchvision.models.resnet.model_urls[pretrained_name])
            model = getattr(models, pretrained_name)(pretrained=True)
            state_dict = model.state_dict()
```

### Trained MPIIFaceGaze model: 15 epochs, angle error: 1.54