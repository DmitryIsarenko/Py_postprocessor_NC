from src.postOOP.classes.nc_operation_classes.nc_operation_mill_3axis_syntec import NcOperationMill3AxisSyntec
from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_4axis_A_syntec import NcSequenceMill4AxisASyntec
from src.postOOP.classes.parsers.ncl_parsers.ncl_parser_mill_4axis_A_syntec import NclParserMill4axisASyntec


class NcOperationMill4AxisASyntec(NcOperationMill3AxisSyntec):
    postprocessor_name = "MILL 4AXIS A SYNTEC POST"

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    def set_nc_sequences_objects_in_list(self):
        lst_of_objects = []
        nc_counter = 0
        for nc_sequence_name in self.list_of_nc_sequences_names:
            nc_counter += 1
            lst_of_objects.append(
                NcSequenceMill4AxisASyntec(
                    detail_name=self.detail_name,
                    nc_sequence_name=nc_sequence_name,
                    cl_list=self.cl_list,
                    nc_sequence_number=nc_counter,
                    nc_sequences_count=self.nc_sequences_count,
                    nc_operation_number=self.operation_number,
                    date_of_creation=self.date_of_creation
                )
            )
        self.list_of_nc_sequences_objects: list[NcSequenceMill4AxisASyntec] = lst_of_objects
