import sys
import json
from datetime import datetime, timedelta
import random

"""
Call this script with the following command:
python <path to script> <path to config.json>

eg: python generate_sequence.py config.json
"""

class GenerateSequenceOfItems:
    """
    Main exercise class to process a json input and return sequenced items via standard out.

    Brief:
    The output of your code should be written to standard out. 
    It should be a json object representation for each item, separated by a newline character (\n).
    Items have the following attributes:
    • id
    • timestamp (time of detection)
    • material_type (plastic, paper, etc.)
    • colour (item colour)
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.starting_timestamp = datetime.now()


    def check_file_format(self) ->bool:
        """
        Corner case
        Check input file to ensure it is of type json
        :return: bool
        """
        if self.file_path.split(".")[-1].upper() != "JSON":
            return False
        return True

    def parse_config(self) -> dict:
        """
        Parse config file
        Open file using python context manager and convert data to python object
        :return: dict
        """

        file_exception = ("Please provide valid json file.")
        
        if self.check_file_format:
            
            try:
                # Open config file using the open() function
                file = open(self.file_path, 'r')
                # Convert the JSON data into Python object
                config_dict = json.load(file)
                # Close config file using the close() function
                file.close()
                return config_dict

            except (FileNotFoundError, OSError, Exception):
                raise Exception(file_exception)
        else:
            raise Exception(file_exception)


    def get_duration(self, config:dict)->int:
        """
        Get sequence duration from config data
        :param: dict
        :return: int
        """
        try:
            return int(config["duration"]) 
        except KeyError:
            Exception('Missing attribute: "duration" is required.')
        except ValueError:
            Exception('Incorrect attribute type: "duration" must be type "int".')

    def get_colour_attribute(self, config:dict)->str:
        """
        Get colour from config data
        :param: dict
        :return: str
        """
        try:
            #Get the value (list) from the attribute key
            colour_list = config["attributes"]["colour"]["values"]
            #Use random to grab a random colour from given list
            colour = random.choice(colour_list)
            return str(colour)
        except KeyError:
            return None

    def get_material_attribute(self, config:dict):
        """
        Get material from config data
        :param: dict
        :return: str
        """
        try:
            #Get the value (list) from the attribute key
            material_list = config["attributes"]["material"]["values"]
            #Use random to grab a random material from given list
            material = random.choice(material_list)
            return str(material)
        except KeyError:
            return None

    def get_rate(self, config:dict)-> int:
        """
        Get rate from config data
        :param: dict
        :return: int
        """
        try:
            rate_min = config["rate"]["min"]
            rate_max = config["rate"]["max"]
            rate = random.randint(int(rate_min), int(rate_max))
            return rate
        except ValueError:
            Exception('Incorrect attribute type: "rate.min" and "rate.max" must be type "int".')
        except (KeyError, TypeError):
            try:
                return int(config["rate"])
            except:
                Exception('Incorrect attribute type: "rate" must be type "int".')

    
    def build_base_dict(self, id:int)->dict:
        """
        Build a dict with common denominators: id and timestamp.
        ID is used to manage the timestamp as it is sequenced
        Increment starting_timestamp by a X second timedelta
        :param: int
        :return: dict
        """
        timestamp = self.starting_timestamp + timedelta(0, id-1)
        sequence = {
            "id": id,
            "timestamp": timestamp.strftime("%Y-%d-%m, %H:%M:%S")
        }
        return sequence


    def generate_sequence(self):
        """
        Main method to process input data
        :return: standard out json
        """
        
        #parse and validate the config file
        config = self.parse_config()

        #call class methods to get duration and rate
        duration = self.get_duration(config)
        rate = self.get_rate(config)

        """
        build a list of sequences.
        Example
        [
         {
          'id': 2, 
          'timestamp': '2023-12-01, 13:01:21'
         }, 
         {
           'id': 3, 
           'timestamp': '2023-12-01, 13:01:22'
         } 
        ]
        """
        sequence_list = []

        id_calculator = 1

        # Note list comprehension would have worked here. However, in this case, i felt 
        # it was easier to read as 2 for loops
        for d in range(duration):
            for r in range(rate):

                #build base dict
                sequence = self.build_base_dict(id_calculator)
                
                #increment id_calculator by 1
                id_calculator += 1

                #handle randomized colour
                colour = self.get_colour_attribute(config)
                if colour:
                    sequence["colour"] = colour

                #handle randomized material
                material = self.get_material_attribute(config)
                if material:
                    sequence["material"] = material
                
                #append results to list
                sequence_list.append(sequence)

        #sort response in timestamp order
        sequence_list.sort(key=lambda item:item['timestamp'], reverse=False)

        for sequence in sequence_list:
            #print each result to standard out
            print(json.dumps(sequence))

"""
Remove 1st argument from the
list of command line arguments
FYI - the first arg is the file name
"""
file_path = sys.argv[1:][0]
GenerateSequenceOfItems(file_path).generate_sequence()



