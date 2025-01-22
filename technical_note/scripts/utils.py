from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from VSM.WingGeometry import Wing
from VSM.WingAerodynamics import WingAerodynamics

PROJECT_DIR = Path(__file__).resolve().parents[1]


def create_wing_aero(
    file_path,
    n_panels,
    spanwise_panel_distribution,
    is_with_corrected_polar=False,
    path_polar_data_dir="",
):
    df = pd.read_csv(file_path, delimiter=",")  # , skiprows=1)
    LE_x_array = df["LE_x"].values
    LE_y_array = df["LE_y"].values
    LE_z_array = df["LE_z"].values
    TE_x_array = df["TE_x"].values
    TE_y_array = df["TE_y"].values
    TE_z_array = df["TE_z"].values
    d_tube_array = df["d_tube"].values
    camber_array = df["camber"].values

    ## populating this list
    rib_list_from_CAD_LE_TE_and_surfplan_d_tube_camber_19ribs = []

    for i in range(len(LE_x_array)):
        LE = np.array([LE_x_array[i], LE_y_array[i], LE_z_array[i]])
        TE = np.array([TE_x_array[i], TE_y_array[i], TE_z_array[i]])
        rib_list_from_CAD_LE_TE_and_surfplan_d_tube_camber_19ribs.append(
            [LE, TE, ["lei_airfoil_breukels", [d_tube_array[i], camber_array[i]]]]
        )
    CAD_wing = Wing(n_panels, spanwise_panel_distribution)

    for i, CAD_rib_i in enumerate(
        rib_list_from_CAD_LE_TE_and_surfplan_d_tube_camber_19ribs
    ):
        CAD_rib_i_0 = CAD_rib_i[0]
        CAD_rib_i_1 = CAD_rib_i[1]

        if is_with_corrected_polar:
            ### using corrected polar
            df_polar_data = pd.read_csv(
                Path(path_polar_data_dir) / f"corrected_polar_{i}.csv"
            )
            alpha = df_polar_data["alpha"].values
            cl = df_polar_data["cl"].values
            cd = df_polar_data["cd"].values
            cm = df_polar_data["cm"].values
            polar_data = ["polar_data", np.array([alpha, cl, cd, cm])]
            CAD_wing.add_section(CAD_rib_i_0, CAD_rib_i_1, polar_data)

        else:
            ### using breukels
            CAD_wing.add_section(CAD_rib_i_0, CAD_rib_i_1, CAD_rib_i[2])

    wing_aero = WingAerodynamics([CAD_wing])

    return wing_aero


def saving_pdf_and_pdf_tex(results_dir: str, filename: str):
    plt.savefig(Path(results_dir) / f"{filename}.pdf")
    plt.close()


x_axis_labels = {
    "alpha": r"$\alpha$ [$^\circ$]",
    "beta": r"$\beta$ [$^\circ$]",
    "Re": r"Re $\times 10^5$ [-]",
    "y/b": r"$y/b$ [-]",
}

y_axis_labels = {
    "CL": r"$C_{\mathrm{L}}$ [-]",
    "CD": r"$C_{\mathrm{D}}$ [-]",
    "CS": r"$C_{\mathrm{S}}$ [-]",
    "CMx": r"$C_{\mathrm{M,x}}$ [-]",
    "CMy": r"$C_{\mathrm{M,y}}$ [-]",
    "CMz": r"$C_{\mathrm{M,z}}$ [-]",
    "L/D": r"$L/D$ [-]",
    "kcrit": r"$k_{\mathrm{crit}}$ [mm]",
    "gamma": r"$\Gamma$ [m$^2$s$^{-1}$]",
}
