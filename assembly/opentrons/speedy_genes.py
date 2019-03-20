'''
AssemblyGenie (c) University of Manchester 2019

All rights reserved.

@author: neilswainston
'''
# pylint: disable=too-few-public-methods
# pylint: disable=wrong-import-order
from itertools import permutations
import sys

from opentrons import robot

from assembly.opentrons import utils
import pandas as pd


class PcrWriter():
    '''Class representing an PCR writer.'''

    def __init__(self, src_plate_dfs, products):
        self.__products = products

        self.__oligos = {fragment
                         for product in products
                         for fragment in product}

        self.__tip_racks = \
            utils.add_container((len(self.__oligos) - 1 // 8) + 1  # oligos
                                + 16,  # water and mastermix
                                typ='opentrons-tiprack-300ul')

        self.__product_plates = utils.add_container(len(self.__products),
                                                    '96-PCR-flat')

        self.__src_plates = [utils.add_plate(src_plate_df, '96-PCR-flat')
                             for src_plate_df in src_plate_dfs]

    def write(self):
        '''Write commands.'''
        for product in self.__products:
            print(product)


def _get_variants(block, num_variant):
    '''Get variants.'''
    variants = list(permutations(block, num_variant))

    return [['%sv' % oligo if oligo in variant else oligo
             for oligo in block]
            for variant in variants]


def main(args):
    '''main method.'''
    plate = pd.read_csv(args[0])
    plate.name = args[0]

    blocks = [['1', '2', '3', '4', '5', '6', '7', '8'],
              ['9', '10', '11', '12', '13', '14', '15', '16']]

    num_variants = [0, 1, 2]

    designs = [[var for lst in [_get_variants(block, num_variant)
                                for num_variant in num_variants]
                for var in lst]
               for block in blocks]

    writer = PcrWriter([plate], [product
                                 for design in designs
                                 for product in design])
    writer.write()

    for command in robot.commands():
        print(command)


if __name__ == '__main__':
    main(sys.argv[1:])
