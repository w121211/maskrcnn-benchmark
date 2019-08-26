import os
from maskrcnn_benchmark.data.datasets.coco import COCODataset

dataset = COCODataset(
    "./my_dataset/train/instances_post_train2018.json",
    "./my_dataset/train/images",
    True,
)

# boxlist = dataset[0]
# print(boxlist.bbox)

# boxlist = dataset[1][1]
# print(boxlist.bbox)
