from src.postOOP.classes.nc_operation_classes.basic.nc_operation_basic import NcOperationBasic
from src.postOOP.classes.nc_sequence_classes.basic.nc_sequence_basic_mill_syntec import NcSequenceMillBasicSyntec
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_basic import PprintParserBasic
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_basic_mill_syntec import NclParserBasicMillSyntec


class NcOperationBasicMillSyntec(NcOperationBasic):
    nc_sequence_class: NcSequenceMillBasicSyntec = NcSequenceMillBasicSyntec
    pprint_parser_class: PprintParserBasic = PprintParserBasic
    ncl_parser_class: NclParserBasicMillSyntec = NclParserBasicMillSyntec

    postprocessor_name = "BASIC MILL SYNTEC POST"



    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
