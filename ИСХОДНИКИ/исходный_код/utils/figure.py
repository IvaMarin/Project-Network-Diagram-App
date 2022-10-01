from PyQt5.QtGui import QPainter, QColor, QBrush


class Figure:
    def __init__(self, vertex, w, h, number):
        self.vertex = vertex
        self.w = w
        self.h = h
        self.number = number
        self.links = {}

    def draw_figure(self, painter: QPainter):
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(self.vertex[0], self.vertex[1], self.w, self.h)
        painter.drawText(self.vertex[0] + 6, self.vertex[1] + 35, f"λ{self.number}")

    def add_link(self, other_figure):
        if other_figure.number != self.number and other_figure.number not in self.links:
            self.links[other_figure.number] = other_figure

    def remove_link(self, other_figure):
        if other_figure.number != self.number and other_figure.number in self.links:
            del self.links[other_figure.number]

    def draw_links(self, painter: QPainter):
        for other_figure in self.links.values():
            painter.drawLine(int(self.vertex[0] + self.w / 2), int(self.vertex[1] + self.h / 2),
                             int(other_figure.vertex[0] + other_figure.w / 2), int(other_figure.vertex[1] + other_figure.h / 2))