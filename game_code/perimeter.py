import math
from game_code.b2d import Vec2

# Class to move along the perimeter of a polygon
class Perimeter:
    @staticmethod
    def get_point(shape, percentage):
        # Get all the vertices of the shape (and repeat first one to close shape)
        vertices = [Vec2(v) for v in shape.vertices + [shape.vertices[0]]]

        # Calculate all the side lengths to find the perimeter
        side_lengths = []
        for i1 in range(0, len(vertices) - 1):
            i2 = i1 + 1
            side_lengths.append((vertices[i2] - vertices[i1]).length)
        total_perimeter = sum(side_lengths)

        # Calculate the percentages of vertices along perimeter
        side_sum = 0.0
        percentages = []
        for s in side_lengths:
            part = side_sum / total_perimeter
            side_sum += s
            percentages.append(part)
        percentages.append(side_sum / total_perimeter)

        # Find which two percentages contain the queried percentage
        indices = (0, 1)
        for index in range(0, len(percentages) - 1):
            if percentages[index] <= percentage <= percentages[index + 1]:
                indices = (index, (index + 1) % len(vertices))
                break

        # Inverse lerp the percentage to the enclosing percentages
        percentage = (percentage - percentages[indices[0]]) / (percentages[indices[1]] - percentages[indices[0]])

        # Lerp along the line segment
        return vertices[indices[0]] + (vertices[indices[1]] - vertices[indices[0]]) * percentage
