from src.postOOP import config
import logging

logger = logging.getLogger(__name__)


class NclParserBasic:
    ncl_parser_class_name = "NclParserBasic"
    # logger.debug(f"NCL parser set to: {ncl_parser_class_name}")

    current_FEED = 0
    current_SPINDLE = 0

    # is_G43_needed = False
    is_G41_cutcom_2D_needed = False
    is_G42_cutcom_2D_needed = False

    # is_G43_ON = False
    is_G41_cutcom_2D_ON = False
    is_G42_cutcom_2D_ON = False

    is_G00_needed = False
    is_G01_needed = False
    is_G02_needed = False
    is_G03_needed = False

    is_G00_ON = False
    is_G01_ON = False
    is_G02_ON = False
    is_G03_ON = False

    @classmethod
    def parse_cl_list(cls, nc_seq_obj) -> list[str]:
        cl_list = nc_seq_obj.cl_list[nc_seq_obj.cl_start_index: nc_seq_obj.cl_end_index]
        result_list = []
        for line_index in range(len(cl_list)):
            if "PPRINT /" in cl_list[line_index]:
                result = cls.parse_PPRINT(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "UNITS /" in cl_list[line_index]:
                result = cls.parse_UNITS(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
                # elif "SET / OFSETL, " in cl_list[line_index]:
                #     result = cls.parse_SET_OFSETL(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "CSYS /" in cl_list[line_index]:
                result = cls.parse_CSYS(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            # elif "LOADTL /" in cl_list[line_index]:
            #     result = cls.parse_LOADTL(cl_list=cl_list, line_index=line_index, nc_seq_obj=nc_seq_obj)
            #     result_list.extend(result)
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
                # elif "CYCLE /" in cl_list[line_index]:
                #     result = cls.parse_CYCLE(cl_list=cl_list, line_index=line_index, nc_seq_obj=nc_seq_obj)
                result_list.extend(result)
            elif "OPSTOP" in cl_list[line_index][0:6]:
                result = cls.parse_OPSTOP(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "STOP" in cl_list[line_index][0:4]:
                result = cls.parse_STOP(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            # elif "GOHOME" in cl_list[line_index][0:6]:
            #     result = cls.parse_GOHOME(cl_list=cl_list, line_index=line_index)
            #     result_list.extend(result)
            elif "END /" in cl_list[line_index]:
                result = cls.parse_END(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "FINI" in cl_list[line_index]:
                result = cls.parse_FINI(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            elif "$$" in cl_list[line_index]:
                result = cls.parse_DOUBLE_DOLLAR(cl_list=cl_list, line_index=line_index)
                result_list.extend(result)
            else:
                cls.parse_UNPARSED(cl_list=cl_list, line_index=line_index)

        # cls.insert_G43H_on_first_Z_move(cl_list=cl_list, nc_seq_obj=nc_seq_obj)

        return result_list

    @classmethod
    def parse_PPRINT(cls, cl_list: list[str], line_index: int) -> list[str]:
        return list()

    @classmethod
    def parse_PARTNO(cls, cl_list: list[str], line_index: int) -> list[str]:
        pass

    @classmethod
    def parse_UNITS(cls, cl_list: list[str], line_index: int) -> list[str]:
        result = list()
        units_str = cl_list[line_index].split(sep=" / ")[1]
        if units_str == "MM":
            result.append("G21")
        elif units_str == "INCH":
            result.append("G20")
        else:
            result.append("UNKNOWN UNITS")
        return result

    @classmethod
    def parse_CSYS(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        right_part_str = cl_list[line_index].split(sep=" / ")[1]
        right_part_list = right_part_str.split(sep=",")
        csys_coords = [round(float(char), ndigits=config.NDIGITS_XYZ) for char in right_part_list]
        return result_list

    @classmethod
    def parse_SPINDL(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        res_line = list()
        right_part = cl_list[line_index].split(sep=" / ")[1].strip()
        if "OFF" in right_part:
            result_list.append("M05")
            cls.current_SPINDLE = 0
        elif "RPM, " in right_part:
            right_part_list = right_part.split(sep=",")
            right_part_list = [item.strip() for item in right_part_list]
            for item in right_part_list:
                if item == "RPM":
                    res_line.append("G97 ")
                elif item == "CLW":
                    res_line.append("M03")
                elif item == "CCLW":
                    res_line.append("M04")
                else:
                    item = round(float(item))
                    cls.current_SPINDLE = item
                    res_line.append(f"S{item} ")

            result_list.append("".join(res_line))
        return result_list

    @classmethod
    def parse_RAPID(cls) -> list[str]:
        result_list = list()
        result_list.append(f"G00 ")
        return result_list


    @classmethod
    def parse_GOTO(cls, cl_list: list[str], line_index: int, nc_seq_obj) -> list[str]:
        result_list = list()
        res_list = list()

        if "RAPID" in cl_list[line_index - 1] and cls.is_G00_needed:
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

        if "CUTCOM / LEFT" in cl_list[line_index - 1] \
                or "CUTCOM / RIGHT" in cl_list[line_index - 1] \
                or "CUTCOM / OFF" in cl_list[line_index - 1]:
            res_list.extend(cls.parse_CUTCOM(cl_list=cl_list, line_index=line_index - 1, nc_seq_obj=nc_seq_obj))


        if ("CIRCLE" not in cl_list[line_index - 1] and "CIRCLE" in cl_list[line_index + 1]) \
                or ("CIRCLE" in cl_list[line_index - 1] and "CIRCLE" not in cl_list[line_index + 1]) \
                or ("CIRCLE" not in cl_list[line_index - 1] and "CIRCLE" not in cl_list[line_index + 1]):
            if cls.is_G01_needed is True and cls.is_G01_ON is False:
                res_list.append(f"G01 ")
            elif cls.is_G00_needed is True and cls.is_G00_ON is False:
                res_list.append(f"G00 ")

            right_part_list = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=",")
            right_part_list = [round(float(item), ndigits=config.NDIGITS_XYZ) for item in right_part_list]

            if len(right_part_list) == 3:
                x, y, z = right_part_list
                res_list.append(f"X{x} Y{y} Z{z}")

            elif len(right_part_list) == 6:
                pass
            else:
                logger.critical("error with num of scalars")
        if res_list:
            result_list.append("".join(res_list))
        return result_list

    @classmethod
    def set_feedrate(cls, cl_line: str):
        cls.is_G00_needed = False
        cls.is_G01_needed = True
        right_part_list = cl_line.split(sep=" / ")[1].strip().split(sep=",")
        feedrate = round(float(right_part_list[0]), ndigits=config.NDIGITS_FEEDRATE_G94)
        cls.current_FEED = feedrate

    @classmethod
    def set_rapid(cls):
        cls.is_G00_needed = True
        cls.is_G01_needed = False

    @classmethod
    def parse_FEDRAT(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        res_list = list()
        right_part_list = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=",")
        feedrate = round(float(right_part_list[0]), ndigits=config.NDIGITS_FEEDRATE_G94)
        res_list.append(f"G01 F{feedrate} ")

        result_list = res_list
        return result_list

    @classmethod
    def set_cutcom(cls, cl_line: str):
        cutcom_str = cl_line.split(sep=" / ")[1].strip()
        if cutcom_str == "OFF":
            cls.is_G41_cutcom_2D_needed = False
            cls.is_G42_cutcom_2D_needed = False
        elif cutcom_str == "LEFT":
            cls.is_G41_cutcom_2D_needed = True
        elif cutcom_str == "RIGHT":
            cls.is_G42_cutcom_2D_needed = True

    @classmethod
    def parse_CUTCOM(cls, cl_list: list[str], line_index: int, nc_seq_obj) -> list[str]:
        result_list = list()
        cutcom_str = cl_list[line_index].split(sep=" / ")[1].strip()
        if config.G41_G42_SIDE_IS_REVERSED_SWITCH is False:
            left_compensation = "G41"
            right_compensation = "G42"
        else:  # config.G41_G42_SIDE_IS_REVERSED_SWITCH is True
            left_compensation = "G42"
            right_compensation = "G41"

        D_corrector_addition = f"D{nc_seq_obj.tool_pot}"

        if cutcom_str == "OFF":
            result_list.append(f"G40 ")
            cls.is_G41_cutcom_2D_needed = False
            cls.is_G41_cutcom_2D_ON = False
            cls.is_G42_cutcom_2D_needed = False
            cls.is_G42_cutcom_2D_ON = False

        elif cutcom_str == "LEFT":
            cls.is_G41_cutcom_2D_needed = True
            result_list.append(f"{left_compensation} {D_corrector_addition} ")
            cls.is_G41_cutcom_2D_ON = True
        elif cutcom_str == "RIGHT":
            cls.is_G42_cutcom_2D_needed = True
            result_list.append(f"{right_compensation} {D_corrector_addition} ")
            cls.is_G42_cutcom_2D_ON = True
        return result_list

    @classmethod
    def parse_CIRCLE(cls, cl_list: list[str], line_index: int) -> list[str]:
        cls.is_G00_ON = False
        cls.is_G01_ON = False
        result_list = list()
        res_list = list()
        prev_coords_list_str = cl_list[line_index - 1].split(sep=" / ")[1].strip().split(sep=",")
        prev_coords_list_float = [round(float(item), ndigits=config.NDIGITS_XYZ) for item in prev_coords_list_str]
        x_start_abs, y_start_abs, z_start_abs = prev_coords_list_float

        right_part_list = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=",")
        right_part_list_float = [round(float(item), ndigits=config.NDIGITS_XYZ) for item in right_part_list]

        end_coords = cl_list[line_index + 1].split(sep=" / ")[1].strip().split(sep=",")
        end_coords_float = [round(float(item), ndigits=config.NDIGITS_XYZ) for item in end_coords]
        x_end_abs, y_end_abs, z_end_abs = end_coords_float

        (x_center_abs, y_center_abs, z_center_abs,
         csys_vector_i, csys_vector_j, csys_vector_k, radius) = right_part_list_float

        x_center_incr = round(x_center_abs - x_start_abs, ndigits=config.NDIGITS_XYZ)
        y_center_incr = round(y_center_abs - y_start_abs, ndigits=config.NDIGITS_XYZ)
        z_center_incr = round(z_center_abs - z_start_abs, ndigits=config.NDIGITS_XYZ)

        if csys_vector_k == -1:
            res_list.append("G02 ")
        elif csys_vector_k == 1:
            res_list.append("G03 ")

        res_list.append(f"X{x_end_abs} "
                        f"Y{y_end_abs} "
                        f"Z{z_end_abs} "
                        f"I{x_center_incr} "
                        f"J{y_center_incr} "
                        f"K{z_center_incr}"
                        )
        result_list.append("".join(res_list))
        return result_list

    @classmethod
    def parse_COOLNT(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        right_part = cl_list[line_index].split(sep=" / ")[1]
        if "ON" in right_part:
            result_list.append(f"M08")
        elif "OFF" in right_part:
            result_list.append(f"M09")
        return result_list


    @classmethod
    def parse_OPSTOP(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        result_list.append("M01")
        return result_list

    @classmethod
    def parse_STOP(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        result_list.append("M00")
        return result_list

    @classmethod
    def parse_END(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        # result_list.append("M01")
        result_list.append("M99")
        result_list.append(f"")
        cls.is_G43_ON = False
        cls.is_G43_needed = False
        return result_list

    @classmethod
    def parse_FINI(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        # result_list.pop()
        result_list.append(f"M30")
        result_list.append(f"")
        return result_list

    @classmethod
    def parse_DOUBLE_DOLLAR(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        return result_list

    @classmethod
    def parse_UNPARSED(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        print(f"HAVENT PARSED cl record: {cl_list[line_index]}")
        return result_list
