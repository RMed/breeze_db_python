# -*- coding: utf-8 -*-
#
# This file is part of BreezeDB - https://github.com/RMed/breezedb_python
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
.. module:: element
    :platform: Unix, Windows
    :synopsis: Element related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import xml.etree.ElementTree as XML
import os, string
from breeze_exceptions import BreezeException

def element_exists(element_index, field_name, table_name, database):
    """ Check whether an element exist in the field.

        :param int element_index: index of the element to check
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :returns: True or false

        :raises BreezeException: supplied index is not a positive integer
    """
    if element_index < 0:
        raise BreezeException('element', 'index needs to be a positive integer')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    last_index = int(field_root[-1].get('index'))
    if element_index <= last_index:
        return True
    else:
        return False

def get_element_content(element_index, field_name, table_name, database):
    """ Get the data contained in an element.

        Returns the contained data as a string, so it must be parsed 
        accordingly.

        .. todo:: Parse the data automatically given a list of available types.

        :param int element_index: index of the element
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :returns str: content of the element
    """
    if not element_exists(element_index, field_name, table_name, database):
        raise BreezeException('element', 'the element does not exist')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    return field_root.findall('element')[element_index].text

def find_element(to_find, field_name, table_name, database):
    """ Find elements in the field.

        :param str to_find: data to find
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :returns: list of indexes that match the criteria
    """
    indexlist = []

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    for element in field_root.iter('element'):
        if string.lower(str(to_find)) in string.lower(str(element.text)):
            indexlist.append(element.get('index'))

    return indexlist

def modify_element(element_index, new_content, field_name,
                    table_name, database):
    """ Modify the content of an element.

        :param int element_index: index of the element to modify
        :param str new_content: new content to store in the element
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :raises BreezeException: element does not exist
    """
    if not element_exists(element_index, field_name, table_name, database):
        raise BreezeException('element', 'the element does not exist')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    field_root.findall('element')[element_index].text = str(new_content)

    field_tree.write(field_file)

def empty_element(element_index, field_name, table_name, database):
    """ Empty the content of an element.

        The content is emptied instead of removing the whole element because
        a single element cannot be removed, as the indexes of other fields
        would not match.

        :param int element_index: index of the element to empty
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :raises BreezeException: element does not exist
    """
    if not element_exists(element_index, field_name, table_name, database):
        raise BreezeException('element', 'the element does not exist')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    field_root.findall('element')[element_index].text = ""

    field_tree.write(field_file)

def remove_element_row(element_index, table_name, database):
    """ Remove an element row from the specified table.

        Removes all the elements that correspond to that index and then
        updates the rest of the indexes of the files.

        :param int element_index: index of the element row to remove
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :raises BreezeException: element does not exist,
            element row cannot be removed
    """
    table_file = os.path.join(database, table_name, 'tableinfo.breeze')
    table_tree = XML.parse(table_file)
    table_root = table_tree.getroot()

    for field in table_root:

        if not element_exists(element_index, field.text, table_name, database):
            raise BreezeException('element', 'the element does not exist')

        try:
            field_file = os.path.join(database, table_name, field.text)
            field_tree = XML.parse(field_file)
            field_root = field_tree.getroot()        

            field_root.remove(field_root.findall('element')[element_index])

            for element in field_root.iter('element'):
                if int(element.get('index')) > element_index:
                    element.set('index', str(int(element.get('index')) - 1))

            field_tree.write(field_file)

        except OSError:
            raise BreezeException('element', 'could not remove element')
