import data.migrations.layers as layers
import json


async def apply_available_migrations(data_file, to_version):
    current_version = _determine_data_file_version(data_file)
    while current_version < to_version:
        await _migrate(data_file, current_version)
        current_version = _determine_data_file_version(data_file)


def _determine_data_file_version(data_file):
    with open(data_file, "r") as file:
        data = json.load(file)
        if type(data) is list:
            return 0
        else:
            return data["data-version"]


async def _migrate(data_file, version):
    if version == 0:
        await layers.apply_layer_0(data_file)
