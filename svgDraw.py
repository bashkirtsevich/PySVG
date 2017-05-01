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

        zoom_factor = 4
        discreet = 10

        for path in self._paths:
            for it in path:
                points = []
                for i in xrange(discreet + 1):
                    pt1 = it.point(i / float(discreet)) * zoom_factor
                    points.append((pt1.real, pt1.imag - 200))

                pygame.draw.aalines(self.display, (100, 100, 100), False, points)


if __name__ == "__main__":
    app = SVGDrawApp("svg/shape2.svg")
    app.startLoop()
