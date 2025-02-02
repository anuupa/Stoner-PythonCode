# -*- coding: utf-8 -*-
"""Stiner.Image.folders test
"""

from Stoner import Data
from Stoner.Image import ImageArray, ImageFolder, ImageStack
import numpy as np
import matplotlib.pyplot as plt
import pytest
from os import path
import os
import re

knownkeys = ['Averaging', 'Comment:', 'Contrast Shift', 'HorizontalFieldOfView',
             'Lens', 'Loaded from', 'Magnification', 'MicronsPerPixel', 'field: units',
             'field: units', 'filename', 'subtraction']
knownfieldvals = [-233.432852, -238.486666, -243.342465, -248.446173,
                  -253.297813, -258.332918, -263.340476, -268.20511]

testdir=os.path.join(os.path.dirname(__file__),"coretestdata","testims")
fldr=ImageFolder(testdir, pattern="*.png")


def test_load():
    fldr=ImageFolder(testdir, pattern="*.png")
    assert len(fldr)==len(os.listdir(testdir)), "Didn't find all the images"
    stack=fldr.as_stack()
    assert len(stack)==len(fldr),"Conversion to ImageStack with as_stack() failed to preserve length"

def test_properties():
    fldr=ImageFolder(testdir, pattern="*.png")
    assert fldr.size==(512, 672),f"fldr.size incorrect at {fldr.size}"
    empty=ImageFolder()
    assert empty.size==tuple(),f"Empty folder.size wrong at {empty.size}"
    fldr[1]=fldr[1].crop(4)
    assert not fldr.size,f"fldr.size didn't return False for non-uniform images, got {fldr.size}"
    for im in fldr.images:
        assert isinstance(im,ImageArray),"fldr.images returned something that wasn't an image array"

def test_methods():
    fldr=ImageFolder(testdir, pattern=re.compile(r"000_field(?P<Field>\d+)_run0.*png"))
    assert len(list(fldr.loaded))==0,"ImageFolder got loaded unexpectedly!"
    fldr.loadgroup()
    assert len(list(fldr.loaded))==8,"ImageFolder.looadgroup() failed to load!"
    fldr.montage(title="Image {Field}mT")
    assert len(plt.get_fignums())==1,"Failed to create correct number of figures with fldr.montage"
    plt.close("all")
    av=fldr.average(_metadata="common")
    std=fldr.stddev(weights=np.ones(8))
    assert av.max()==65535.0
    assert av.min()==0
    assert std.max()>449
    assert std.min()==0





if __name__=="__main__":
    pytest.main(["--pdb",__file__])
