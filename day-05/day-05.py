# FILE_NAME = "day-05-test-input.txt"
FILE_NAME = "day-05-input.txt"


class LineSegment:
    def __init__(self, start, end):
        self.is_horizontal = False
        self.is_vertical = False

        if start[1] == end[1]:
            self.is_horizontal = True
        elif start[0] == end[0]:
            self.is_vertical = True

        # Store with 'smallest' coord as start
        points = [start, end]
        points.sort(key=lambda x: (x[0], x[1]))
        self.start = points[0]
        self.end = points[1]

    def __repr__(self):
        return f"{self.start} -> {self.end}"

    def get_coords(self):
        if self.is_horizontal:
            return [(i, self.start[1]) for i in range(self.start[0], self.end[0] + 1)]
        if self.is_vertical:
            return [(self.start[0], i) for i in range(self.start[1], self.end[1] + 1)]
        # Diagonal
        slope = (self.end[1] - self.start[1]) // (self.end[0] - self.start[0])
        num_coords = abs(self.end[1] - self.start[1]) + 1
        if slope > 0:
            return [(self.start[0] + i, self.start[1] + i) for i in range(num_coords)]
        return [(self.start[0] + i, self.start[1] - i) for i in range(num_coords)]


def get_num_dangerous_coords(include_diagonals=False):
    seen_coords = set()
    dangerous_coords = set()
    valid_segments = []

    with open(FILE_NAME) as input:
        for line in input:
            line = line.rstrip()
            tokens = line.split()
            segment_start = [int(num) for num in tokens[0].split(",")]
            segment_end = [int(num) for num in tokens[2].split(",")]
            line_segment = LineSegment(segment_start, segment_end)
            if not include_diagonals and (line_segment.is_horizontal or line_segment.is_vertical):
                valid_segments.append(line_segment)
            elif include_diagonals:
                valid_segments.append(line_segment)

    total_coords = []
    for segment in valid_segments:
        segment_coords = segment.get_coords()
        total_coords.extend(segment_coords)

    for coord in total_coords:
        if coord not in seen_coords:
            seen_coords.add(coord)
        else:
            dangerous_coords.add(coord)

    return len(dangerous_coords)


print(get_num_dangerous_coords())
print(get_num_dangerous_coords(include_diagonals=True))
