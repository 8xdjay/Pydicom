# DICOM Dataset을 Byte Array로 write 후, Byte Array에서 다시 읽는 방법을 표시
# 데이터베이스에 blobs로 저장된 데이터셋을 사용하는 경우에 유용함.

from io import BytesIO

from pydicom import dcmread, dcmwrite
from pydicom.filebase import DicomFileLike

print(__doc__)

usage = "Usage: python MemoryBasedDataset.py dicom_filename"


def write_dataset_to_bytes(dataset):
    # 버퍼 생성
    with BytesIO() as buffer:
        # DicomFileLike 오브젝트 생성
        memory_dataset = DicomFileLike(buffer)
        dcmwrite(memory_dataset, dataset)
        
        memory_dataset.seek(0)
        
        return memory_dataset.read()


def adapt_dataset_from_bytes(blob):

    dataset = dcmread(BytesIO(blob))
    
    dataset.is_little_endian = False
    dataset.PatientName = 'Bond^James'
    dataset.PatientID = '007'
    return dataset


class DummyDataBase:
    def __init__(self):
        self._blobs = {}

    def save(self, name, blob):
        self._blobs[name] = blob

    def load(self, name):
        return self._blobs.get(name)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Please supply a dicom file name:\n")
        print(usage)
        sys.exit(-1)
    file_path = sys.argv[1]
    
    db = DummyDataBase()

    dataset = dcmread(file_path)
    print(dataset)

    ds_bytes = write_dataset_to_bytes(dataset)
    db.save('dataset', ds_bytes)

    read_bytes = db.load('dataset')
    read_dataset = adapt_dataset_from_bytes(read_bytes)
    print(read_dataset)
    dcmwrite(file_path + '_new', read_dataset)