from src.postOOP import config


def execute_postprocess(post_obj):
    operations = list()

    filepath = config.work_ncl_file_path
    if filepath:
        operations.append(post_obj())

    for operation in operations:
        operation.start_postprocessing()
