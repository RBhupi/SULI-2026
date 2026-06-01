# Self-Supervised Vision Transformers for Cloud segmentation and characterization Cloud-DINO

PyTorch implementation for Cloud-DINO.

This project is based in the [original DINO](https://github.com/facebookresearch/dino) repository by [Facebook AI research group](https://ai.facebook.com/).

## For training Cloud-DINO

`python3 -m torch.distributed.launch --nproc_per_node=1 cloud_dino_training.py --data_path /path/to/your/sky_images/ --output_dir /path/to/your/model/ --use_fp16 false`

## Running inference to obtain Cloud-DINO's features

`python3 -m torch.distributed.launch --nproc_per_node=1 cloud_dino_inference.py --data_path /path/to/your/sky_images/ --pretrained_weights /path/to/your/model/checkpoint0000.pth --dump_features /path/to/your/features/`

## Running associative inference to obtain Cloud-DINO's features and their respective file input names

Here we are truncating the inference ptocess to only 100 samples. That means that after the first 100 samples the inference process will be stoped.

`python3 -m torch.distributed.launch --nproc_per_node=1 cloud_dino_associative_inference.py --data_path /path/to/your/sky_images/ --pretrained_weights /path/to/your/model/checkpoint0000.pth --dump_features /path/to/your/features/ --inference_up_to 100`

## Training Cloud-DINO in a node on 8 GPUs

To run it during 10 min do

`qsub -n 1 -q full-node -t 10 -A your_project ./train_Cloud_DINO.sh`

This is the `train_Cloud_DINO.sh` script for training Cloud-DINO in a node with 8 GPUs

```
#!/bin/sh

# Common paths
sky_images_path='/sky/images/path'
singularity_image_path='/path/to/the/singularity/container/your_singularity_image_file.sif'
cloud_dino_path='/path/to/cloud_dino'
train_cloud_dino_path='/path/to/cloud_dino/cloud_dino_training.py'
model_path='/path/to/the/model'

cd $cloud_dino_path
singularity exec --nv -B $sky_images_path:/Sky_Images $singularity_image_path python -m torch.distributed.launch --nproc_per_node=8 $train_cloud_dino_path --arch vit_small --data_path /Sky_Images --output_dir $model_path
```


## Inferencing using a Cloud-DINO trained model on 8 GPUs

To run it during 10 min do

`qsub -n 1 -q full-node -t 10 -A your_project ./inference_Cloud_DINO.sh`

This is the `inference_Cloud_DINO.sh` script for making inference on Cloud-DINO in a node with 8 GPUs

```
#!/bin/sh

# Common paths
sky_images_path='/sky/images/path'
singularity_image_path='/path/to/the/singularity/container/your_singularity_image_file.sif'
cloud_dino_path='/path/to/cloud_dino'
inference_cloud_dino_path='/path/to/cloud_dino/cloud_dino_inference.py'
model_path='/path/to/the/model/checkpoint0000.pth'
output_path='/path/to/output/features'

cd $dino_path
singularity exec --nv -B $sky_images_path:/Sky_Images $singularity_image_path python -m torch.distributed.launch --nproc_per_node=8 $inference_cloud_dino_path --data_path /Sky_Images --pretrained_weights $model_path --dump_features $output_path
```


## For visualizing attention maps

For attention maps visualiztions, run the following command

`python3 visualize_attention.py --pretrained_weights /path/to/your/pretrained/weights/checkpoint.pth --image_path /path/to/the/image.jpg --image_size size_of_the_image --output_dir /where/to/save/the/maps/ --threshold (a number between 0 and 1) --patch_size 8-16`
