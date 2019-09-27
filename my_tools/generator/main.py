from __future__ import absolute_import

import os
import random

from PIL import Image

from config import get_parameters
import blocks as bk


class Sampler:
    def __init__(self, blocks, opt):
        self.blocks = blocks
        self.imsize = opt.imsize

    def sample(self):
        im = Image.new("RGBA", (self.imsize, self.imsize))
        anns = dict()

        for bk in self.blocks:
            bk.sample(self.imsize)
            im.alpha_composite(bk.im)
            for k, v in bk.annotations:
                anns.setdefault(k, []).append(v)
        return im, anns


if __name__ == "__main__":
    opt = get_parameters()

    os.makedirs(os.path.join(opt.save_to, "images"), exist_ok=True)
    os.makedirs(os.path.join(opt.save_to, "annotations"), exist_ok=True)

    rect = bk.Rectangle()
    jpg = bk.Photo("/tf/CoordConv-pytorch/data/facebook")
    text = bk.Text()
    bg = bk.Background(
        [bk.Rectangle()]
        # [bk.Rectangle(), bk.Photo("/tf/CoordConv-pytorch/data/facebook")]
    )

    samplers = [
        Sampler([bg, rect, text], opt),
        Sampler([bg, rect, rect, text], opt),
        Sampler([bg, rect, text, rect], opt),
    ]
    # samplers = [Sampler([bg, rect], opt)]

    for i in range(opt.n_samples):
        sp = random.choice(samplers)
        im, anns = sp.sample()
        im.save(os.path.join(opt.save_to, "images", "{}.png".format(i)), "PNG")

        count = 0
        for k, v in anns.items():
            for im in v:
                im.save(
                    os.path.join(
                        opt.save_to,
                        "annotations",
                        "{}_crowd_{}_{}.png".format(i, k, count),
                    ),
                    "PNG",
                )
                count += 1
