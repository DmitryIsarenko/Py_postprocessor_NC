import logging
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_B_syntec import NclParserMill4AxisBSyntec
from src.postOOP.classes.parsers.coord_parsers.coords_parser_TF import CoordsParserTF
from src.postOOP import config

logger = logging.getLogger(__name__)


class NclParserMill4AxisBSyntecTF(NclParserMill4AxisBSyntec):
    ncl_parser_class_name = "NclParserMill4axisASyntecTF"

    @classmethod
    def parse_GOTO(cls, cl_list: list[str], line_index: int, nc_seq_obj) -> list[str]:
        final_result_list = list()
        res_list = list()
        cls.goto_counter += 1

        if "RAPID" in cl_list[line_index - 1] and cls.is_G00_needed:
            res_list.extend(cls.parse_RAPID())
            cls.is_G00_ON = True
            cls.is_G01_ON = False
            cls.is_G02_ON = False
            cls.is_G03_ON = False
        elif "RAPID" in cl_list[line_index - 2] and cls.is_G00_needed:
            res_list.extend(cls.parse_RAPID())
            cls.is_G00_ON = True
            cls.is_G01_ON = False
            cls.is_G02_ON = False
            cls.is_G03_ON = False
        elif "FEDRAT" in cl_list[line_index - 1] and cls.is_G01_needed:
            cls.is_G00_ON = False
            cls.is_G01_ON = True
            cls.is_G02_ON = False
            cls.is_G03_ON = False
            res_list.extend(cls.parse_FEDRAT(cl_list=cl_list, line_index=line_index - 1))
        elif "FEDRAT" in cl_list[line_index - 2] and cls.is_G01_needed:
            cls.is_G00_ON = False
            cls.is_G01_ON = True
            cls.is_G02_ON = False
            cls.is_G03_ON = False
            res_list.extend(cls.parse_FEDRAT(cl_list=cl_list, line_index=line_index - 2))

        if "CUTCOM / LEFT" in cl_list[line_index - 1] \
                or "CUTCOM / RIGHT" in cl_list[line_index - 1] \
                or "CUTCOM / OFF" in cl_list[line_index - 1]:
            res_list.extend(cls.parse_CUTCOM(cl_list=cl_list, line_index=line_index - 1, nc_seq_obj=nc_seq_obj))
        if "CUTCOM / LEFT" in cl_list[line_index - 2] \
                or "CUTCOM / RIGHT" in cl_list[line_index - 2] \
                or "CUTCOM / OFF" in cl_list[line_index - 2]:
            res_list.extend(cls.parse_CUTCOM(cl_list=cl_list, line_index=line_index - 2, nc_seq_obj=nc_seq_obj))

        if cls.is_G43_ON is False and cls.is_G43_needed is True:
            res_list.append(cls.create_G43_addition(nc_seq_obj=nc_seq_obj))
            cls.is_G43_ON = True

        # если кругового нет позади, но есть впереди
        # если круговое есть позади, но нет впереди
        # если кругового нет ни позади, ни впереди
        if ("CIRCLE" not in cl_list[line_index - 1] and "CIRCLE" in cl_list[line_index + 1]) \
                or ("CIRCLE" in cl_list[line_index - 1] and "CIRCLE" not in cl_list[line_index + 1]) \
                or ("CIRCLE" not in cl_list[line_index - 1] and "CIRCLE" not in cl_list[line_index + 1]):
            if cls.is_G01_needed is True and cls.is_G01_ON is False:
                res_list.append(f"G01 ")
            elif cls.is_G00_needed is True and cls.is_G00_ON is False:
                res_list.append(f"G00 ")

            right_part_list = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=",")
            right_part_list = [round(float(item), ndigits=config.NDIGITS_CALC_XYZ) for item in right_part_list]

            if len(right_part_list) == 3:
                x, y, z = right_part_list
                x, y, z = round(x, config.NDIGITS_XYZ), round(y, config.NDIGITS_XYZ), round(z, config.NDIGITS_XYZ)

                if x == -0.0:
                    x = 0.0
                if y == -0.0:
                    y = 0.0
                if z == -0.0:
                    z = 0.0

                if cls.is_multax_operation is False:
                    res_list.append(f"X{x} Y{y} Z{z}")
                elif cls.is_multax_operation:
                    if cls.goto_counter == 1:
                        final_result_list.append(f"M11")
                        final_result_list.append(f"G00 G90 B0")
                        final_result_list.append(f"M10")
                        # final_result_list.append(f"")
                        res_list.append(f"X{x} Y{y} Z{z}")
                    else:
                        res_list.append(f"X{x} Y{y} Z{z}")

            elif len(right_part_list) == 6:
                x, y, z, i, j, k = right_part_list

                b = CoordsParserTF.count_B_angle_by_orts(i=i, k=k)
                x, z = CoordsParserTF.count_new_X_Z_for_B_rotation(x_start=x, z_start=z, angle_B_deg=b)

                x, y, z = round(x, config.NDIGITS_XYZ), round(y, config.NDIGITS_XYZ), round(z, config.NDIGITS_XYZ)
                b = round(b, config.NDIGITS_ABC)

                if x == -0.0:
                    x = 0.0
                if y == -0.0:
                    y = 0.0
                if z == -0.0:
                    z = 0.0

                # первая строка
                if cls.goto_counter == 1:
                    # позиционная обработка
                    if cls.is_positional_multax:
                        final_result_list.append(f"M11")
                        final_result_list.append(f"G00 G90 B{b}")
                        final_result_list.append(f"M10")
                        # final_result_list.append(f"")
                        res_list.append(f"X{x} Y{y} Z{z}")
                    # непрерывная обработка
                    else:
                        final_result_list.append(f"M11")
                        final_result_list.append(f"G00 G90 B{b}")
                        res_list.append(f"X{x} Y{y} Z{z}")
                # не первая строка
                else:
                    # позиционная обработка
                    if cls.is_positional_multax:
                        res_list.append(f"X{x} Y{y} Z{z}")
                    # непрерывная обработка
                    else:
                        res_list.append(f"B{b} X{x} Y{y} Z{z}")
            else:
                logger.critical(f"Wrong num of scalars in right part of GOTO")
                raise ValueError
        if res_list:
            final_result_list.append("".join(res_list))
        return final_result_list

    @classmethod
    def parse_CIRCLE(cls, cl_list: list[str], line_index: int) -> list[str]:
        cls.is_G00_ON = False
        cls.is_G01_ON = False
        final_result_list = list()
        res_list = list()

        # logger.debug(f"cl_list[line_index - 1] = {cl_list[line_index - 1]}")
        # logger.debug(f"cl_list[line_index] = {cl_list[line_index]}")
        # logger.debug(f"cl_list[line_index + 1] = {cl_list[line_index + 1]}")

        start_coords_list_str = cl_list[line_index - 1].split(sep=" / ")[1].strip().split(sep=",")
        center_coords_list_str = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=",")
        end_coords_list_str = cl_list[line_index + 1].split(sep=" / ")[1].strip().split(sep=",")

        # logger.debug(f"start_coords_list_str = {start_coords_list_str}")
        # logger.debug(f"center_coords_list_str = {center_coords_list_str}")
        # logger.debug(f"end_coords_list_str = {end_coords_list_str}")

        start_coords_list_float = [round(float(item), ndigits=config.NDIGITS_CALC_XYZ) for item in
                                   start_coords_list_str]
        center_coords_list_float = [round(float(item), ndigits=config.NDIGITS_CALC_XYZ) for item in
                                    center_coords_list_str]
        end_coords_list_float = [round(float(item), ndigits=config.NDIGITS_CALC_XYZ) for item in end_coords_list_str]

        (x_center_abs, y_center_abs, z_center_abs,
         i_center, j_center, k_center, radius) = center_coords_list_float

        if len(end_coords_list_float) == 3 and len(start_coords_list_float) == 3:
            x_start_abs, y_start_abs, z_start_abs = start_coords_list_float
            x_end_abs, y_end_abs, z_end_abs = end_coords_list_float

            x_center_incr = round(x_center_abs - x_start_abs, ndigits=config.NDIGITS_XYZ)
            y_center_incr = round(y_center_abs - y_start_abs, ndigits=config.NDIGITS_XYZ)
            z_center_incr = round(z_center_abs - z_start_abs, ndigits=config.NDIGITS_XYZ)

            x_end_abs = round(x_end_abs, config.NDIGITS_XYZ)
            y_end_abs = round(y_end_abs, config.NDIGITS_XYZ)
            z_end_abs = round(z_end_abs, config.NDIGITS_XYZ)

            if k_center == -1:
                res_list.append("G02 ")
            elif k_center == 1:
                res_list.append("G03 ")

            if x_end_abs == -0.0:
                x_end_abs = 0.0
            if y_end_abs == -0.0:
                y_end_abs = 0.0
            if z_end_abs == -0.0:
                z_end_abs = 0.0
            if x_center_incr == -0.0:
                x_center_incr = 0.0
            if y_center_incr == -0.0:
                y_center_incr = 0.0
            if z_center_incr == -0.0:
                z_center_incr = 0.0

            res_list.append(f"X{x_end_abs} "
                            f"Y{y_end_abs} "
                            f"Z{z_end_abs} "
                            f"I{x_center_incr} "
                            f"J{y_center_incr} "
                            f"K{z_center_incr}"
                            )
            final_result_list.append("".join(res_list))
            return final_result_list

        elif len(end_coords_list_float) == 6 and len(start_coords_list_float) == 6:
            (x_start_abs, y_start_abs, z_start_abs,
             i_start, j_start, k_start) = start_coords_list_float

            (x_end_abs, y_end_abs, z_end_abs,
             i_end, j_end, k_end) = end_coords_list_float

            start_b = CoordsParserTF.count_B_angle_by_orts(i=i_start, k=k_start)
            end_b = CoordsParserTF.count_B_angle_by_orts(i=i_end, k=k_end)

            i_sum_vector = (i_start + i_center) / 2
            j_sum_vector = (j_start + j_center) / 2
            k_sum_vector = (k_start + k_center) / 2

            sum_angle = CoordsParserTF.count_B_angle_by_orts(i=i_sum_vector, k=k_sum_vector)

            # logger.debug(f"start ijk = {i_start} {j_start} {k_start}")
            # logger.debug(f"center ijk = {i_center} {j_center} {k_center}")
            # logger.debug(f"sum_ijk = {i_sum_vector} {j_sum_vector} {k_sum_vector}")
            # logger.debug(f"sum_angle = {sum_angle}")
            # logger.debug(f"start_a   = {start_a}")
            if i_sum_vector == 0 and j_sum_vector == 0 and k_sum_vector == 0:
                res_list.append("G02 ")
            elif i_start == i_center and j_start == j_center and k_start == k_center:
                res_list.append("G03 ")

            if start_b == end_b:
                x_start_abs, z_start_abs = CoordsParserTF.count_new_X_Z_for_B_rotation(x_start=x_start_abs,
                                                                                       z_start=z_start_abs,
                                                                                       angle_B_deg=start_b)
                x_center_abs, z_center_abs = CoordsParserTF.count_new_X_Z_for_B_rotation(x_start=x_center_abs,
                                                                                         z_start=z_center_abs,
                                                                                         angle_B_deg=start_b)
                x_end_abs, z_end_abs = CoordsParserTF.count_new_X_Z_for_B_rotation(x_start=x_end_abs,
                                                                                   z_start=z_end_abs,
                                                                                   angle_B_deg=end_b)

                x_center_incr = round(x_center_abs - x_start_abs, ndigits=config.NDIGITS_XYZ)
                y_center_incr = round(y_center_abs - y_start_abs, ndigits=config.NDIGITS_XYZ)
                z_center_incr = round(z_center_abs - z_start_abs, ndigits=config.NDIGITS_XYZ)

                x_end_abs = round(x_end_abs, config.NDIGITS_XYZ)
                y_end_abs = round(y_end_abs, config.NDIGITS_XYZ)
                z_end_abs = round(z_end_abs, config.NDIGITS_XYZ)

                if x_end_abs == -0.0:
                    x_end_abs = 0.0
                if y_end_abs == -0.0:
                    y_end_abs = 0.0
                if z_end_abs == -0.0:
                    z_end_abs = 0.0
                if x_center_incr == -0.0:
                    x_center_incr = 0.0
                if y_center_incr == -0.0:
                    y_center_incr = 0.0
                if z_center_incr == -0.0:
                    z_center_incr = 0.0

                res_list.append(f"X{x_end_abs} "
                                f"Y{y_end_abs} "
                                f"Z{z_end_abs} "
                                f"I{x_center_incr} "
                                f"J{y_center_incr} "
                                f"K{z_center_incr}"
                                )
                final_result_list.append("".join(res_list))
                return final_result_list


            else:
                logger.critical("Different start and end angles in a CIRCLE cl line!")
                raise ValueError

        else:
            logger.critical("Different start and end len of GOTO lines around a CIRCLE cl line!")
            raise IndexError



