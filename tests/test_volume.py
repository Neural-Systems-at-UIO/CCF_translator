import unittest
import numpy as np
import json
import os
from CCF_translator import volume


class TestVolume(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")

    def load_test_case(self, filename):
        with open(os.path.join(self.test_data_dir, filename), "r") as file:
            return json.load(file)

    def test_transform(self):
        test_case = self.load_test_case("test_case_1.json")

        expected_output = test_case["expected_output"]

        vol = volume(
            np.array(input_data["values"]),
            input_data["space"],
            input_data["voxel_size_micron"],
            input_data["age_PND"],
            input_data["segmentation_file"],
        )

        vol.transform(
            input_data["target_age"],
            input_data["target_space"],
            input_data["rescale_output"],
        )

        np.testing.assert_array_almost_equal(
            vol.values, np.array(expected_output["values"])
        )
        self.assertEqual(vol.age_PND, expected_output["age_PND"])
        self.assertEqual(vol.space, expected_output["space"])


if __name__ == "__main__":
    unittest.main()
