from src.postOOP.classes.nc_operation_classes.nc_operation import NcOperation
from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_3axis import NcSequenceMill3Axis
from src.postOOP.classes.nc_sequence_classes.nc_sequence_mill_3axis_tf import NcSequenceMill3AxisTF


class NcOperationMill3AxisTF(NcOperation):
    postprocessor_name = "TF Basic 3 axis mill post Syntec"

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
        # self.set_nc_sequences_objects_in_list()

    def set_nc_sequences_objects_in_list(self):
        lst_of_objects = []
        nc_counter = 0
        for nc_sequence_name in self.list_of_nc_sequences_names:
            nc_counter += 1
            lst_of_objects.append(
                NcSequenceMill3AxisTF(
                    detail_name=self.detail_name,
                    nc_sequence_name=nc_sequence_name,
                    cl_list=self.cl_list,
                    nc_sequence_number=nc_counter,
                    nc_sequences_count=self.nc_sequences_count,
                    nc_operation_number=self.operation_number,
                    date_of_creation=self.date_of_creation
                )
            )
        self.list_of_nc_sequences_objects: list[NcSequenceMill3Axis] = lst_of_objects
