#!/usr/bin/env python
import pygame
from xml.dom import minidom
from gameApp import GameApp, Camera
from svg.path import parse_path


class SVGDrawApp(GameApp):
    def __init__(self, svg_file):
        GameApp.__init__(self)

        doc = minidom.parse(svg_file)
        try:
            self._paths = map(
                lambda path: parse_path(path.getAttribute("d")),
                doc.getElementsByTagName("path")
            )
        finally:
            doc.unlink()

    def draw(self):
        self.display.fill((255, 255, 255))

        zoom_factor = 2
        discreet = 10

        for path in self._paths:
            for it in path:
                for i in xrange(discreet):
                    pt1 = it.point(i / float(discreet)) * zoom_factor
                    pt2 = it.point((i + 1) / float(discreet)) * zoom_factor
                    pygame.draw.aaline(self.display, (0, 0, 0), (pt1.real, pt1.imag), (pt2.real, pt2.imag))


if __name__ == "__main__":
    app = SVGDrawApp("svg/shape3.svg")
    app.startLoop()
