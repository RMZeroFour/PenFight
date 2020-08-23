from game_code.b2d import Vec2


# Class to Lerp along the perimeter of a polygon
class Perimeter:
    @staticmethod
    def get_point(shape, percentage):
        # Get all the vertices of the shape
        vertices = [Vec2(v) for v in shape.vertices]

        # Calculate all the side lengths and perimeter
        side_lengths = []
        for i1 in range(0, len(vertices)):
            i2 = (i1 + 1) % len(vertices)
            side_lengths.append((vertices[i2] - vertices[i1]).length)
        total_perimeter = sum(side_lengths)

        # Find out how long the lerped part is
        part_of_perimeter = percentage * total_perimeter
        indices = (0, 1)
        for index in range(0, len(side_lengths)):
            # Keep subtracting sides until the remaining part is smaller
            if side_lengths[index] < part_of_perimeter:
                part_of_perimeter -= side_lengths[index]
            else:
                indices = (index, (index + 1) % len(side_lengths))
                break

        # Find out what part of the line segment joining the indices is the remaining part
        percentage_of_segment = part_of_perimeter / side_lengths[indices[0]]

        # Use the section formula to return the coords
        return (vertices[indices[1]] * percentage_of_segment + vertices[indices[0]]) / (percentage_of_segment + 1)
