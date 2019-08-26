# Docker setup

```bash
$ sudo docker build -t maskrcnn-benchmark .
$ sudo docker run --runtime=nvidia -d -it \
    --name=maskrcnn \
    -v=$(pwd):/notebooks/maskrcnn-benchmark \
    -p=8888:8888 \
    --ipc="host" \
    maskrcnn-benchmark
$ sudo docker logs maskrcnn
$ sudo docker start maskrcnn
$ sudo docker exec -it maskrcnn /bin/bash
```

- Open Jupyter notebook via [http://192.168.0.102:8888]

# Run

```bash
pip install -e .  # install current package

python tools/train_net.py --config-file "my_dataset/e2e_mask_rcnn_R_50_FPN_1x.yaml" SOLVER.IMS_PER_BATCH 4 SOLVER.BASE_LR 0.005 SOLVER.MAX_ITER 360000 SOLVER.STEPS "(240000, 320000)" TEST.IMS_PER_BATCH 1

python tools/train_net.py --config-file "my_dataset/e2e_faster_rcnn_R_50_FPN_1x.yaml" SOLVER.IMS_PER_BATCH 4 SOLVER.BASE_LR 0.005 SOLVER.MAX_ITER 360000 SOLVER.STEPS "(240000, 320000)" TEST.IMS_PER_BATCH 1
```

#
