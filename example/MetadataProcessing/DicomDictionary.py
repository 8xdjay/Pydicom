# HL7 V2.x 의 Z 세그먼트와 같이 추가적으로 필요한 경우 Custom Dicom 항목을 추가할 수 있을 듯.
# Note that this is not a recommended solution in general but it is useful as a demonstration or for in-house programs only, 
# or to get around elements missing from pydicom’s DICOM dictionaries.

from pydicom.datadict import DicomDictionary, keyword_dict
from pydicom.dataset import Dataset

print(__doc__)

#   Define items as (VR, VM, description, is_retired flag, keyword)
#   Leave is_retired flag blank.
new_dict_items = {
    0x10011001: ('UL', '1', "Test One", '', 'A'),
    0x10011002: ('OB', '1', "Test Two", '', 'B'),
    0x10011003: ('UI', '1', "Test Three", '', 'C'),
}

# Update the dictionary itself
DicomDictionary.update(new_dict_items)

# Tag를 맵핑하여 Value Update
new_names_dict = dict([(val[4], tag) for tag, val in
                       new_dict_items.items()])
keyword_dict.update(new_names_dict)

ds = Dataset()  # or could get one from dcmread, etc
ds.A = 42
ds.B = '12345'
ds.C = '1.2.3.4.5'

print(ds.top())

'''
output
(1001, 1001) Private tag data                    UL: 42
(1001, 1002) Private tag data                    OB: '12345'
(1001, 1003) Private tag data                    UI: 1.2.3.4.5
'''