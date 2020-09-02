
'''
Sequence : multiple dataset을 보유하기 위한 클래스

This class is derived from MultiValue and as such enforces that all items added to the list are Dataset instances. 
In order to do this, a validator is substituted for type_constructor when constructing the MultiValue super class.

링크 : https://pydicom.github.io/pydicom/dev/reference/generated/pydicom.sequence.Sequence.html
'''

from pydicom.sequence import Sequence
from pydicom.dataset import Dataset

# create to toy datasets
block_ds1 = Dataset()
block_ds1.BlockType = "APERTURE"
block_ds1.BlockName = "Block1"

block_ds2 = Dataset()
block_ds2.BlockType = "APERTURE"
block_ds2.BlockName = "Block2"

# block type, name 외에도, Material ID, Block Tray ID, Bloc Divergence 등의 데이터 추가 가능

beam = Dataset()

plan_ds = Dataset()
plan_ds.BeamSequence = Sequence([beam])
plan_ds.BeamSequence[0].BlockSequence = Sequence([block_ds1, block_ds2])
plan_ds.BeamSequence[0].NumberOfBlocks = 2

beam0 = plan_ds.BeamSequence[0]
print('Number of blocks: {}'.format(beam0.BlockSequence))

block_ds3 = Dataset()
# add data elements to it as above and don't forget to update Number of Blocks
beam0.BlockSequence.append(block_ds3)
beam0.NumberOfBlocks = 3 # Block을 append하여, Number of Block 업데이트..?

# del plan_ds.BeamSequence[0].BlockSequence[1]