import os
import sys
sys.path.append(os.path.abspath("/home/harryc/github/CCF_translator/"))

import unittest
import nibabel as nib
import numpy as np
import json
from CCF_translator import VolumeSeries, Volume

class TestVolumeSeries(unittest.TestCase):
    def setUp(self):
        self.test_case_dir = os.path.join(os.path.dirname(__file__), 'VolumeSeries_test_cases')
        self.voxel_size_micron = 20
        self.space_name = "demba_dev_mouse"
        self.data_folder = "/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v1/interpolated_templates/"

    def load_test_case(self, filename):
        with open(os.path.join(self.test_case_dir, filename), 'r') as file:
            return json.load(file)

    def run_test_case(self, test_case_filename):
        test_case = self.load_test_case(test_case_filename)
        key_ages = test_case['key_ages']
        expected_output_dir = test_case['expected_output_dir']

        volumes = []
        for age in key_ages:
            volume_path = os.path.join(self.data_folder, f"DeMBA_P{age}_brain.nii.gz")
            try:
                volume_data = nib.load(volume_path).get_fdata()
            except FileNotFoundError:
                print(f"File not found: {volume_path}")
                continue
            volume = Volume(
                values=volume_data,
                space=self.space_name,
                voxel_size_micron=self.voxel_size_micron,
                segmentation_file=False,
                age_PND=age,
            )
            volumes.append(volume)

        volume_series = VolumeSeries(volumes)
        volume_series.interpolate_series()
        volume_series.save(output_dir="demo_data/demba_volumes/")

        # Compare the output directory with the expected output directory
        for file_name in os.listdir(expected_output_dir):
            expected_file_path = os.path.join(expected_output_dir, file_name)
            output_file_path = os.path.join("demo_data/demba_volumes/", file_name)
            expected_data = nib.load(expected_file_path).get_fdata()
            output_data = nib.load(output_file_path).get_fdata()
            np.testing.assert_array_almost_equal(output_data, expected_data)

# List of test case filenames
test_case_files = [
    'test_case_1.json',
    'test_case_2.json',
    'test_case_3.json',
]

# Dynamically create test methods for each test case file
for test_case_file in test_case_files:
    def test_method(self, test_case_file=test_case_file):
        self.run_test_case(test_case_file)
    setattr(TestVolumeSeries, f'test_{test_case_file.split(".")[0]}', test_method)

if __name__ == '__main__':
    unittest.main()