from src.postOOP.classes.nc_operation_classes.basic.nc_operation_basic_mill_syntec import NcOperationBasicMillSyntec
from src.postOOP.classes.nc_sequence_classes.common.nc_sequence_mill_3axis_syntec import NcSequenceMill3AxisSyntec
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_3axis_syntec import NclParserMill3axisSyntec


class NcOperationMill3AxisSyntec(NcOperationBasicMillSyntec):
    nc_sequence_class: NcSequenceMill3AxisSyntec = NcSequenceMill3AxisSyntec
    pprint_parser_class: PprintParserBasic = PprintParserBasic
    ncl_parser_class: NclParserMill3axisSyntec = NclParserMill3axisSyntec

    postprocessor_name = "MILL 3AXIS SYNTEC POST"

    # def __init__(self, filepath: str):
    #     super().__init__(filepath=filepath)

    def __init__(self):
        super().__init__()