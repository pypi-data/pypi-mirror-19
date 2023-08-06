# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""

import os
import random
import shutil
import string
import tempfile
import unittest

import dicom2nifti.convert_generic as convert_generic
import tests.test_data as test_data
from dicom2nifti.common import is_dicom_file, read_dicom_directory
from tests.test_tools import compare_nifti, ground_thruth_filenames


class TestConversionGeneric(unittest.TestCase):
    def test_anatomical(self):
        tmp_output_dir = tempfile.mkdtemp()
        try:
            results = convert_generic.dicom_to_nifti(read_dicom_directory(test_data.GE_ANATOMICAL),
                                                     os.path.join(tmp_output_dir, 'test.nii.gz'))
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GE_ANATOMICAL)[0]) == True

        finally:
            shutil.rmtree(tmp_output_dir)

    def test_is_dicom_file(self):
        input_file = os.path.join(test_data.GENERIC_COMPRESSED, 'IM-0001-0001-0001.dcm')
        assert is_dicom_file(input_file)
        temporary_directory = tempfile.mkdtemp()
        try:
            # test for empty file
            non_dicom1 = os.path.join(temporary_directory, 'non_dicom.dcm')
            open(non_dicom1, 'a').close()
            assert not is_dicom_file(non_dicom1)
            # test for non empty file
            non_dicom2 = os.path.join(temporary_directory, 'non_dicom2.dcm')
            with open(non_dicom2, 'w') as file_2:
                file_2.write(''.join(random.SystemRandom().choice(string.digits) for _ in range(300)))

            assert not is_dicom_file(non_dicom2)
        finally:
            shutil.rmtree(temporary_directory)


if __name__ == '__main__':
    unittest.main()
