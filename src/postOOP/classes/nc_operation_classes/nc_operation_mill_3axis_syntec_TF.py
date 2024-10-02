from src.postOOP.classes.nc_operation_classes.nc_operation_basic_mill_syntec import NcOperationBasicMillSyntec
from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_3axis_syntec import NcSequenceMill3AxisSyntec
from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_3axis_syntec_TF import NcSequenceMill3AxisSyntecTF


class NcOperationMill3AxisSyntecTF(NcOperationBasicMillSyntec):
    postprocessor_name = "MILL 3AXIS SYNTEC TF POST"

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    def set_nc_sequences_objects_in_list(self):
        lst_of_objects = []
        nc_counter = 0
        for nc_sequence_name in self.list_of_nc_sequences_names:
            nc_counter += 1
            lst_of_objects.append(
                NcSequenceMill3AxisSyntecTF(
                    detail_name=self.detail_name,
                    nc_sequence_name=nc_sequence_name,
                    cl_list=self.cl_list,
                    nc_sequence_number=nc_counter,
                    nc_sequences_count=self.nc_sequences_count,
                    nc_operation_number=self.operation_number,
                    date_of_creation=self.date_of_creation
                )
            )
        self.list_of_nc_sequences_objects: list[NcSequenceMill3AxisSyntecTF] = lst_of_objects
