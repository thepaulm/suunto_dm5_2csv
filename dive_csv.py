#!/usr/bin/env python

import sys
import re
import xml.etree.ElementTree as ET


class Sample(object):
    def __init__(self):
        self.depth = None
        self.time = None

    def complete(self):
        return self.depth is not None and self.time is not None

    def __str__(self):
        return "{depth: %f, time: %d}" % (self.depth, self.time)


def ename(e):
    return re.sub('{.*}', '', e.tag)


def main():
    path = sys.argv[1]
    tree = ET.parse(path)
    root = tree.getroot()
    samples_root = [e for e in root if ename(e) == 'DiveSamples']
    dss = samples_root[0]

    samples = []
    s = Sample()
    for ds in dss:
        for k in ds:
            if ename(k) == 'Depth':
                s.depth = float(k.text)
            if ename(k) == 'Time':
                s.time = int(k.text)
            if s.complete():
                samples.append(s)
                s = Sample()

    samples = sorted(samples, key=lambda s: s.time)
    for s in samples:
        print(s.time, ",", s.depth)

if __name__ == '__main__':
    main()
