import os

os.chdir("..")
import numpy as np
from CCF_translator.deformation import apply_deformation, route_calculation
import CCF_translator
import pandas as pd
from tqdm import tqdm

key_ages = [56, 28, 21, 14, 7, 4]
points_dataset_h = pd.read_excel(r"demo_data/DeMBA_landmarksValidation_Heidi.xlsx")
points_dataset_i = pd.read_excel(r"demo_data/DeMBA_landmarksValidation_Ingvild.xlsx")


target_space = "demba_dev_mouse"

col_format = "{}: {} ({} sections)"
for m in ["iterative", "individual"]:
    mean_older_points = None
    for i in tqdm(range(len(key_ages) - 1)):
        older_age = key_ages[i]
        if older_age == 56:
            name_older_age = "adult"
        else:
            name_older_age = f"P{str(older_age).zfill(2)}"

        younger_age = key_ages[i + 1]
        name_younger_age = f"P{str(younger_age).zfill(2)}"
        older_points_heidi = points_dataset_h[
            [
                col_format.format(name_older_age, "x", "sagittal"),
                col_format.format(name_older_age, "y", "horizontal"),
                col_format.format(name_older_age, "z", "coronal"),
            ]
        ].values
        younger_points_heidi = points_dataset_h[
            [
                col_format.format(name_younger_age, "x", "sagittal"),
                col_format.format(name_younger_age, "y", "horizontal"),
                col_format.format(name_younger_age, "z", "coronal"),
            ]
        ].values
        older_points_ingvild = points_dataset_i[
            [
                col_format.format(name_older_age, "x", "sagittal"),
                col_format.format(name_older_age, "y", "horizontal"),
                col_format.format(name_older_age, "z", "coronal"),
            ]
        ].values
        younger_points_ingvild = points_dataset_i[
            [
                col_format.format(name_younger_age, "x", "sagittal"),
                col_format.format(name_younger_age, "y", "horizontal"),
                col_format.format(name_younger_age, "z", "coronal"),
            ]
        ].values
        if mean_older_points is None or m == "individual":
            mean_older_points = np.mean(
                [older_points_ingvild, older_points_heidi], axis=0
            )
        points = CCF_translator.PointSet(
            values=mean_older_points,
            space=target_space,
            age_PND=older_age,
            voxel_size_micron=20,
        )
        points.transform(target_age=younger_age, target_space=target_space)

        i2h = []
        h2d = []
        i2d = []
        d2a = []
        hx = []
        hy = []
        hz = []
        ix = []
        iy = []
        iz = []
        dx = []
        dy = []
        dz = []
        new_mean_older_points = []
        for i in range(len(mean_older_points)):
            if np.isnan(mean_older_points[i]).any():
                new_mean_older_points.append([np.nan, np.nan, np.nan])
                i2h.append(np.nan)
                h2d.append(np.nan)
                i2d.append(np.nan)
                hx.append(np.nan)
                hy.append(np.nan)
                hz.append(np.nan)
                ix.append(np.nan)
                iy.append(np.nan)
                iz.append(np.nan)
                dx.append(np.nan)
                dy.append(np.nan)
                dz.append(np.nan)
                continue
            pred_point = points.values[i]
            new_mean_older_points.append(pred_point)
            heidi_point = younger_points_heidi[i]
            ingvild_point = younger_points_ingvild[i]
            h_i_dist = abs(np.linalg.norm(heidi_point - ingvild_point))
            d_i_dist = abs(np.linalg.norm(pred_point - ingvild_point))
            d_h_dist = abs(np.linalg.norm(pred_point - heidi_point))
            # d_a_dist =  abs(np.linalg.norm(pred_point - np.mean([heidi_point, ingvild_point], axis=0)))
            i2h.append(h_i_dist)
            h2d.append(d_h_dist)
            i2d.append(d_i_dist)
            hx.append(heidi_point[0])
            hy.append(heidi_point[1])
            hz.append(heidi_point[2])
            ix.append(ingvild_point[0])
            iy.append(ingvild_point[1])
            iz.append(ingvild_point[2])
            dx.append(pred_point[0])
            dy.append(pred_point[1])
            dz.append(pred_point[2])
            # d2a.append(d_a_dist)
        output_data = {
            "Acronym": points_dataset_h["Acronym"],
            "Full Name": points_dataset_h["Full name"],
            "Distance Ingvild to Heidi": i2h,
            "Distance Ingvild to Demba": i2d,
            "Distance Heidi to Demba": h2d,
            "Heidi x": hx,
            "Heidi y": hy,
            "Heidi z": hz,
            "Ingvild x": ix,
            "Ingvild y": iy,
            "Ingvild z": iz,
            "Demba x": dx,
            "Demba y": dy,
            "Demba z": dz,
        }
        pd.DataFrame(output_data).to_csv(f"demo_data/{m}_{name_younger_age}.csv")
        mean_older_points = np.array(new_mean_older_points)

        print(f"ingvild to heidi median: {np.nanmedian(i2h)}")
        print(f"ingvild to demba median: {np.nanmedian(i2d)}")
        print(f"heidi to demba median: {np.nanmedian(h2d)}")
        print(f"demba to average median: {np.nanmedian(d2a)}")
