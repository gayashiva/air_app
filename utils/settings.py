
"""Location specific settings used to initialise icestupa object
"""

# External modules
import pandas as pd
from datetime import datetime
import logging
import os, sys
import numpy as np

# Spammers
logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
logging.getLogger("numexpr").setLevel(logging.CRITICAL)

dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(dirname)


def config(location="guttannen21", spray="man"):

    if location == "Guttannen 2022" or location == "guttannen22":

        SITE = dict(
            name="guttannen22",
            alt=1047.6,
            coords=[46.65549,8.29149],
            # Calibrated values
            DX=45e-03,  # Surface layer thickness [m]
        )

        if spray == "auto":
            auto= dict(
                start_date=datetime(2021, 12, 3, 8),
                expiry_date=datetime(2022, 1, 27),
                fountain_off_date=datetime(2022, 1, 27),
                h_i = 0.13, #Initialise ice height at start
            # perimeter=35, # on Jan 28
            )

            SITE = dict(SITE, **auto)
            f_heights = [
                {"time": SITE["start_date"], "h_f": 3},
                {"time": datetime(2022, 12, 23, 16), "h_f": 4},
            ]

        if spray == "man":
            man = dict(
                start_date=datetime(2021, 12, 8, 14),
                expiry_date=datetime(2022, 1, 27),
                fountain_off_date=datetime(2022, 1, 27),
                alt=1047.6,
                coords=[46.65549,8.29149],
                #TODO correct snow height
                h_i = 0.13, #Initialise ice height at start
            )

            SITE = dict(SITE, **man)
            f_heights = [
                {"time": SITE["start_date"], "h_f": 3.7},
                {"time": datetime(2022, 12, 23, 16), "h_f": 4.7},
                {"time": datetime(2022, 2, 12, 16), "h_f": 5.7},
            ]

    if location == "Guttannen 2021" or location == "guttannen21":

        SITE = dict(
            name="guttannen21",
            start_date=datetime(2020, 11, 22, 15),
            # end_date=datetime(2021, 5, 10, 1),
            expiry_date=datetime(2021, 5, 10, 1),
            fountain_off_date=datetime(2021, 2, 20, 10),
            D_F=7.5,  # Fountain mean discharge
            # R_F=4.3,  # Fountain mean discharge
            # R_F=5.4,  # First drone rad
            alt=1047.6,
            coords=[46.65549,8.29149],
            # h_f=5,
            # perimeter=45, # on Feb 11

            # Calibrated values
            DX=45e-03,  # Surface layer thickness [m]
        )

        f_heights = [
            {"time": SITE["start_date"], "h_f": 2.68},
            {"time": datetime(2020, 12, 30, 16), "h_f": 3.75},
            {"time": datetime(2021, 1, 7, 16), "h_f": 4.68},
            {"time": datetime(2021, 1, 11, 16), "h_f": 5.68},
        ]

    if location == "Guttannen 2020" or location == "guttannen20":

        SITE = dict(
            name="guttannen20",
            start_date=datetime(2020, 1, 3, 16),
            # end_date=datetime(2020, 4, 6, 12),
            expiry_date=datetime(2020, 4, 6, 12),
            fountain_off_date=datetime(2020, 3, 8, 9),  # Image shows Dani switched off at 8th Mar 10 am
            D_F=7.5,  # Fountain mean discharge
            # R_F=6.68,  # First drone rad
            alt=1047.6,
            coords=[46.65549,8.29149],
            # h_f=3,
            # perimeter=28, # on 24 Jan

            # Calibrated values
            DX=45e-03,  # Surface layer thickness [m]
        )

        f_heights = [
            {"time": SITE["start_date"], "h_f": 2.5},
            {"time": datetime(2020, 1, 24, 12), "h_f": 3.5},
            {"time": datetime(2020, 2, 5, 19), "h_f": 2.5},
        ]

    if location == "Gangles 2021" or location == "gangles21":

        SITE = dict(
            name="gangles21",
            start_date=datetime(2021, 1, 18),
            # end_date=datetime(2021, 7, 8),
            expiry_date=datetime(2021, 6, 20),
            fountain_off_date=datetime(2021, 3, 10, 18),
            D_F=60,  # FOUNTAIN min discharge
            # R_F=9.05,  # First drone rad
            alt=4009,
            coords=[34.216638,77.606949],
            h_f=9,
            tcc=0,  # Total cloud cover
            # tcc=0.1,  # Total cloud cover
            # perimeter=82.3, # On 3 Mar

            # Calibrated values
            DX=65e-03,  # Surface layer thickness [m]
        )

        f_heights = [
            {"time": SITE["start_date"], "h_f": 5},
            {"time": datetime(2021, 1, 22, 16), "h_f": 9},
        ]

    # Define directory structure
    FOLDER = dict(
        raw="data/" + SITE["name"] + "/raw/",
        input="data/" + SITE["name"] + "/interim/",
        output="data/" + SITE["name"] + "/processed/",
        output_auto="data/" + SITE["name"] + "/processed/auto/",
        output_man="data/" + SITE["name"] + "/processed/man/",
        sim="data/" + SITE["name"] + "/processed/simulations/",
        fig="data/" + SITE["name"] + "/figs/",
    )
    df_h = pd.DataFrame(f_heights)

    """Model, Physical and Surface Constants"""
    CONSTANTS = dict(
        DT=60 * 60,  # Model time step [s]
        H_AWS=2,  # AWS height [m]

        VAN_KARMAN=0.4,  # Van Karman constant
        sigma=5.67e-8,  # Stefan-Bolzmann constant [W m-2 K-4]
        P0=1013,  # Standard air pressure hPa
        RHO_S=300,  # Density of snow
        RHO_W=1000,  # Density of water
        RHO_I=917,  # Density of Ice RHO_I
        RHO_A=1.29,  # air density at mean sea level
        C_W=4186,  # specific heat of water [J Kg-1 K-1]
        C_I=2097,  # specific heat of ice [J Kg-1 K-1]
        C_A=1010,  # specific heat of air [J kg-1 K-1]
        L_F=3.34e5,  # latent heat for melting [J kg-1]
        L_V=2.5e6,  # latent heat for vaporization [J kg-1]
        L_S=2.848e6,  # latent heat for sublimation [J kg-1]
        K_I=2.123,  # thermal conductivity ice [W m^-1 K^-1] Waite et al. 2006
        G=9.81,  # Gravitational acceleration


        # Weather uncertainty
        IE=0.97,  # Ice Emissivity IE
        Z=0.003,  # Ice Momentum and Scalar roughness length
        A_I=0.25,  # Albedo of Ice A_I
        A_S=0.85,  # Albedo of Fresh Snow A_S
        T_PPT=1,  # Temperature condition for liquid precipitation
        A_DECAY=16,  # Albedo decay rate decay_t_d

        # Fountain uncertainty
        T_F=1.5,  # Fountain temp

        # Fix these first with calibration step
        DX=50e-03,  # Surface layer thickness [m]
    )

    return CONSTANTS, SITE, FOLDER
