# DICOM 데이터를 읽은 뒤, Tag(patient name, id 등...)를 교체하여 익명화 함 (클라우드 서비스와 관련?)

import tempfile

import pydicom
from pydicom.data import get_testdata_files

print(__doc__)

filename = get_testdata_files('MR_small.dcm')[0]
dataset = pydicom.dcmread(filename)

# Dataset에서 사용자 이름에 해당하는 모든 태그를 찾는 콜백함수
def person_names_callback(dataset, data_element):
    if data_element.VR == "PN": # VR-> PN (환자이름)
        data_element.value = "anonymous"

dataset.PatientID = "id"
dataset.walk(person_names_callback) # walk : walk(callback, recursive=True)  : Iterate through the Dataset's elements and run callback on each.

# private tags 삭제
dataset.remove_private_tags()

# optional (type3) data element는 del, delattr 메서드로 삭제 가능
if 'OtherPatientIDs' in dataset:
    delattr(dataset, 'OtherPatientIDs')

if 'OtherPatientIDsSequence' in dataset:
    del dataset.OtherPatientIDsSequence

# type2 의 dataelement는 빈 문자열을 할당하여 blanking 가능
tag = 'PatientBirthDate'
if tag in dataset:
    # dataset.data_element(tag).value = '19000101'
    dataset.data_element(tag).value = ''

data_elements = ['PatientID',
                 'PatientBirthDate']

for de in data_elements:
    print(dataset.data_element(de))

# store the image
output_filename = tempfile.NamedTemporaryFile().name
dataset.save_as(output_filename)