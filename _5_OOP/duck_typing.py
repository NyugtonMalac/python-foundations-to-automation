"""
ducktyping.py

Demonstrates the concept of duck typing in object-oriented programming.

The module defines multiple handler classes (CsvHandler, JsonHandler, XmlHandler)
that share the same interface: an `export()` method.

Each handler is responsible for exporting data into a different file format
(JSON, CSV, or XML).

The `export_data()` function accepts any object that implements
an `export()` method, illustrating duck typing in practice.
"""

####################### SETTINGS #######################

import sys
import os
import logging
import json
import csv
import xml.etree.ElementTree as ET

# Add the helpers directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                 '../_0_helpers'))
                                ) 

from path_utils import set_base_dir, get_file_path
from setup_logger_v1 import setup_logger


# Configure base directory for file operations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
set_base_dir(BASE_DIR)

# Create a module-level logger
logger = logging.getLogger(__name__)

ENCODING = "utf-8"

####################################################

class CsvHandler:
    """
    Handles exporting data to CSV format.

    Supports:
    - A single dictionary (written as one row)
    - A list of dictionaries (written as multiple rows)

    The CSV header is generated from dictionary keys.
    """

    def __init__(self):
        pass

    def dict_data(self, data:dict, path):
        """
        Export a single dictionary to a CSV file as one row.

        Args:
            data (dict): Dictionary containing the data to export.
            path (str): Absolute file path for the CSV file.

        Raises:
            TypeError: If serialization fails.
            OSError: If the file cannot be created or written.
        """
        
        try:
            with open(path, "w", newline="", encoding=ENCODING) as file:
                fieldnames = list(data.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow(data)

                logger.info("CSV file successfully created at %s", path)
                return
        except TypeError as e:
            logger.error("CSV serialization failed: %s", e)
            raise
        except OSError as e:
            logger.error("CSV file cannot be created or written: %s", e )
            raise  

    def list_of_dict(self, data: list, path):
        """
        Export a list of dictionaries to a CSV file.

        The CSV header is generated from the union of all dictionary keys.
        Missing values are written as empty cells.

        Args:
            data (list): List of dictionaries to export.
            path (str): Absolute file path for the CSV file.

        Raises:
            TypeError: If serialization fails.
            OSError: If the file cannot be created or written.
        """

        field_set = set()

        for item in data:
            field_set.update(item.keys())

        try:
            with open(path, "w", newline="", encoding=ENCODING) as file:
                
                fieldnames = list(field_set)
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                for item in data:
                    writer.writerow(item)

                logger.info("CSV file successfully created at %s", path)
                return
        except TypeError as e:
            logger.error("CSV serialization failed: %s", e)
            raise
        except OSError as e:
            logger.error("CSV file cannot be created or written: %s", e )
            raise                    
    

    def other_data(self):
        raise TypeError("Data must be either a dictionary or a list of dictionaries.")    
        
    def export(self, data, file_name:str = "data_export", file_extension:str = ".csv"):
        
        path = get_file_path(file_name, file_extension)

        if isinstance(data, dict):
            return self.dict_data(data=data, path=path)
        elif data and isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return self.list_of_dict(data=data, path=path)
        else:
            return self.other_data()
        
            

class JsonHandler:
    """
    Handles exporting data to JSON format.

    The handler creates (or overwrites) a JSON file and writes the given data
    using UTF-8 encoding.
    """

    def __init__(self):
        pass

    def export(self, data:dict, file_name:str ="data_export", file_extension:str =".json"):
        """
        Export data to a JSON file.

        Creates (or overwrites) the target file and serializes the provided data
        as JSON.

        Args:
            data (dict): Data to serialize to JSON (must be JSON-serializable).
            file_name (str): Output file name without extension.
            file_extension (str): File extension (default is ".json").

        Raises:
            TypeError: If the data is not JSON-serializable.
            OSError: If the file cannot be created or written.
        """

        path = get_file_path(file_name, file_extension)

        try:                
            with open(path, "w", encoding=ENCODING) as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                logger.info("JSON file successfully created at %s", path)
        except TypeError as e:
            logger.error("JSON serialization failed: %s", e)
            raise
        

class XmlHandler:
    """
    Handles exporting data to XML format.
    """

    def __init__(self):
        pass

    def dict_data(self, data:dict, root_data="data"): 
        """
        Build an XML element tree from a dictionary and return the root element.
        """

        # Create the root element
        root = ET.Element(root_data)

        # Add child elements from key-value pairs
        for key,value in data.items():
            
            child = ET.SubElement(root, key)
            child.text = str(value)
        
        return root

    def list_of_dict(self, data:list):
        """
        Build an XML element tree from a list of dictionaries and return the root element.
        """

        # Create the root element
        root = ET.Element("data")

        for record in data:
            item_elem = self.dict_data(data=record, root_data="item")
            # Append each <item> element under the root
            root.append(item_elem)

        return root
    
    def file_writing(self, root, path):
        """
        Write the given XML root element to a file with pretty indentation.
        """

        try: 
            tree = ET.ElementTree(root)
            ET.indent(tree, space="    ")
            tree.write(path, encoding=ENCODING, xml_declaration=True)
            logger.info("XML file successfully created at %s", path)
        except TypeError as e:
            logger.error("XML creation failed: %s", e)
            raise 

    def other_data(self):
        raise TypeError("Data must be either a dictionary or a list of dictionaries.") 

    def export(self, data, file_name:str ="data_export", file_extension:str =".xml"):
        
        path = get_file_path(file_name, file_extension)

        if isinstance(data, dict):
            return self.file_writing(self.dict_data(data=data), path=path)
        elif data and isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return self.file_writing(self.list_of_dict(data=data), path=path)
        else:
            return self.other_data()



data = [
    {
        "id": 101,
        "name": "Anna Kovacs",
        "department": "Data Engineering",
        "email": "anna.kovacs@example.com",
        "salary": 72000,
        "active": True
    },
    {
        "id": 102,
        "name": "David Nagy",
        "department": "Automation",
        "email": "david.nagy@example.com",
        "salary": 68000,
        "active": True
    },
    {
        "id": 103,
        "name": "Sofia Toth",
        "department": "Analytics",
        "email": "sofia.toth@example.com",
        "salary": 75000,
        "active": False
    }
]

def export_data(handler, data:dict):

    handler.export(data=data)


####################### MAIN #######################

def main():
    setup_logger(name = "duck_typing_OOP", log_file="logs/ducktyping.log")
    logger.info("Application started.")
    
    csv_handler = CsvHandler()
    json_handler = JsonHandler()
    xml_handler = XmlHandler()

    export_data(handler=csv_handler, data=data)
    export_data(handler=json_handler, data=data)
    export_data(handler=xml_handler, data=data)

    logger.info("Application finished.")


if __name__ == "__main__":
    main()