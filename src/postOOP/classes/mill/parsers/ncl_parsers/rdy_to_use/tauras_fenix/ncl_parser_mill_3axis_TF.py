from src.postOOP.classes.mill.parsers.ncl_parsers.basic.ncl_parser_mill_3axis import NclParserMill3axis
from src.postOOP import config
import logging

logger = logging.getLogger(__name__)


class NclParserMill3axisTF(NclParserMill3axis):
    ncl_parser_class_name = "NclParserMill3axisTF"

    # logger.debug(f"NCL parser set to: {ncl_parser_class_name}")

    @classmethod
    def parse_LOADTL(cls, cl_list: list[str], line_index: int, nc_seq_obj) -> list[str]:
        result_list = list()
        if config.G_CODE_TOOL_POT_PARAMS_ENABLED is False:
            result_list.append(
                f"T{nc_seq_obj.tool_pot} M6", )
            pass
        elif config.G_CODE_TOOL_POT_PARAMS_ENABLED is True:
            result_list.append(
                f"{config.G_CODE_TOOL_POT_PARAMETER}={nc_seq_obj.tool_pot}(NOMER T INSTRUMENTA)", )
            pass

        if config.G_CODE_SPINDLE_PARAMS_ENABLED is False:
            pass
        elif config.G_CODE_SPINDLE_PARAMS_ENABLED is True:
            result_list.append(f"{config.G_CODE_TOOL_RPM_PARAMETER}="
                               f"{nc_seq_obj.spindle_speed_master}"
                               f"(OBOROTI)")
            pass

        if config.G_CODE_FEED_PARAMS_ENABLED is False:
            pass
        elif config.G_CODE_FEED_PARAMS_ENABLED is True and nc_seq_obj.cut_feed_master:
            result_list.append(
                f"{config.G_CODE_TOOL_FEED_PARAMETER}={nc_seq_obj.cut_feed_master}"
                f"(PODACHA)")
        cls.is_G43_needed = True
        cls.is_G43_ON = False
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
                    if config.G_CODE_SPINDLE_PARAMS_ENABLED is False:
                        item = round(float(item))
                        cls.current_SPINDLE = item
                        res_line.append(f"S{item} ")
                    elif config.G_CODE_SPINDLE_PARAMS_ENABLED is True:
                        res_line.append(f"S{config.G_CODE_TOOL_RPM_PARAMETER} ")
            result_list.append("".join(res_line))
        return result_list

    @classmethod
    def create_G43_addition(cls, nc_seq_obj) -> str:
        res_line = str()
        res_line += f"G43 "
        if config.G_CODE_TOOL_POT_PARAMS_ENABLED is False:
            res_line += f"H{nc_seq_obj.tool_pot} "
        if config.G_CODE_TOOL_POT_PARAMS_ENABLED is True:
            res_line += f"H{config.G_CODE_TOOL_POT_PARAMETER} "
        return res_line

    @classmethod
    def parse_FEDRAT(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        res_list = list()
        if config.G_CODE_FEED_PARAMS_ENABLED is False:
            right_part_list = cl_list[line_index].split(sep=" / ")[1].strip().split(sep=",")
            feedrate = round(float(right_part_list[0]), ndigits=2)
            res_list.append(f"G01 F{feedrate} ")
        elif config.G_CODE_FEED_PARAMS_ENABLED is True:
            res_list.append(f"G01 F{config.G_CODE_TOOL_FEED_PARAMETER} ")
        result_list = res_list
        return result_list

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

        if config.G_CODE_TOOL_POT_PARAMS_ENABLED is False:
            D_corrector_addition = f"D{nc_seq_obj.tool_pot}"
        if config.G_CODE_TOOL_POT_PARAMS_ENABLED is True:
            D_corrector_addition = f"D{config.G_CODE_TOOL_POT_PARAMETER}"

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
        # если имя операции из перечня ключей словаря с типами операций
        elif right_part_list[0] in config.dict_of_axial_operations_G_codes.keys():

            operation_data["Z_START"] = cls.get_z_start_for_cycle(cl_list=cl_list, line_index=line_index + 1)
            cl_list[line_index + 1] = "$$-> line removed because CYCLE is parsed in previous line"

            res_list = list()
            res_list.append(f"G98 ")
            res_list.append(config.dict_of_axial_operations_G_codes[right_part_list[0]] + " ")

            if "MMPM" in right_part_list:
                operation_data["FEED_TYPE"] = "G94"
                feed_type_index = right_part_list.index("MMPM")
                operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]),
                                                    ndigits=config.NDIGITS_FEEDRATE_G94)
                if config.G_CODE_FEED_PARAMS_ENABLED is False or nc_seq_obj.cut_feed_master is None:
                    res_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
                elif config.G_CODE_FEED_PARAMS_ENABLED is True:
                    res_list.append(f"{operation_data["FEED_TYPE"]} F{config.G_CODE_TOOL_FEED_PARAMETER} ")

            elif "MMPR" in right_part_list:
                operation_data["FEED_TYPE"] = "G95"
                feed_type_index = right_part_list.index("MMPR")
                operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]),
                                                    ndigits=config.NDIGITS_FEEDRATE_G95)
                if config.G_CODE_FEED_PARAMS_ENABLED is False or nc_seq_obj.cut_feed_master is None:
                    res_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
                elif config.G_CODE_FEED_PARAMS_ENABLED is True:
                    res_list.append(f"{operation_data["FEED_TYPE"]} F{config.G_CODE_TOOL_FEED_PARAMETER} ")
            if "DEPTH" in right_part_list:
                depth_index = right_part_list.index("DEPTH")
                operation_data["DEPTH"] = round(float(right_part_list[depth_index + 1]),
                                                ndigits=config.NDIGITS_CALC_XYZ)
                drill_to_z = round(operation_data["Z_START"] - operation_data["DEPTH"], ndigits=config.NDIGITS_XYZ)
                res_list.append(f"Z{drill_to_z} ")
            if "STEP" in right_part_list:
                step_index = right_part_list.index("STEP")
                operation_data["STEP"] = round(float(right_part_list[step_index + 1]), ndigits=config.NDIGITS_XYZ)
                res_list.append(f"Q{operation_data["STEP"]} ")
            if "CLEAR" in right_part_list:
                clear_index = right_part_list.index("CLEAR")
                operation_data["CLEAR"] = round(float(right_part_list[clear_index + 1]),
                                                ndigits=config.NDIGITS_CALC_XYZ)
                retract_dist = round(operation_data["CLEAR"] + operation_data["Z_START"], ndigits=config.NDIGITS_XYZ)
                res_list.append(f"R{retract_dist} ")
            if "ZFEED" in right_part_list:
                zfeed_index = right_part_list.index("ZFEED")
                operation_data["ZFEED"] = round(float(right_part_list[zfeed_index + 1]),
                                                ndigits=config.NDIGITS_FEEDRATE_G95)
            result_list.append("".join(res_list))
        return result_list

    @classmethod
    def parse_OPSTOP(cls, cl_list: list[str], line_index: int) -> list[str]:
        result_list = list()
        result_list.append("M00")
        return result_list

    @classmethod
    def parse_STOP(cls, cl_list: list[str], line_index: int) -> list[str]:
        pass

    @classmethod
    def insert_G43H_on_first_Z_move(cls, cl_list: list[str], nc_seq_obj):
        result_list = list()
        counter_lines_with_z = 0
        for line_index in range(len(result_list)):
            line = result_list[line_index]
            if "G00" in line or "G01" in line:
                counter_lines_with_z += 1
                if counter_lines_with_z > 0:
                    if config.G_CODE_TOOL_POT_PARAMS_ENABLED is False:
                        insertion = f"G43 H{nc_seq_obj.tool_pot} "
                    elif config.G_CODE_TOOL_POT_PARAMS_ENABLED is True:  # G_CODE_PARAMS_ENABLED == 1:
                        insertion = f"G43 H{config.G_CODE_TOOL_POT_PARAMETER} "
                    result_list[line_index] = insertion + result_list[line_index]
                    break
                else:
                    continue
            else:
                continue
        return result_list
