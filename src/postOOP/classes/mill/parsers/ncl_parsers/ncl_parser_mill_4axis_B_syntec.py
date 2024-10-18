from src.postOOP import config
from src.postOOP.classes.mill.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec import NclParserMill3axisSyntec
from src.postOOP.classes.mill.parsers.coord_parsers.coords_parser import CoordsParser
# from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_4axis_A_syntec import NcSequenceMill4AxisASyntec
import logging

logger = logging.getLogger(__name__)


class NclParserMill4AxisBSyntec(NclParserMill3axisSyntec):
    ncl_parser_class_name = "NclParserMill4axisASyntec"
    # logger.debug(f"NCL parser set to: {ncl_parser_class_name}")

    current_X = 0
    current_Y = 0
    current_Z = 0
    current_A = 0

    is_G43_needed = False
    is_G43_ON = False

    is_A_clamped = True
    is_A_clamp_needed = True

    is_positional_multax = True
    goto_counter = 0

    is_multax_active = False

    # is_multax_operation = False

    @classmethod
    def parse_cl_list(cls, nc_seq_obj) -> list[str]:
        cls.set_is_all_ijk_same(nc_seq_obj=nc_seq_obj)
        cls.is_multax_operation = nc_seq_obj.is_multax_operation
        cl_list = nc_seq_obj.cl_list[nc_seq_obj.cl_start_index: nc_seq_obj.cl_end_index]

        result_list = []
        cls.goto_counter = 0
        for line_index in range(len(cl_list)):
            if "PPRINT /" in cl_list[line_index]:
                result = cls.parse_PPRINT(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "UNITS /" in cl_list[line_index]:
                result = cls.parse_UNITS(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "SET / OFSETL, " in cl_list[line_index]:
                result = cls.parse_SET_OFSETL(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "CSYS /" in cl_list[line_index]:
                result = cls.parse_CSYS(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "LOADTL /" in cl_list[line_index]:
                result = cls.parse_LOADTL(cl_list=cl_list, line_index=line_index, nc_seq_obj=nc_seq_obj)
                result_list.extend(result)
            elif "SPINDL /" in cl_list[line_index]:
                result = cls.parse_SPINDL(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "COOLNT /" in cl_list[line_index]:
                result = cls.parse_COOLNT(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "FEDRAT / " in cl_list[line_index]:
                cls.set_feedrate(cl_line=cl_list[line_index])
            elif "CUTCOM / " in cl_list[line_index]:
                cls.set_cutcom(cl_line=cl_list[line_index])
            elif "GOTO / " in cl_list[line_index]:
                result = cls.parse_GOTO(cl_list=cl_list, line_index=line_index, nc_seq_obj=nc_seq_obj)
                result_list.extend(result)
            elif "RAPID" in cl_list[line_index]:
                cls.set_rapid()
            elif "CIRCLE / " in cl_list[line_index]:
                result = cls.parse_CIRCLE(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "CYCLE /" in cl_list[line_index]:
                result = cls.parse_CYCLE(cl_list=cl_list, line_index=line_index, nc_seq_obj=nc_seq_obj)
                result_list.extend(result)
            elif "OPSTOP" in cl_list[line_index][0:6]:
                result = cls.parse_OPSTOP(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "STOP" in cl_list[line_index][0:4]:
                result = cls.parse_STOP(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "GOHOME" in cl_list[line_index][0:6]:
                result = cls.parse_GOHOME(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "END /" in cl_list[line_index]:
                result = cls.parse_END(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "FINI" in cl_list[line_index]:
                result = cls.parse_FINI(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "$$" in cl_list[line_index]:
                result = cls.parse_DOUBLE_DOLLAR(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "MULTAX / ON" in cl_list[line_index]:
                nc_seq_obj.is_multax_active = True
            else:
                cls.parse_UNPARSED(cl_list=cl_list, line_index=line_index)

        # cls.insert_G43H_on_first_Z_move(cl_list=cl_list, nc_seq_obj=nc_seq_obj)

        return result_list

    @classmethod
    def parse_LOADTL(cls, cl_list: list[str], line_index: int, nc_seq_obj) -> list[str]:
        result_list = list()

        result_list.append(
            f"T{nc_seq_obj.tool_pot} M6", )

        cls.is_G43_needed = True
        cls.is_G43_ON = False
        return result_list

    @classmethod
    def parse_SET_OFSETL(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        right_part = cl_list[line_index].split(sep=", ")[1].strip()
        if "OFF" in right_part:
            result_list.append("G00 G28 Z0.0 G49")
        elif int(float(right_part)).is_integer():
            # result_list.append(f"G{right_part}")
            pass
        return result_list

    @classmethod
    def create_G43_addition(cls, nc_seq_obj) -> str:
        res_line = str()
        res_line += f"G43 "
        res_line += f"H{nc_seq_obj.tool_pot} "
        return res_line

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

                b = CoordsParser.count_B_angle_by_orts(i=i, k=k)
                x, z = CoordsParser.count_new_X_Z_for_B_rotation(x_start=x, z_start=z, angle_B_deg=b)

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
    def set_is_all_ijk_same(cls, *, nc_seq_obj):
        cl_list = nc_seq_obj.cl_list[nc_seq_obj.cl_start_index: nc_seq_obj.cl_end_index]
        unic_ijk_set = set()
        for line in cl_list:
            if "GOTO" in line:
                right_part_list = line.split(sep=" / ")[1].strip().split(sep=",")
                if len(right_part_list) == 6:
                    right_part_str = " ".join(right_part_list[3::])
                    unic_ijk_set.add(right_part_str)
        # logger.debug(f"{unic_ijk_set}")
        if len(unic_ijk_set) == 1:
            cls.is_positional_multax = True
            # logger.debug(f"check_is_all_ijk_same = {cls.is_positional_multax}")
            return True
        elif len(unic_ijk_set) > 1:
            cls.is_positional_multax = False
            # logger.debug(f"check_is_all_ijk_same = {cls.is_positional_multax}")
            return False
        else:
            logger.debug("While check of ijk if same - len of set is 0")
            return False

    @classmethod
    def parse_CYCLE(cls, cl_list: list[str], line_index: int, nc_seq_obj) -> list[str]:
        result_list = list()
        right_part_list = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=", ")

        operation_data: dict = {
            "OPERATION_CODE": None,
            "DEPTH": None,
            "STEP": None,
            "ZFEED": None,
            "FEED_TYPE": None,  # MMPM or MMPR
            "FEED_RATE": None,
            "CLEAR": None,
            "RETURN": None,
        }

        if "OFF" in right_part_list:
            result_list.append("G80", )
        elif right_part_list[  # если имя операции из перечня ключей словаря с типами операций
            0] in config.dict_of_axial_operations_G_codes.keys():
            res_list = list()
            res_list.append(f"G98 ")
            res_list.append(config.dict_of_axial_operations_G_codes[right_part_list[0]] + " ")

            if "MMPM" in right_part_list:
                operation_data["FEED_TYPE"] = "G94"
                feed_type_index = right_part_list.index("MMPM")
                operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]),
                                                    ndigits=config.NDIGITS_FEEDRATE_G94)
                res_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
            elif "MMPR" in right_part_list:
                operation_data["FEED_TYPE"] = "G95"
                feed_type_index = right_part_list.index("MMPR")
                operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]),
                                                    ndigits=config.NDIGITS_FEEDRATE_G95)
                res_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")

            if "DEPTH" in right_part_list:
                depth_index = right_part_list.index("DEPTH")
                operation_data["DEPTH"] = round(float(right_part_list[depth_index + 1]), ndigits=config.NDIGITS_XYZ)
                res_list.append(f"Z{operation_data["DEPTH"]} ")
            if "STEP" in right_part_list:
                step_index = right_part_list.index("STEP")
                operation_data["STEP"] = round(float(right_part_list[step_index + 1]), ndigits=config.NDIGITS_XYZ)
                res_list.append(f"Q{operation_data["STEP"]} ")
            if "CLEAR" in right_part_list:
                clear_index = right_part_list.index("CLEAR")
                operation_data["CLEAR"] = round(float(right_part_list[clear_index + 1]), ndigits=config.NDIGITS_XYZ)
                res_list.append(f"R{operation_data["CLEAR"]} ")
            if "ZFEED" in right_part_list:
                zfeed_index = right_part_list.index("ZFEED")
                operation_data["ZFEED"] = round(float(right_part_list[zfeed_index + 1]),
                                                ndigits=config.NDIGITS_FEEDRATE_G95)
            result_list.append("".join(res_list))
        return result_list

    @classmethod
    def parse_GOHOME(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        result_list.append("G00 G28 Z0.0")
        result_list.append("G00 G28 X0.0")
        result_list.append("G00 G28 Y0.0")
        result_list.append("G00 G28 B0.0")
        result_list.append("M00")
        return result_list

    @classmethod
    def insert_G43H_on_first_Z_move(cls, cl_list: list[str], nc_seq_obj):
        result_list = list()
        counter_lines_with_z = 0
        for line_index in range(len(result_list)):
            line = result_list[line_index]
            if "G00" in line or "G01" in line:
                counter_lines_with_z += 1
                if counter_lines_with_z > 0:
                    insertion = f"G43 H{nc_seq_obj.tool_pot} "
                    result_list[line_index] = insertion + result_list[line_index]
                    break
                else:
                    continue
            else:
                continue
        return result_list

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

            start_b = CoordsParser.count_B_angle_by_orts(i=i_start, k=k_start)
            end_b = CoordsParser.count_B_angle_by_orts(i=i_end, k=k_end)

            i_sum_vector = (i_start + i_center) / 2
            j_sum_vector = (j_start + j_center) / 2
            k_sum_vector = (k_start + k_center) / 2

            sum_angle = CoordsParser.count_B_angle_by_orts(i=i_sum_vector, k=k_sum_vector)

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
                x_start_abs, z_start_abs = CoordsParser.count_new_X_Z_for_B_rotation(x_start=x_start_abs,
                                                                                     z_start=z_start_abs,
                                                                                     angle_B_deg=start_b)
                x_center_abs, z_center_abs = CoordsParser.count_new_X_Z_for_B_rotation(x_start=x_center_abs,
                                                                                       z_start=z_center_abs,
                                                                                       angle_B_deg=start_b)
                x_end_abs, z_end_abs = CoordsParser.count_new_X_Z_for_B_rotation(x_start=x_end_abs,
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
