import math
from src.postOOP import config
from src.postOOP.classes.mill.parsers.coord_parsers.coords_parser import CoordsParser


class CoordsParserTF(CoordsParser):

    @staticmethod
    def count_A_angle_by_orts(j: float, k: float) -> float:
        angle_rot = 0
        if k == 1:  # angle 0 deg
            angle_rot = 0
        elif j < 0 and k > 0:  # angle <90 deg
            angle_rot = math.atan(abs(j) / abs(k))
        elif j == -1:  # angle 90 deg
            angle_rot = 0.5 * math.pi
        elif j < 0 and k < 0:  # angle 90 < 180 deg
            angle_rot = math.atan(abs(k) / abs(j))
            angle_rot += math.pi * 0.5
        elif k == -1:  # angle 180 deg
            angle_rot = 1 * math.pi
        elif j > 0 and k < 0:  # angle 180 < 270 deg
            angle_rot = math.atan(abs(j) / abs(k))
            angle_rot += math.pi * 1
        elif j == 1:  # angle 270 deg
            angle_rot = 1.5 * math.pi
        elif j > 0 and k > 0:  # angle > 270 deg
            angle_rot = math.atan(abs(k) / abs(j))
            angle_rot += math.pi * 1.5

        angle_rot = angle_rot * 180 / math.pi
        return 360 - round(angle_rot, ndigits=config.NDIGITS_CALC_ABC)

    # @staticmethod
    # def count_B_angle_by_orts(i: float, k: float) -> float:
    #     angle_rot = 0
    #     if k == 1:  # angle 0 deg
    #         angle_rot = 0
    #     elif i > 0 and k > 0:  # angle <90 deg
    #         angle_rot = math.atan(abs(i) / abs(k))
    #     elif i == 1:  # angle 90 deg
    #         angle_rot = 0.5 * math.pi
    #     elif i > 0 and k < 0:  # angle 90 < 180 deg
    #         angle_rot = math.atan(abs(k) / abs(i))
    #         angle_rot += math.pi * 0.5
    #     elif k == -1:  # angle 180 deg
    #         angle_rot = 1 * math.pi
    #     elif i < 0 and k < 0:  # angle 180 < 270 deg
    #         angle_rot = math.atan(abs(i) / abs(k))
    #         angle_rot += math.pi * 1
    #     elif i == -1:  # angle 270 deg
    #         angle_rot = 1.5 * math.pi
    #     elif i < 0 and k > 0:  # angle > 270 deg
    #         angle_rot = math.atan(abs(k) / abs(i))
    #         angle_rot += math.pi * 1.5
    #
    #     angle_rot = angle_rot * 180 / math.pi
    #     return 360 - round(angle_rot, ndigits=config.NDIGITS_CALC_ABC)

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
    #     return round(angle_rot, ndigits=config.NDIGITS_CALC_ABC)

    @staticmethod
    def count_new_Y_Z_for_A_rotation(*, y_start: float | int,
                                     z_start: float | int,
                                     angle_A_deg: float | int) -> tuple[float | int, float | int]:
        angle_A_deg = -angle_A_deg + 360
        angle_A_deg = angle_A_deg * math.pi / 180
        y_end = y_start * math.cos(angle_A_deg) + z_start * math.sin(angle_A_deg)
        z_end = z_start * math.cos(angle_A_deg) - y_start * math.sin(angle_A_deg)
        return round(y_end, ndigits=config.NDIGITS_CALC_XYZ), round(z_end, ndigits=config.NDIGITS_CALC_XYZ)

    # @staticmethod
    # def count_new_X_Z_for_B_rotation(*, x_start: float | int,
    #                                  z_start: float | int,
    #                                  angle_B_deg: float | int) -> tuple[float | int, float | int]:
    #     angle_B_deg = angle_B_deg
    #     angle_B_deg = - angle_B_deg * math.pi / 180
    #     x_end = x_start * math.cos(angle_B_deg) + z_start * math.sin(angle_B_deg)
    #     z_end = z_start * math.cos(angle_B_deg) - x_start * math.sin(angle_B_deg)
    #     return round(x_end, ndigits=config.NDIGITS_CALC_XYZ), round(z_end, ndigits=config.NDIGITS_CALC_XYZ)
    #
    # @staticmethod
    # def count_new_X_Y_for_C_rotation(*, x_start: float | int,
    #                                  y_start: float | int,
    #                                  angle_C_deg: float | int) -> tuple[float | int, float | int]:
    #     angle_C_deg = angle_C_deg * math.pi / 180
    #     x_end = x_start * math.cos(angle_C_deg) + y_start * math.sin(angle_C_deg)
    #     y_end = y_start * math.cos(angle_C_deg) - x_start * math.sin(angle_C_deg)
    #     return round(x_end, ndigits=config.NDIGITS_CALC_XYZ), round(y_end, ndigits=config.NDIGITS_CALC_XYZ)


if __name__ == '__main__':
    pass
