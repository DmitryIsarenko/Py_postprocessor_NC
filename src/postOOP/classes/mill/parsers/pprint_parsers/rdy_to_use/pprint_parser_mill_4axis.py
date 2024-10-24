# from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_mill_3axis import PprintParserMill3Axis
from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_oper_4axis import MixinOper4Axis
from src.postOOP.classes.mill.parsers.pprint_parsers.basic.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.mill.parsers.pprint_parsers.mixins_pprint_parser.mixin_pprint_arrays import MixinPprintArrays
from src.postOOP.classes.mill.parsers.pprint_parsers.mixins_pprint_parser.mixin_pprint_multax import MixinPprintMultax


class PprintParserMill4Axis(PprintParserBasic,
                            MixinPprintArrays,
                            MixinPprintMultax,
                            ):
    pprint_parser_class_name = "PprintParserMill4AxisA"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)