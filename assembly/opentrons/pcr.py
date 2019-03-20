'''
AssemblyGenie (c) University of Manchester 2019

All rights reserved.

@author: neilswainston
'''
# pylint: disable=too-few-public-methods
# pylint: disable=ungrouped-imports
from collections import defaultdict

from opentrons import instruments, labware

from assembly.opentrons import utils


class PcrWriter():
    '''Class representing an PCR writer.'''

    def __init__(self, src_plate_dfs, products):
        self.__plt_mgr = utils.PlateManager()
        self.__products = products
        self.__fragments = defaultdict(list)

        for product_id, product in products.items():
            for frag_idx, fragment in enumerate(product):
                self.__fragments[fragment].append(
                    (product_id, frag_idx in [0, len(fragment) - 1]))

        # Add trash:
        self.__trash = labware.load('trash-box', '1')

        # Add tipracks:
        tip_racks = \
            self.__plt_mgr.add_containers('opentrons-tiprack-300ul',
                                          (len(self.__fragments) -
                                           1 // 8) + 1  # oligos
                                          + 16)  # water and mastermix

        # Add water-trough:
        self.__plt_mgr.add_container('trough-12row', ['water'],
                                     name='water')

        # Add plates:
        self.__plt_mgr.add_containers('96-PCR-flat',
                                      self.__products.keys())

        for src_plate_df in src_plate_dfs:
            self.__plt_mgr.add_plate_df('96-PCR-flat', src_plate_df)

        # Add pipettes:
        self.__single_pipette = \
            instruments.P300_Single(mount='left', tip_racks=tip_racks)

        self.__multi_pipette = \
            instruments.P50_Multi(mount='right', tip_racks=tip_racks)

    def write(self):
        '''Write commands.'''
        self.__add_water()
        self.__add_fragments()
        self.__add_mastermix()

    def __add_water(self):
        '''Add water.'''
        pass

    def __add_mastermix(self):
        '''Add water.'''
        pass

    def __add_fragments(self, primer_vol=5, internal_vol=1):
        '''Add fragments.'''
        for fragment, prods in self.__fragments.items():
            src_plate, src_well = \
                self.__plt_mgr.get_plate_well([fragment])[0]

            prod_plate_wells = defaultdict(list)

            for plate_well in self.__plt_mgr.get_plate_well(list(zip(*prods))[0]):
                prod_plate_wells[plate_well[0]].append(plate_well[1])

            for prod_plate, prod_wells in prod_plate_wells.items():
                self.__single_pipette.distribute(internal_vol,
                                                 src_plate.wells(src_well),
                                                 prod_plate.wells(prod_wells))
