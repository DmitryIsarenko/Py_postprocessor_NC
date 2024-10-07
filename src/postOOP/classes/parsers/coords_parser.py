import math


class CoordsParser:

    @staticmethod
    def count_A_angle_by_orts(j: float, k: float) -> float:
        angle_rot = 0
        if k == 1:  # angle 0 deg
            angle_rot = 0
        elif j < 0 and k > 0:  # angle <90 deg
            angle_rot = math.atan(abs(j) / abs(k))
        elif j == 1:  # angle 90 deg
            angle_rot = 0.5 * math.pi
        elif j < 0 and k < 0:  # angle 90 < 180 deg
            angle_rot = math.atan(abs(k) / abs(j))
            angle_rot += math.pi * 0.5
        elif k == -1:  # angle 180 deg
            angle_rot = 1 * math.pi
        elif j > 0 and k < 0:  # angle 180 < 270 deg
            angle_rot = math.atan(abs(j) / abs(k))
            angle_rot += math.pi * 1
        elif j == -1:  # angle 270 deg
            angle_rot = 1.5 * math.pi
        elif j > 0 and k > 0:  # angle > 270 deg
            angle_rot = math.atan(abs(k) / abs(j))
            angle_rot += math.pi * 1.5

        angle_rot = angle_rot * 180 / math.pi
        return round(angle_rot, ndigits=2)

    @staticmethod
    def count_B_angle_by_orts(i: float, k: float) -> float:
        angle_rot = 0
        if k == 1:  # angle 0 deg
            angle_rot = 0
        elif i > 0 and k > 0:  # angle <90 deg
            angle_rot = math.atan(abs(i) / abs(k))
        elif i == 1:  # angle 90 deg
            angle_rot = 0.5 * math.pi
        elif i > 0 and k < 0:  # angle 90 < 180 deg
            angle_rot = math.atan(abs(k) / abs(i))
            angle_rot += math.pi * 0.5
        elif k == -1:  # angle 180 deg
            angle_rot = 1 * math.pi
        elif i < 0 and k < 0:  # angle 180 < 270 deg
            angle_rot = math.atan(abs(i) / abs(k))
            angle_rot += math.pi * 1
        elif i == -1:  # angle 270 deg
            angle_rot = 1.5 * math.pi
        elif i < 0 and k > 0:  # angle > 270 deg
            angle_rot = math.atan(abs(k) / abs(i))
            angle_rot += math.pi * 1.5

        angle_rot = angle_rot * 180 / math.pi
        return angle_rot

    # def count_C_angle_by_orts(i: float, j: float) -> float:
    #     if j == 1:
    #         angle = 0
    #     elif i > 0 and j > 0:
    #         angle = math.atan(i / j)
    #     elif i == 1:
    #         angle = 0.5 * math.pi
    #     elif i > 0 and j < 0:
    #         angle = math.atan(abs(j) / i)
    #         angle += math.pi * 0.5
    #     elif j == -1:
    #         angle = 1 * math.pi
    #     elif i < 0 and j < 0:
    #         angle = math.atan(abs(i) / abs(j))
    #         angle += math.pi * 1
    #     elif i == -1:
    #         angle = 1.5 * math.pi
    #     elif i < 0 and j > 0:
    #         angle = math.atan(abs(j) / abs(i))
    #         angle += math.pi * 1.5
    #
    #     angle = angle * 180 / math.pi
    #     return angle

    @staticmethod
    def count_new_Y_Z_for_A_rotation(*, y_start: float | int,
                                     z_start: float | int,
                                     angle_A_deg: float | int) -> tuple[float | int, float | int]:
        angle_A_deg = angle_A_deg * math.pi / 180
        y_end = y_start * math.cos(angle_A_deg) + z_start * math.sin(angle_A_deg)
        z_end = z_start * math.cos(angle_A_deg) - y_start * math.sin(angle_A_deg)
        return round(y_end, ndigits=4), round(z_end, ndigits=4)

    @staticmethod
    def count_new_X_Z_for_B_rotation(*, x_start: float | int,
                                     z_start: float | int,
                                     angle_C_deg: float | int) -> tuple[float | int, float | int]:
        angle_C_deg = - angle_C_deg * math.pi / 180
        x_end = x_start * math.cos(angle_C_deg) + z_start * math.sin(angle_C_deg)
        z_end = z_start * math.cos(angle_C_deg) - x_start * math.sin(angle_C_deg)
        return round(x_end, ndigits=4), round(z_end, ndigits=4)

    @staticmethod
    def count_new_X_Y_for_C_rotation(*, x_start: float | int,
                                     y_start: float | int,
                                     angle_C_deg: float | int) -> tuple[float | int, float | int]:
        angle_C_deg = angle_C_deg * math.pi / 180
        x_end = x_start * math.cos(angle_C_deg) + y_start * math.sin(angle_C_deg)
        y_end = y_start * math.cos(angle_C_deg) - x_start * math.sin(angle_C_deg)
        return round(x_end, ndigits=4), round(y_end, ndigits=4)


if __name__ == '__main__':
    angle = count_A_angle_by_orts(j=-0.1736482, k=0.9848078)
    # angle = count_A_angle_by_orts(j=-0.9848078, k=-0.1736482)
    # angle = count_A_angle_by_orts(j=0.1736482, k=-0.9848078)
    # angle = count_A_angle_by_orts(j=0.9848078, k=0.1736482)

    # angle = count_B_angle_by_orts(i=0.1736482, k=0.9848078)
    # angle = count_B_angle_by_orts(i=0.9848078, k=-0.1736482)
    # angle = count_B_angle_by_orts(i=-0.1736482, k=-0.9848078)
    # angle = count_B_angle_by_orts(i=-0.9848078, k=0.1736482)
    #
    # angle = count_C_angle_by_orts(i=0.1736482, j=0.9848078)
    # angle = count_C_angle_by_orts(i=0.9848078, j=-0.1736482)
    # angle = count_C_angle_by_orts(i=-0.1736482, j=-0.9848078)
    # angle = count_C_angle_by_orts(i=-0.9848078, j=0.1736482)

    # print(angle)

    # lisA = [100, 173.2051, 0]
    # lisA = [68.4040, 187.9385, 10]
    # lisA = [-187.9385, 68.4040, 100]
    # lisA = [-68.4040, -187.9385, 190]
    # lisA = [187.9385, -68.4040, 280]
    # cordsA = count_new_Y_Z_for_A_rotation(y_start=lisA[0],
    #                                       z_start=lisA[1],
    #                                       angle_C_deg=lisA[2])
    #
    # print(cordsA)

    lisB = [-100, 173.2051, 0]
    lisB = [-68.4040, 187.9385, 10]
    lisB = [187.9385, 68.4040, 100]
    lisB = [68.4040, -187.9385, 190]
    lisB = [-187.9385, -68.4040, 280]
    cordsB = count_new_X_Z_for_B_rotation(x_start=lisB[0],
                                          z_start=lisB[1],
                                          angle_C_deg=lisB[2])

    print(cordsB)
