```bash
$ docker build -t pt-maskrcnn .
$ sudo docker run --runtime=nvidia -d -it \
    --name=ptm \
    -v=$(pwd):/maskrcnn-benchmark \
    --ipc=host \
    pt-maskrcnn
$ docker exec -it ptm /bin/bash
```