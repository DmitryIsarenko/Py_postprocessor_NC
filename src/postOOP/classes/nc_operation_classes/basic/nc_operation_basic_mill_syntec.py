from src.postOOP.classes.nc_operation_classes.basic.nc_operation_basic import NcOperationBasic
from src.postOOP.classes.nc_sequence_classes.basic.nc_sequence_basic_mill_syntec import NcSequenceMillBasicSyntec
from src.postOOP.classes.parsers.pprint_parsers.pprint_parser_basic_mill import PprintParserBasicMill
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_basic_mill_syntec import NclParserBasicMillSyntec


class NcOperationBasicMillSyntec(NcOperationBasic):
    nc_sequence_class: NcSequenceMillBasicSyntec = NcSequenceMillBasicSyntec
    pprint_parser_class: PprintParserBasicMill = PprintParserBasicMill
    ncl_parser_class: NclParserBasicMillSyntec = NclParserBasicMillSyntec

    postprocessor_name = "BASIC MILL SYNTEC POST"

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    # def set_nc_sequences_objects_in_list(self):
    #     lst_of_objects = []
    #     nc_counter = 0
    #     for nc_sequence_name in self.list_of_nc_sequences_names:
    #         nc_counter += 1
    #         lst_of_objects.append(
    #             NcSequenceMillBasicSyntec(
    #                 detail_name=self.detail_name,
    #                 nc_sequence_name=nc_sequence_name,
    #                 cl_list=self.cl_list,
    #                 nc_sequence_number=nc_counter,
    #                 nc_sequences_count=self.nc_sequences_count,
    #                 nc_operation_number=self.operation_number,
    #                 date_of_creation=self.date_of_creation
    #             )
    #         )
    #     self.list_of_nc_sequences_objects: list[NcSequenceMillBasicSyntec] = lst_of_objects
