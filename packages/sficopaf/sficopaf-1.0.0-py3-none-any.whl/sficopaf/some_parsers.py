from io import TextIOBase
from typing import Dict, Union

import pandas as pd

from sficopaf import check_var


class NoConfigSectionError(Exception):
    """ This is raised whenever a configuration section does not exist in a config object.
    Like configparser.NoConfigSection but with a free error message."""


# Declare the two new subtypes that we'll use.
TsDataFrame = NewType('TsDataFrame', pd.DataFrame)
ParamDict = NewType('ParamDict', Dict[str, str])

# These are the currently supported file extensions for the various types of objects, and the associated readers
READERS = {
        TsDataFrame: {
            '.csv': read_tsdf_from_csv_file_stream
        },
        ParamDict: {
            '.cfg': read_dict_from_config_file_stream,
            '.xls': read_dict_from_xls_file_stream
        }
    }


# These have to be out of the class otherwise they can't be referenced from the static field "readers"
def read_dict_from_config_file_stream(file_object: TextIOBase, config_section_name: str = None) -> Union[
    Dict[str, str], Dict[str, Dict[str, str]]]:
    """
    Helper method to read a configuration file and return it as a dictionary. If a configuration section name is
    provided, the contents of this section will be returned as a dictionary. Otherwise a dictionary of dictionaries
    will be returned

    :param file_object:
    :param config_section_name: optional configuration section name to return
    :return:
    """
    check_var(file_object, var_types=TextIOBase, var_name='file_object')
    check_var(config_section_name, var_types=str, var_name='config_section_name', enforce_not_none=False)

    # see https://docs.python.org/3/library/configparser.html for details
    from configparser import ConfigParser
    config = ConfigParser()
    config.read_file(file_object)
    sections = config.sections()

    # convert the whole config to a dictionary of dictionaries
    config_as_dict = {
        section_name: {key: config[config_section_name][key] for key in config[config_section_name].keys()} for
        section_name in
        config.sections()}

    # return the required section or the whole configuration
    if config_section_name is None:
        return config_as_dict
    else:
        if config_section_name in config_as_dict.keys():
            return config_as_dict[config_section_name]
        else:
            raise NoConfigSectionError('Unknown configuration section : ' + config_section_name
                                       + '. Available section names are ' + str(config_as_dict.keys()))


def read_dict_from_xls_file_stream(file_object: TextIOBase) -> Dict[str, str]:
    """
    Helper method to read a dictionary from a single-row xls file

    :param file_object:
    :return:
    """
    pdf = read_paramdf_from_xls_file_stream(file_object)
    return FormatConverters.paramdf_to_paramdict(pdf)


def read_paramdf_from_xls_file_stream(file_object: TextIOBase) -> pd.DataFrame:
    """
    Helper method to read a dataframe with headers from a xls file stream. Note: this methods should be used for
    parameters, not for timeseries, since it does not enforce any timezone/time format parsing.

    :param file_object:
    :return:
    """
    check_var(file_object, var_types=TextIOBase, var_name='file_object')

    return pd.read_excel(file_object, header=0)


def read_tsdf_from_csv_file_stream(file_object: TextIOBase, col_separator: str = ',', decimal_char: str = '.',
                                   date_column_indices: List[int] = [0]) -> pd.DataFrame:
    """
    Helper method to read a csv file and return it as a timeseries dataframe. Ensures consistent reading in
    particular for timezones and datetime parsing

    :param file_object:
    :param col_separator:
    :param decimal_char:
    :param date_column_indices:
    :return:
    """

    check_var(file_object, var_types=TextIOBase, var_name='file_object')
    check_var(col_separator, var_types=str, var_name='col_separator')
    check_var(decimal_char, var_types=str, var_name='decimal_char')

    # 1- import a csv test file into pd dataframe
    data_frame = pd.read_csv(file_object, sep=col_separator, decimal=decimal_char,
                             infer_datetime_format=True, parse_dates=date_column_indices)

    # 2- time is in ISO format in our test files, so the time column after import is UTC. We just have to declare it
    datetimeColumns = [colName for colName, colType in data_frame.dtypes.items() if
                       np.issubdtype(colType, np.datetime64)]
    for datetimeCol in datetimeColumns:
        # time is in ISO format in our test files, so the time column after import is UTC. We just have to declare it
        data_frame[datetimeCol] = data_frame[datetimeCol].dt.tz_localize(tz="UTC")

    return data_frame


class FormatConverters:
    """
    A class with helper methods to convert formats.
    """

    @staticmethod
    def paramdf_to_paramdict(param_df: pd.DataFrame) -> Dict[str, str]:
        """
        Helper method to convert a parameters dataframe with one row to a dictionary.

        :param param_df:
        :return:
        """
        check_var(param_df, var_types=pd.DataFrame, var_name='param_df')

        if len(param_df.index.values) == 1:
            return {col_name: param_df[col_name][param_df.index.values[0]] for col_name in param_df.columns}
        else:
            raise ValueError('Unable to convert provided dataframe to a parameters dictionary : '
                             'expected exactly 1 row, found : ' + len(param_df.index.values))


