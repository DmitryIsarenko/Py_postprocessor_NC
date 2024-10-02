from src.postOOP import config
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_basic_mill_syntec import NclParserBasicMillSyntec
import logging

logger = logging.getLogger(__name__)


class NclParserMill3axisSyntec(NclParserBasicMillSyntec):
    ncl_parser_name = "NclParserBasicMill3axis"
    logger.debug(f"NCL parser set to: {ncl_parser_name}")

    current_X = 0
    current_Y = 0
    current_Z = 0

    is_G43_needed = False

    is_G43_ON = False

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
            result_list.append(f"G{right_part}")
        return result_list

    @classmethod
    def create_G43_addition(cls, nc_seq_obj) -> str:
        res_line = str()
        res_line += f"G43 "
        res_line += f"H{nc_seq_obj.tool_pot} "
        return res_line

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

        if cls.is_G43_ON is False and cls.is_G43_needed is True:
            res_list.append(cls.create_G43_addition(nc_seq_obj=nc_seq_obj))
            cls.is_G43_ON = True

        if ("CIRCLE" not in cl_list[line_index - 1] and "CIRCLE" in cl_list[line_index + 1]) \
                or ("CIRCLE" in cl_list[line_index - 1] and "CIRCLE" not in cl_list[line_index + 1]) \
                or ("CIRCLE" not in cl_list[line_index - 1] and "CIRCLE" not in cl_list[line_index + 1]):
            if cls.is_G01_needed is True and cls.is_G01_ON is False:
                res_list.append(f"G01 ")
            elif cls.is_G00_needed is True and cls.is_G00_ON is False:
                res_list.append(f"G00 ")

            right_part_list = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=",")
            right_part_list = [round(float(item), ndigits=5) for item in right_part_list]

            if len(right_part_list) == 3:
                x, y, z = right_part_list
                res_list.append(f"X{x} Y{y} Z{z}")

            elif len(right_part_list) == 6:
                pass
            else:
                print("error with num of scalars")
        if res_list:
            result_list.append("".join(res_list))
        return result_list

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
                operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]), ndigits=4)
                res_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")

            elif "MMPR" in right_part_list:
                operation_data["FEED_TYPE"] = "G95"
                feed_type_index = right_part_list.index("MMPR")
                operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]), ndigits=4)
                res_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
            if "DEPTH" in right_part_list:
                depth_index = right_part_list.index("DEPTH")
                operation_data["DEPTH"] = round(float(right_part_list[depth_index + 1]), ndigits=5)
                res_list.append(f"Z{operation_data["DEPTH"]} ")
            if "STEP" in right_part_list:
                step_index = right_part_list.index("STEP")
                operation_data["STEP"] = round(float(right_part_list[step_index + 1]), ndigits=5)
                res_list.append(f"Q{operation_data["STEP"]} ")
            if "CLEAR" in right_part_list:
                clear_index = right_part_list.index("CLEAR")
                operation_data["CLEAR"] = round(float(right_part_list[clear_index + 1]), ndigits=5)
                res_list.append(f"R{operation_data["CLEAR"]} ")
            if "ZFEED" in right_part_list:
                zfeed_index = right_part_list.index("ZFEED")
                operation_data["ZFEED"] = round(float(right_part_list[zfeed_index + 1]), ndigits=4)
            result_list.append("".join(res_list))
        return result_list

    @classmethod
    def parse_GOHOME(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        result_list.append("G00 G28 Z0.0")
        result_list.append("G00 G28 X0.0")
        result_list.append("G00 G28 Y0.0")
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
