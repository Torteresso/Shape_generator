from math import cos, sin, radians, sqrt, atan2, degrees
from random import randint


class Figure:

    def __init__(self, name, lenght, turtle, n_centers=4, weights=None, fictive=False):
        self.name = name

        self.fictive = fictive
        self.n_centers = n_centers
        self.centers_positions = self.get_centers_pos()
        self.current_center_index = 0
        self.center = self.centers_positions[self.current_center_index]

        self.lenght = lenght
        self.turtles = [turtle.clone() for _ in range(len(self.centers_positions))]
        self.t = turtle.clone()

        self.points = self.get_points_from_name()
        self.previous_set_of_points = []

        if weights is None:
            self.weights = [randint(5, 20) for i in range(len(self.points))]
            # self.weights = [10, 15, 10, 15, 10, 15, 10, 15]
        else:
            self.weights = weights

        self.weights_to_add = []
        self.previous_set_of_weights = []

        self.generation = 1

        self.current_color = randint(0, 255), randint(0, 255), randint(0, 255)

        self.area = compute_area(self.points, self.center)

    def get_centers_pos(self):
        n = self.n_centers
        centers_pos = []
        for i in range(n, 0, -1):
            xn = 300*cos(radians(i * 360 / n))
            yn = 300*sin(radians(i * 360 / n))
            centers_pos.append((xn, yn))
        return centers_pos

    def get_points_from_name(self):
        if self.name == "square":
            return [(self.center[0] - self.lenght / 2, self.center[1] - self.lenght / 2),
                    (self.center[0] + self.lenght / 2, self.center[1] - self.lenght / 2),
                    (self.center[0] + self.lenght / 2, self.center[1] + self.lenght / 2),
                    (self.center[0] - self.lenght / 2, self.center[1] + self.lenght / 2)]
        elif "polygon" in self.name:
            n = int(self.name.split("-")[0])
            if n <= 2:
                raise Exception("Un polygon ne peut pas avoir moins de 3 côtés")
            points = []
            for i in range(n):
                xn = self.center[0] + self.lenght * cos(radians(i * 360 / n))
                yn = self.center[1] + self.lenght * sin(radians(i * 360 / n))
                points.append((xn, yn))
            return points
        elif "random" in self.name:
            n = int(self.name.split("-")[0])
            if n <= 2:
                raise Exception("Un polygon ne peut pas avoir moins de 3 côtés")
            points = []

            angles = []
            for i in range(n):
                different = False
                while not different:
                    angle = randint(0, 359)
                    if angle not in angles:
                        different = True
                        angles.append(angle)

            angles.sort()

            lenghts = [randint(self.lenght/2, self.lenght*3/2) for _ in range(n)]

            for l, angle in zip(lenghts, angles):
                xn = self.center[0] + l * cos(radians(angle))
                yn = self.center[1] + l * sin(radians(angle))
                points.append((xn, yn))
            return points
        else:
            raise Exception("Le type de figure '" + self.name + "' n'est pas supporté")


    def evolve(self, primitive=False, conserve_area=True):
        self.draw(fill=True, color=self.current_color, offset=(-self.center[0], -self.center[1]))
        self.draw_weights(offset=(-self.center[0], -self.center[1]))

        if not primitive:
            self.t = self.turtles[self.current_center_index]

            while not self.is_stable() and self.generation < 1000:
                n = self.generation - 1
                if n % 7 == 0:
                    self.t = self.t.clone()
                    off_set1 = (-580 - self.center[0], 340 - n//7* 50 - self.center[1])
                    self.resize(3)
                    self.draw(fill=True, color=self.current_color, offset=off_set1)
                    self.resize(1/3)
                    self.t = self.turtles[self.current_center_index]
                self.draw(fill=True, color=self.current_color, clear=True)
                self.draw_weights()
                self.go_to_next_generation(conserve_area)

            if self.is_stable():
                pass
            else:
                print("\nThis figure '", self.name, "' might not be stable", self.previous_set_of_weights[0], self.weights)

    def draw(self, fill=False, color=None, clear=False, offset=(0, 0)):
        if self.fictive:
            return None
        if clear:
            self.turtles[self.current_center_index].clear()
        if color is None:
            color = randint(0, 255), randint(0, 255), randint(0, 255)
        self.t.pencolor(color)
        self.t.fillcolor(color)
        self.current_color = color
        if fill:
            self.t.begin_fill()
        self.t.penup()
        for p in self.points:
            p_tild = (p[0] + offset[0], p[1] + offset[1])
            self.t.goto(p_tild)
            self.t.pendown()
        self.t.goto((self.points[0][0] + offset[0], self.points[0][1] + offset[1]))
        if fill:
            self.t.end_fill()

    def draw_weights(self, offset=(0, 0)):
        if self.fictive:
            return None
        mid_points = self.get_mid_points()
        weights_ends = self.get_weights_end()
        for mid_p, w_end in zip(mid_points, weights_ends):
            mid_p_tild = (mid_p[0] + offset[0], mid_p[1] + offset[1])
            w_end_tild = (w_end[0] + offset[0], w_end[1] + offset[1])
            draw_segment(self.t, mid_p_tild, w_end_tild)

    def get_weights_end(self):
        weights_ends = []

        mid_points = self.get_mid_points()
        relat_centers = self.get_relative_centers()

        for mid_p, relat_c, w in zip(mid_points, relat_centers, self.weights):
            if isinstance(w, float) or isinstance(w, int):
                weights_ends.append(get_segment_end_from_line(relat_c, mid_p, mid_p, w))
            else:
                weights_ends.append(None)

        return weights_ends

    def get_relative_centers(self):
        relat_centers = []
        for i in range(len(self.points)):
            if i + 1 == len(self.points):
                relat_centers.append(get_segment_relative_center(self.points[i],
                                                                 self.points[0], self.center))
            else:
                relat_centers.append(get_segment_relative_center(self.points[i],
                                                                 self.points[i + 1], self.center))

        return relat_centers

    def get_mid_points(self):
        mid_points = []
        for i in range(len(self.points)):
            if i + 1 == len(self.points):
                mid_points.append(get_bisector(self.points[i], self.points[0]))
            else:
                mid_points.append(get_bisector(self.points[i], self.points[i + 1]))

        return mid_points

    def get_next_segments_intersections(self):
        points_tild = self.points.copy()
        w_end_tild = self.get_weights_end()

        segments_info = []

        for i in range(len(points_tild)):
            if isinstance(self.weights[i], float) or isinstance(self.weights[i], int):
                if i == len(points_tild) - 1:
                    i_next = 0
                else:
                    i_next = i + 1
                segments_info.append(([points_tild[i], points_tild[i_next]], w_end_tild[i], i))

        segments_info.insert(0, segments_info[-1])

        intersections = []
        for i_s in range(len(segments_info) - 1):
            A = segments_info[i_s][0][0]
            B = segments_info[i_s][0][1]
            w_end_AB = segments_info[i_s][1]

            C = segments_info[i_s + 1][0][0]
            D = segments_info[i_s + 1][0][1]
            w_end_CD = segments_info[i_s + 1][1]

            u1 = (w_end_AB[0] - get_bisector(A, B)[0], w_end_AB[1] - get_bisector(A, B)[1])
            u2 = (w_end_CD[0] - get_bisector(C, D)[0], w_end_CD[1] - get_bisector(C, D)[1])

            A_tild = (A[0] + u1[0], A[1] + u1[1])
            C_tild = (C[0] + u2[0], C[1] + u2[1])

            if is_line_intersecting_segment(A_tild, w_end_AB, w_end_CD, get_bisector(C, D)):
                i_to_remove = segments_info[i_s + 1][2]
                self.weights[i_to_remove] = [self.get_mid_points()[i_to_remove], self.get_weights_end()[i_to_remove]]
                return self.get_next_segments_intersections()

            if is_line_intersecting_segment(C_tild, w_end_CD, w_end_AB, get_bisector(A, B)):
                i_to_remove = segments_info[i_s][2]
                self.weights[i_to_remove] = [self.get_mid_points()[i_to_remove], self.get_weights_end()[i_to_remove]]
                return self.get_next_segments_intersections()

            x = None
            if abs((B[0] - A[0])) < 1e-6:
                x = w_end_AB[0]
                a1 = None
            else:
                a1 = (B[1] - A[1])\
                 /(B[0] - A[0])
                b1 = w_end_AB[1] - a1 * w_end_AB[0]
            if abs((D[0] - C[0])) < 1e-6:
                x = w_end_CD[0]
                a2 = None
            else:
                a2 = (D[1] - C[1])\
                 /(D[0] - C[0])
                b2 = w_end_CD[1] - a2 * w_end_CD[0]

            if a1 is not None and a2 is not None:
                if abs(a1 - a2) < 1e-6:

                    old_i1 = segments_info[i_s][2] + 1
                    if old_i1 >= len(self.weights):
                        old_i1 = 0
                    old_i2 = segments_info[i_s + 1][2] - 1
                    if old_i2 < 0:
                        old_i2 = len(self.weights) - 1

                    p1_1 = self.weights[old_i1][0]
                    p1_2 = self.weights[old_i1][1]

                    x1 = None
                    if abs(p1_1[0] - p1_2[0]) < 1e-6:
                        x1 = p1_1[0]
                    else:
                        a11 = (p1_1[1] - p1_2[1])/(p1_1[0] - p1_2[0])
                        b11 = p1_1[1] - a11*p1_1[0]

                    p2_1 = self.weights[old_i2][0]
                    p2_2 = self.weights[old_i2][1]

                    x2 = None
                    if abs(p2_1[0] - p2_2[0]) < 1e-6:
                        x2 = p2_1[0]
                    else:
                        a22 = (p2_1[1] - p2_2[1])/(p2_1[0] - p2_2[0])
                        b22 = p2_1[1] - a22*p2_1[0]

                    if x1 is None:
                        x1 = (b1 - b11)/(a11 - a1)
                    if x2 is None:
                        x2 = (b2 - b22)/(a22 - a2)

                    y1 = a1 * x1 + b1
                    y2 = a2 * x2 + b2

                    intersections.append((x1, y1))
                    intersections.append((x2, y2))
                    self.weights_to_add.append((old_i1, (self.weights[old_i1 - 1] + self.weights[old_i2 + 1])/2))
                    continue

            if x is None:
                x = (b2 - b1)/(a1 - a2)

            if a1 is None and a2 is None:
                x1 = w_end_AB[0]
                x2 = w_end_CD[0]

                old_i1 = segments_info[i_s][2] + 1
                old_i2 = segments_info[i_s + 1][2] - 1

                p1_1 = self.weights[old_i1][0]
                p1_2 = self.weights[old_i1][1]
                a11 = (p1_1[1] - p1_2[1])/(p1_1[0] - p1_2[0])
                b11 = p1_1[1] - a11*p1_1[0]

                p2_1 = self.weights[old_i2][0]
                p2_2 = self.weights[old_i2][1]
                a22 = (p2_1[1] - p2_2[1])/(p2_1[0] - p2_2[0])
                b22 = p2_1[1] - a22*p2_1[0]

                y1 = a11 * x1 + b11
                y2 = a22 * x2 + b22

                intersections.append((x1, y1))
                intersections.append((x2, y2))
                continue

            elif a1 is None:
                y = a2 * x + b2
            else:
                y = a1 * x + b1

            intersections.append((x, y))

        return intersections

    def get_next_points(self):
        points_tild = self.get_next_segments_intersections()
        # points_tild.insert(0, points_tild[-1])
        #
        # for i_p in range(len(points_tild) - 1):
        #     p1 = (points_tild[i_p][0] - self.center[0],
        #           points_tild[i_p][1] - self.center[1])
        #     p2 = (points_tild[i_p + 1][0] - self.center[0],
        #           points_tild[i_p + 1][1] - self.center[1])
        #     dot = p1[0] * p2[0] + p1[1] * p2[1]
        #     det = p1[0] * p2[1] - p1[1] * p2[0]
        #     angle = atan2(det, dot)
        #     if angle < 0:
        #         pass
        #         if i_p - 1 < 0:
        #             i_to_remove = len(self.weights)
        #         else:
        #             i_to_remove = i_p - 1
        #         print("ANGLEEEE", angle, i_to_remove, self.weights)
        #         self.weights[i_to_remove] = [self.get_mid_points()[i_to_remove], self.get_weights_end()[i_to_remove]]
        #         return self.get_next_points()
        #
        # points_tild.pop(0)
        return points_tild

    def replace_points(self):
        self.previous_set_of_points.append(self.points.copy())
        self.previous_set_of_weights.append(self.weights.copy())
        self.points = self.get_next_points()

    def go_to_next_generation(self, conserve_area):
        self.replace_points()
        self.draw()
        if conserve_area:
            factor = sqrt(compute_area(self.points, self.center)/self.area)
            self.resize(factor)
        self.next_center_position()
        self.update_properties()
        self.generation += 1

    def next_center_position(self):
        if self.current_center_index == len(self.centers_positions) - 1:
            next_center_index = 0
        else:
            next_center_index = self.current_center_index + 1

        u = (self.centers_positions[next_center_index][0] - self.center[0],
             self.centers_positions[next_center_index][1] - self.center[1])

        for i_p in range(len(self.points)):
            p = self.points[i_p]
            self.points[i_p] = (p[0] + u[0], p[1] + u[1])

        self.t = self.turtles[next_center_index]

        self.center = self.centers_positions[next_center_index]
        self.current_center_index = next_center_index

        # If distance between every two points don't vary over generation, it's stable
        def check_if_solution_stable(self):
            pass

    def update_properties(self):
        self.area = compute_area(self.points, self.center)

        new_weights = []
        for i in range(len(self.weights)):
            if isinstance(self.weights[i], float) or isinstance(self.weights[i], int):
                new_weights.append(self.weights[i])

        for i, w in self.weights_to_add:
            new_weights.insert(i, w)

        self.weights = new_weights

    def resize(self, factor):
        new_points = []
        for i_p in range(len(self.points)):
            p_centered = (self.points[i_p][0] - self.center[0], self.points[i_p][1] - self.center[1])
            p_resized= (p_centered[0]/factor, p_centered[1]/factor)
            p_uncentered = (p_resized[0] + self.center[0], p_resized[1] + self.center[1])
            new_points.append(p_uncentered)

        self.points = new_points

    def is_stable(self):
        if self.generation > 1:
            if len(self.points) != len(self.previous_set_of_points[self.generation - 2]):
                return False

            for p1, previous_p1 in zip(self.points, self.previous_set_of_points[self.generation - 2]):
                for p2, previous_p2 in zip(self.points, self.previous_set_of_points[self.generation - 2]):
                    if p1 != p2:
                        d = dist(p1, p2)
                        previous_d = dist(previous_p1, previous_p2)
                        if not abs(d - previous_d) < 1e-6:
                            return False

            return True
        else:
            return False

def compute_area(points, center):
    area = 0
    for i_p in range(len(points) - 1):
        area += compute_triangle_area(points[i_p], points[i_p + 1], center)

    area += compute_triangle_area(points[-1], points[0], center)

    return area


def compute_triangle_area(p1, p2, p3):
    if abs(p1[0] - p2[0]) < 1e-6:
        h_x = p1[0]
        h_y = p3[1]
    else:
        a = (p1[1] - p2[1])/(p1[0] - p2[0])
        b = p1[1] - a * p1[0]

        num = (p2[0] - p1[0])*p3[0] + (p2[1] - p1[1])*(p3[1] - b)
        denum = p2[0] - p1[0] + a * (p2[1] - p1[1])
        h_x = num / denum
        h_y = a * h_x + b

    h = dist((h_x, h_y), p3)
    base = dist(p1, p2)

    return base * h / 2


def dist(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def get_bisector(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def draw_segment(t, p1, p2):
    t.penup()
    t.goto(p1)
    t.pendown()
    t.goto(p2)


def is_line_intersecting_segment(p1, p2, A, B):
    x1, x2 = None, None
    if abs((p1[0] - p2[0])) < 1e-6:
        x1 = p1[0]
    else:
        a1 = (p1[1] - p2[1])/(p1[0] - p2[0])
        b1 = p1[1] - a1 * p1[0]

    if abs((B[0] - A[0])) < 1e-6:
        x2 = A[0]
    else:
        a2 = (B[1] - A[1])/(B[0] - A[0])
        b2 = A[1] - a2 * A[0]

    if x1 is not None and x2 is not None:
        return False
    elif x1 is None and x2 is None:
        if abs(a1 - a2) < 1e-6:
            return False
        else:
            x = (b2 - b1)/(a1 - a2)
            y = a1 * x + b1
    elif x1 is None:
        x = x2
        y = a1 * x + b1
    else:
        x = x1
        y = a2 * x + b2

    x_min = min(A[0], B[0]) - 1e-6
    x_max = max(A[0], B[0]) + 1e-6

    y_min = min(A[1], B[1]) - 1e-6
    y_max = max(A[1], B[1]) + 1e-6

    if x_min <= x <= x_max and y_min <= y <= y_max:
        return True
    else:
        return False


# the segment is oriented from P1 to P2, start from P0 and has length l
def get_segment_end_from_line(p1, p2, pi, lenght):
    # y = ax + b
    if abs(p2[0] - p1[0]) < 1e-6:
        if dist((pi[0], pi[1] + lenght), pi) >= dist((pi[0], pi[1] + lenght), p1)\
                or dist((pi[0], pi[1] + lenght), p1) <= dist(pi, p1):
            return pi[0], pi[1] - lenght
        else:
            return pi[0], pi[1] + lenght
    else:
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])

    dx = sqrt((lenght ** 2) / (1 + a ** 2))
    dy = a * dx

    if dist((pi[0] + dx, pi[1] + dy), pi) >= dist((pi[0] + dx, pi[1] + dy), p1)\
            or dist((pi[0] + dx, pi[1] + dy), p1) <= dist(pi, p1):
        pf = (pi[0] - dx, pi[1] - dy)
    else:
        pf = (pi[0] + dx, pi[1] + dy)

    return pf


# intersection entre la bisectrice d'un segment et la droite
# passant par l'origine qui est perpendiculaire à la bisectrce
def get_segment_relative_center(p1, p2, center):
    if abs(p2[0] - p1[0]) < 1e-6:
        return center[0], get_bisector(p1, p2)[1]
    else:
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = center[1] - a * center[0]

    # |P1M| = |P2M|
    x = (p2[0] ** 2 + p2[1] ** 2 - p1[0] ** 2 - p1[1] ** 2 - 2 * b * (p2[1] - p1[1])) / (
                2 * (p2[0] - p1[0]) + 2 * a * (p2[1] - p1[1]))

    y = a * x + b

    return x, y


def draw_random_polygon(t, nbr):
    for i in range(nbr):
        pol = Figure(str(randint(3, 10)) + "polygon", randint(-200, 200),
                     randint(-200, 200), randint(30, 100), t)
        pol.draw()
        pol.draw_weights()
