"""
This module has functions to generate simple tabular reports.

:Written By:
    John Glasgow
    (Northampton Community College)
"""

import sys
from io import TextIOWrapper

__version__ = "1.0.0"

justify_options = {"left": "<",
                   "center": "^",
                   "right": ">"}


def column_generator(list_of_column_widths: list, fill=" ", justify_text=justify_options["left"]) -> str:
    """
    Creates a format string, specifying each of the column widths, the character to pad the columns(fill), and the
    justification of the text.
    :param list_of_column_widths: A list of numeric data types that will specify the width of each column.
    :param fill: By default this is whitespace, however it can be changed else. Should be a single character.
    :param justify_text: Can use the formatstring syntax or use justify_options referencing left, center, or right.
    :return: Formatstring that can be used in the column_format parameter of generate_report.
    """
    formatted_list = ["{:" + fill + justify_text + str(column) + "}" for column in list_of_column_widths]
    formatted_string = "{}\n".format("".join(formatted_list))  # joining the list of string formats
    return formatted_string


def title_generator(title: str, gutter: int) -> str:
    """
    Creates a boilerplate title, centered between two lines of equal signs.
    :param title: Text to be the title.
    :param gutter: Space on the sides of the title.
    :return: The finished boilerplate title.
    """
    header = column_generator([len(title) + gutter, ], "=", justify_options["left"]).format("=")
    header += column_generator([len(title) + gutter, ], " ", justify_options["center"]).format(title)
    header += column_generator([len(title) + gutter, ], "=", justify_options["left"]).format("=")
    return header


def generate_report(title: str, column_header: str, column_format: str, data):
    """
    Creates a report as a string.
    :param title: Title, can use the title_generator function for a nicely formatted title.
    :param column_header: Row(s) of text that represents the columns' names. Use of the column_generator is recommended.
    :param column_format: Formatstring representing how the columns should display. Use of the column_generator is recommended.
    :param data: List of the rows to display, should be iterable.
    :return: String containing the report.
    """
    report = "{title}{column_header}{header_closing}\n".format(title=add_newline(title),
                                                               column_header=add_newline(column_header),
                                                               header_closing=column_generator([len(column_header), ],
                                                                                               "=")).format("=")
    for item in data:
        report += column_format.format(*item)
    return report


def display_report(generated_report: str, file_name: str = None):
    """
    Displays report to stdout or to a specified file.
    :param generated_report: String of text to write to stdout or file.
    :param file_name: Path to the file.  Omit to display through the console.
    """
    out_file = _open_output(file_name)
    print(generated_report, file=out_file)
    _close_output(out_file)


def add_newline(text: str) -> str:
    """
    Adds a newline if a string does not have one.
    :param text: String to add the newline character to.
    :return: String with a newline character on the end.
    """
    return text if text.endswith("\n") else text + "\n"


def _close_output(out_file: TextIOWrapper):
    """
    Closes the output. Does not close stdout.
    :param out_file: File object to close
    """
    if out_file is not sys.stdout:
        out_file.close()


def _open_output(file_name: str = None) -> TextIOWrapper:
    """
    Opens a file for output if one is specified, else uses stdout.
    :param file_name: Path to the file that is to be overwritten.
    :return: File object for saving the report to.
    """
    out_file = open(file_name, "w") if file_name else sys.stdout
    return out_file
