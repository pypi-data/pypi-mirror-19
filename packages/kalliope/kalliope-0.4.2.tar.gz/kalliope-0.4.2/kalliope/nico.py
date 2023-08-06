import time

import logging

from kalliope import ResourcesManager
from kalliope.core.ConfigurationManager.DnaLoader import DnaLoader
from kalliope.core.Models import Resources
from kalliope.core.Models.Dna import Dna

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.INFO)

# action = "install"
#
# parameter = {
#     "git_url": "https://github.com/kalliope-project/kalliope_neuron_wikipedia.git"
# }
#
# resourcemanager = ResourcesManager(**parameter)
# resourcemanager.install()


# dna_file = "/home/nico/Documents/kalliope_community_neurons/wikipedia_searcher/dna.yml"
#
# dna = DnaLoader(dna_file).get_dna()
#
# print dna

resources = Resources()
resources.neuron_folder = "/tmp"

dna = Dna()
dna.module_type = "stt"

ResourcesManager.is_settings_ok(resources, dna)