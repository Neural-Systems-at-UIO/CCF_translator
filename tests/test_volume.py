import unittest
import numpy as np
import json
import os
from CCF_translator import volume
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas



class TestVolume(unittest.TestCase):
    def setUp(self):
        self.test_case_dir = os.path.join(os.path.dirname(__file__), '..', 'volume_test_cases')

    def load_test_case(self, filename):
        with open(os.path.join(self.test_case_dir, filename), 'r') as file:
            return json.load(file)

    def test_transform(self):
        test_case = self.load_test_case('allen_to_demba_P56.json')
        input_data_path = test_case['input']
        expected_output_path = test_case['expected_output']
        input_data = np.load(input_data_path)
        vol = volume(
            input_data,
            input_data['space'],
            input_data['voxel_size_micron'],
            input_data['age_PND'],
            input_data['segmentation_file']
        )

        vol.transform(
            input_data['target_age'],
            input_data['target_space'],
        )

        np.testing.assert_array_almost_equal(vol.values, np.array(expected_output['values']))
        self.assertEqual(vol.age_PND, expected_output['age_PND'])
        self.assertEqual(vol.space, expected_output['space'])

if __name__ == '__main__':
    unittest.main()