# agent_map_data.py   written by Duncan Murray 30/9/2014

import os
import aikif.agents.agent as mod_agt

class AgentMapDataFile(object):
    def __init__(self, list_name, src_file, mapping):
        """
        class to map a data file to aikif structures
        """
        self.name = list_name
        self.list = []
        self.process = []
        self.mapping = mapping
        self.src_file = src_file
        
    def __str__(self):
        """
        returns the name and list of mappings
        """
        txt = self.name + '\n'
        txt += '------------------------------\n'
        for num, mp in enumerate(self.mapping):
            txt += str(num).zfill(3) + ' ' + mp + '\n'
        for proc in self.process:
            txt +=  proc + '\n'
        return txt

    def map_data(self):
        """
        provides a mapping from the CSV file to the 
        aikif data structures.
        """
        with open(self.src_file, "r") as f:
            for line in f:
                cols = line.split(',')
                print(cols)
                
    def add_process(self, proc):
        """
        adds to processes
        """
        self.process.append(proc)
        

