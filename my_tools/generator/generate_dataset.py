from __future__ import absolute_import

import random
import copy

from PIL import Image

from config import get_parameters
import blocks as bk


class Sampler:
    def __init__(self, blocks, opt):
        self.blocks = blocks
        self.imsize = opt.imsize
        pass

    def sample(self):
        im = Image.new("RGBA", (self.imsize, self.imsize))
        for bk in self.blocks:
            # bk.refresh()
            bk.sample()
            im = im.alpha_composite(bk.im)
            # bk.annotation.save()
        
        return im


if __name__ == "__main__":
    opt = get_parameters()

    # jpg = bk.Photo("")
    # png = bk.Photo("")  # transparent
    # bg = bk.Background([copy.deepcopy(jpg)])
    rect = bk.Rectangle()
    # text = bk.Text()

    # samplers = [Sampler([bg, rect, jpg, text], opt)]
    samplers = [Sampler([rect], opt)]
    sp.sample()

    # for i in range(opt.n_samples):
    #     sp = random.choices(samplers)
