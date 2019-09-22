from __future__ import absolute_import

import glob
import random
from abc import ABC, abstractmethod

import numpy as np
from PIL import Image, ImageDraw
from gym import spaces


class Block(ABC):
    def __init__(self):
        super(Block, self).__init__()
        self.param_space = []
        self._im = None
        self._param = None

    def _reset(self):
        self._im = None
        self._param = None

    @property
    def im(self):
        if self._im is None:
            raise Exception()
        else:
            return self._im

    def _merge_param_space(self, merge_space):
        sp = {k: fn for k, fn in merge_space}
        new = []
        for k, fn in self.param_space:
            pass

    @abstractmethod
    def sample(self, imsize):
        param = dict()
        for k, fn in self.param_space:
            param[k] = fn(param, imsize)
        self._param = param


def rgb(param, imsize):
    rgb = (param["_rgb"] * 256).astype(np.uint8)
    return tuple(rgb)


def to_imsize(key):
    def fn(param, imsize):
        p = (param[key] * imsize).astype(np.int16)
        return tuple(p)
    return fn


def wh(param, imsize):
    wh = (param["_wh"] * imsize).astype(np.int16)
    return tuple(wh)


def box(param, imsize):
    _xy = param["_cxy"] - param["_wh"] / 2
    wh = (param["_wh"] * imsize).astype(np.int16)
    xy = (_xy * imsize).astype(np.int16)
    box = np.concatenate((xy, xy + wh))
    return tuple(box)


class Rectangle(Block):
    def __init__(self):
        super(Rectangle, self).__init__()
        self.param_space = [
            ("_wh", lambda *args: np.random.normal(0.4, 0.2, 2)),
            ("_cxy", lambda *args: np.random.uniform(0, 1, 2)),
            ("_rgb", lambda *args: np.random.uniform(0, 1, 3)),
            ("rgb", rgb),
            ("box", box),
        ]

    def sample(self, imsize):
        super().sample(imsize)
        im = Image.new("RGBA", (imsize, imsize))
        draw = ImageDraw.Draw(im)
        draw.rectangle(self._param["box"], fill=self._param["rgb"], outline=None)
        self._im = im


class Photo(Block):
    def __init__(self, root):
        super(Photo, self).__init__()
        self.samples = glob.glob(root + "/*.jpg")

        self.param_space = [
            ("_wh", lambda *args: np.random.normal(0.8, 0.2, 2)),
            ("_cxy", lambda *args: np.random.uniform(0, 1, 2)),
            ("_rgb", lambda *args: np.random.uniform(0, 1, 3)),
            ("rgb", rgb),
            ("wh", to_imsize("_wh")),
            ("cxy", to_imsize("_cxy")),
            ("box", box),
            ("idx", lambda *args: np.random.randint(0, len(self.samples), 1)[0]),
        ]


    def sample(self, imsize):
        super().sample(imsize)
        print("here")
        cx, cy = self._param["cxy"]
        im = Image.new("RGBA", (imsize, imsize))
        p = Image.open(self.samples[self._param["idx"]])
        p.thumbnail(self._param["wh"])
        im.paste(p, (int(cx-p.width/2), int(cy-p.height/2)))
        self._im = im

class Text:
    pass


class Icon:
    pass


class Effect:
    pass


class Component(Block):
    pass


class Background(Block):
    def __init__(self, choices=[]):
        super().__init__(self)
        self.choices = choices
        self.param_space = [
            ("cxy", lambda acc: (0.5, 0.5)),
            ("wh", lambda acc: (1, 1)),
            ("i_bk", lambda acc: np.random.randint(0, len(choices), (1,))),
        ]

    def sample(self, imsize):
        super().sample(imsize)
        bk = self.choices[self._param["i_bk"]]
        bk.sample(imsize)
        self._im = bk.im
