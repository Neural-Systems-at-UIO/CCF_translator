class volume:
    def __init__(self, data, space, voxel_size_um, age_PND, segmentation_file=False):
        self.values = data
        self.space = space
        self.voxel_size_um = voxel_size_um
        self.current_age = age_PND
        self.original_age = age_PND
        self.segmentation_file = segmentation_file
        pass

    def translate(self, target_age):
        self.current_age = target_age
        pass
