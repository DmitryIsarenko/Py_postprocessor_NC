# from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_3axis import PprintParserMill3Axis
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_basic import PprintParserBasic


class PprintParserMill4Axis(PprintParserBasic):
    pprint_parser_class_name = "PprintParserMill4AxisA"

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_is_oper_multax_in_cl_list(cl_list: list[str]) -> bool:
        for line in cl_list:
            if "MULTAX / ON" in line:
                return True
        else:
            return False