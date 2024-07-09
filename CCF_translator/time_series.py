class time_series:
    def __init__(self, volumes):
        self.volumes = volumes
        self.data_ages = [i.age_PND for i in volumes]
        self.data_ages.sort()
