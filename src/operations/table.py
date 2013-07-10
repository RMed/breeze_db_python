# This file is part of BreezeDB - https://github.com/RMed/breeze_db
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import xml.etree.ElementTree as XML
import os

class TableException(Exception):
    """Class for exceptions in Table module."""
    def __init__(self, value):
        print 'Table exception: ', value

def table_exists(table_name, database):
    """Check whether a table exists in the database or not.

    Returns True in case the table exits and False in case it does not.

    Arguments:
        table_name -- Name of the table to check
        database -- Database to check (usually obtained from the Connector)
    """
    # Check the root.breeze file for the table
    root_breeze = os.path.join(database, 'root.breeze')
    tree = xmltree.parse(root_file)
    # Get the root of the tree
    root = tree.getroot()    
    # Check if the table is listed
    table_exists = False
    for table in root:
        if table.text == table_name:
            # Table exists in the file
            table_exists = True
            break

    # Does the table exist in the file?
    if table_exists == False:
        return False

    # Check if the directory corresponding to the table exists
    table_path = os.path.join(database, table_name)
    if os.path.exists(table_path):
        # Directory exists
        return True

def add_table(table_name, database):
    """Add a table to the database.

    Add a new <table> element to the root.breeze file and create the
    corresponding table structure.

    Arguments:
        table_name -- Name of the table to create
        database -- Database to check (usually obtained from the Connector)
    """

    # Check for write access in the database
    can_write = os.access(database, os.W_OK)

    if !can_write:
        # Raise exception
        raise TableException('cannot write to database')

    # Add <table> element to root.breeze and create table structure
    try:
        # Add <table> element
        # Parse the file
        breeze_file = os.path.join(database, 'root.breeze')
        tree = XML.parse('breeze_file')
        root = db_root.getroot()

        # Add element to root
        new_table = XML.Element('table')
        new_table.text = table_name
        root.append(new_table)

        # Write to file
        tree.write(breeze_root)

        # Create directory
        newdir = os.path.join(database, table_name)
        os.makedirs(newdir)

        # Create tableinfo.breeze file
        tableinfo_file = os.path.join(newdir, tableinfo.breeze)
        breeze_tag = XML.Element('breeze')
        output = open(tableinfo_file, 'w')
        output.write(XML.tostring(breeze_tag)
        output.close()

    except OSError:
        # Raise exception
        raise TableException('could not create base directory')

    except IOError:
        # Raise exception
        raise ConnectorException('error creating tableinfo.breeze file')
