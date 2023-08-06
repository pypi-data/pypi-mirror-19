# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""

import os
import shutil
import tempfile
import unittest

import dicom2nifti.convert_dicom as convert_dicom
import dicom2nifti.tests.test_data as test_data
from dicom2nifti.common import read_dicom_directory
from dicom2nifti.tests.test_tools import compare_nifti, ground_thruth_filenames


class TestConversionDicom(unittest.TestCase):
    def test_anatomical(self):
        tmp_output_dir = tempfile.mkdtemp()
        try:
            results = convert_dicom.dicom_series_to_nifti(test_data.SIEMENS_ANATOMICAL,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          False)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.SIEMENS_ANATOMICAL)[0]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.SIEMENS_ANATOMICAL,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          True)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.SIEMENS_ANATOMICAL)[1]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.SIEMENS_ANATOMICAL_IMPLICIT,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          False)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.SIEMENS_ANATOMICAL_IMPLICIT)[0]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.SIEMENS_ANATOMICAL_IMPLICIT,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          True)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.SIEMENS_ANATOMICAL_IMPLICIT)[1]) == True


            results = convert_dicom.dicom_series_to_nifti(test_data.GENERIC_ANATOMICAL,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          False)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GENERIC_ANATOMICAL)[0]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.GENERIC_ANATOMICAL,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          True)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GENERIC_ANATOMICAL)[1]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.GENERIC_ANATOMICAL_IMPLICIT,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          False)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GENERIC_ANATOMICAL_IMPLICIT)[0]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.GENERIC_ANATOMICAL_IMPLICIT,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          True)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GENERIC_ANATOMICAL_IMPLICIT)[1]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.GENERIC_COMPRESSED,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          False)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GENERIC_COMPRESSED)[0]) == True

            results = convert_dicom.dicom_series_to_nifti(test_data.GENERIC_COMPRESSED,
                                                          os.path.join(tmp_output_dir, 'test.nii.gz'),
                                                          True)
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GENERIC_COMPRESSED)[1]) == True

        finally:
            shutil.rmtree(tmp_output_dir)

    def test_are_imaging_dicoms(self):
        assert convert_dicom.are_imaging_dicoms(read_dicom_directory(test_data.SIEMENS_ANATOMICAL))

    def test_get_vendor(self):
        assert convert_dicom._get_vendor(
            read_dicom_directory(test_data.SIEMENS_ANATOMICAL)) == convert_dicom.Vendor.SIEMENS
        assert convert_dicom._get_vendor(read_dicom_directory(test_data.GE_ANATOMICAL)) == convert_dicom.Vendor.GE
        assert convert_dicom._get_vendor(
            read_dicom_directory(test_data.PHILIPS_ANATOMICAL)) == convert_dicom.Vendor.PHILIPS
        assert convert_dicom._get_vendor(
            read_dicom_directory(test_data.PHILIPS_ENHANCED_ANATOMICAL)) == convert_dicom.Vendor.PHILIPS
        assert convert_dicom._get_vendor(
            read_dicom_directory(test_data.GENERIC_ANATOMICAL)) == convert_dicom.Vendor.GENERIC

    def test_is_compressed(self):
        assert convert_dicom.is_compressed(test_data.GENERIC_COMPRESSED) == True
        assert convert_dicom.is_compressed(test_data.GENERIC_ANATOMICAL) == False

    def test_decompress_file(self):
        temporary_directory = tempfile.mkdtemp()
        try:
            dicom_file = os.path.join(temporary_directory, 'IM-0001-0001-0001.dcm')
            input_file = os.path.join(test_data.GENERIC_COMPRESSED, 'IM-0001-0001-0001.dcm')
            shutil.copy(input_file, dicom_file)
            convert_dicom.decompress_dicom(dicom_file)
            assert os.path.isfile(dicom_file)
        finally:
            shutil.rmtree(temporary_directory)

    def test_decompress_directory(self):
        temporary_directory = tempfile.mkdtemp()
        try:
            shutil.rmtree(temporary_directory)
            shutil.copytree(test_data.GENERIC_COMPRESSED, temporary_directory)
            convert_dicom.decompress_directory(temporary_directory)
            assert _count_files(test_data.GENERIC_COMPRESSED) == _count_files(temporary_directory)
        finally:
            shutil.rmtree(temporary_directory)

    def test_compress_file(self):
        temporary_directory = tempfile.mkdtemp()
        try:
            dicom_file = os.path.join(temporary_directory, 'IM-0001-0001-0001.dcm')
            input_file = os.path.join(test_data.GENERIC_ANATOMICAL, 'IM-0001-0001-0001.dcm')
            shutil.copy(input_file, dicom_file)
            convert_dicom.compress_dicom(dicom_file)
            assert os.path.isfile(dicom_file)
        finally:
            shutil.rmtree(temporary_directory)

    def test_compress_directory(self):
        temporary_directory = tempfile.mkdtemp()
        try:
            shutil.rmtree(temporary_directory)
            shutil.copytree(test_data.GENERIC_ANATOMICAL, temporary_directory)
            convert_dicom.compress_directory(temporary_directory)
            assert _count_files(test_data.GENERIC_ANATOMICAL) == _count_files(temporary_directory)
        finally:
            shutil.rmtree(temporary_directory)


def _count_files(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(name)])


if __name__ == '__main__':
    unittest.main()
