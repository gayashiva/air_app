"""Streamlit web app to display Icestupa class object
"""

# External modules
import streamlit as st
import pandas as pd
import sys, os, math, json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from utils.metadata import get_parameter_metadata
from utils.settings import config


# SETTING PAGE CONFIG TO WIDE MODE
air_logo = "logos/AIR_logo_circle.png"
st.set_page_config(
    layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
    page_title="Icestupa",  # String or None. Strings get appended with "• Streamlit".
    page_icon=air_logo,  # String, anything supported by st.image, or None.
)

# github_url = "https://github.com/gayashiva/air_model/tree/master/"


@st.cache
def vars(df):
    input_cols = []
    input_vars = []
    output_cols = []
    output_vars = []
    derived_cols = []
    derived_vars = []
    for variable in df.columns:
        v = get_parameter_metadata(variable)
        if v["kind"] == "Input":
            input_cols.append(v["name"])
            input_vars.append(variable)
        if v["kind"] == "Output":
            output_cols.append(v["name"])
            output_vars.append(variable)
        if v["kind"] == "Derived":
            derived_cols.append(v["name"])
            derived_vars.append(variable)
    return input_cols, input_vars, output_cols, output_vars, derived_cols, derived_vars


if __name__ == "__main__":
    # Main logger
    logger = logging.getLogger(__name__)
    logger.setLevel("WARNING")

    st.sidebar.markdown(
        """
    # Select Ice Reservoir

    """
    )

    location = st.sidebar.radio(
        " ",
        # ("gangles21", "guttannen21", "guttannen20", "guttannen22"),
        ( "Home",  "Guttannen 2020", "Guttannen 2021", "Guttannen 2022","Gangles 2021"),
    )

    if location == "Home":
        row1_1, row1_2 = st.columns((2, 5))
        with row1_1:
            st.image(air_logo, width=160)

        with row1_2:
            st.markdown(
                """
            # Artificial Ice Reservoirs
            ***_A sustainable water storage technology for mountain communities_***
                """
                    )
        st.markdown(
                """

##### This app showcases the results from a [publication](https://www.frontiersin.org/articles/10.3389/feart.2021.771342/full) that evaluated fountain efficiency and meltwater quantities of icestupas in India and Switzerland. 

##### Start by selecting an icestupa from the left. Tables and plots will display a summary of the results for the selected Icestupa.

##### Some Icestupas also have a *timelapse* video that shows the daily variation in ice volumes seen at the respective site.

##### 💻 The code is available freely at [github](https://github.com/Gayashiva/air_model).

##### Summary of the research results can also be viewed in the video below:

        """
        )
        url = "https://youtu.be/WwnfSO3gJBo"
        st.video(url)

    else:

        loc_dict ={
                "Gangles 2021": "gangles21",
                "Guttannen 2020": "guttannen20",
                "Guttannen 2021": "guttannen21",
                "Guttannen 2022": "guttannen22",
            }
        location = loc_dict[location]

        spray = "man"
        # if location == "guttannen22":
        #     spray = "auto"

        CONSTANTS, SITE, FOLDER = config(location)

        df = pd.read_hdf("data/" + location + "/processed/" + spray + "/output.h5", "df")

        (
            input_cols,
            input_vars,
            output_cols,
            output_vars,
            derived_cols,
            derived_vars,
        ) = vars(df)

        row1_1, row1_2 = st.columns((2, 5))

        with row1_1:
            st.image(air_logo, width=160)

        with row1_2:
            st.markdown(
                """
            # **_%s_** Icestupa

            """
                % get_parameter_metadata(location)["name"].split()[0]
            )
            visualize = [
                "Timelapse",
                "Validation",
                "Data Overview",
                "Input",
                "Output",
                "Derived",
            ]
            display = st.multiselect(
                "Choose type of web below:",
                options=(visualize),
                # default=["Validation"],
                default=["Validation", "Timelapse"],
            )
            intro_markdown = Path("utils/intro.md").read_text()
            st.markdown(intro_markdown, unsafe_allow_html=True)

        st.markdown("---")
        st.sidebar.write("### Map")
        lat = SITE["coords"][0]
        lon = SITE["coords"][1]
        map_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
        st.sidebar.map(map_data, zoom=10)


        st.sidebar.write(
            """
            ### Partners
            """
        )
        row2_1, row2_2, row2_3 = st.sidebar.columns((1, 1, 1))
        row3_1, row3_2 = st.columns((1, 1))
        with row2_1:
            st.image(
                "logos/unifr.png",
                caption="UniFR",
                use_column_width=True,
            )
            st.markdown(" ")
            st.image(
                "logos/GA.png",
                caption="GlaciersAlive",
                use_column_width=True,
            )
            st.markdown(" ")
            st.image(
                "logos/ng-logo.png",
                # caption="GlaciersAlive",
                use_column_width=True,
            )
        with row2_2:
            st.image(
                "logos/HIAL-logo.png",
                caption="HIAL",
                use_column_width=True,
            )
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.image(
                "logos/logo-schwarzsee.png",
                caption="Schwarzsee Tourism",
                use_column_width=True,
            )
            st.markdown(" ")
            st.markdown(" ")
            st.image(
                "logos/dfrobot.png",
                # caption="GlaciersAlive",
                use_column_width=True,
            )
        with row2_3:
            st.image(
                "logos/guttannen-bewegt.png",
                caption="Guttannen Moves",
                use_column_width=True,
            )
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.image(
                "logos/Logo-Swiss-Polar-Institute.png",
                use_column_width=True,
            )
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.image(
                "logos/hochschule-luzern.jpg",
                # caption="GlaciersAlive",
                use_column_width=True,
            )

        st.sidebar.write(
            """
        ###
        [![Follow](https://img.shields.io/twitter/follow/know_just_ice?style=social)](https://www.twitter.com/know_just_ice)
        """
        )

        with row3_1:

            with open("data/" + location + "/processed/" + spray + "/results.json", "r") as read_file:
                results_dict = json.load(read_file)

            mean_freeze_rate = df[
                df.Discharge != 0
            ].fountain_froze.mean() / (CONSTANTS["DT"] / 60)
            fountain_duration = df[df.Discharge != 0].shape[0]
            mean_melt_rate = df.melted.mean() / (CONSTANTS["DT"] / 60)
            st.markdown(
                """
            | Fountain | Estimation |
            | --- | --- |
            | Spray Radius | %.1f $m$|
            | Water sprayed| %i $m^3$ |
            | Mean discharge rate | %i $l/min$ |
            | Mean freeze rate | %.1f $l/min$ |
            | Mean melt rate | %.1f $l/min$ |
            | Runtime | %s $hours$ |
            """
                % (
                    results_dict["R_F"],
                    results_dict["M_F"] / 1000,
                    results_dict["D_F"],
                    mean_freeze_rate,
                    mean_melt_rate,
                    fountain_duration,
                )
            )

        with row3_2:

            st.markdown(
                """
            | Icestupa| Estimation |
            | --- | --- |
            | Max Ice Volume | %i $m^{3}$|
            | Meltwater released | %i $tons$ |
            | Vapour loss | %i $tons$ |
            | Water Use Efficiency | %i $percent$ |
            | Melt-out date | %s |
            """
                % (
                    df["iceV"].max(),
                    results_dict["M_water"] / 1000,
                    results_dict["M_sub"] / 1000,
                    results_dict["WUE"],
                    SITE["expiry_date"].strftime("%b %d"),
                )
            )

        st.markdown("---")
        if not (display):
            st.error("Please select at least one option.")
        else:
            if "Validation" in display:

                st.write("## Validation")
                path = "data/" + location + "/figs/" + spray + "/Vol_Validation.png"
                st.image(path)

            if "Timelapse" in display:
                st.write("## Timelapse")
                if location == "schwarzsee19":
                    url = "https://youtu.be/GhljRBGpxMg"
                    st.video(url)
                elif location == "guttannen21":
                    url = "https://www.youtube.com/watch?v=kXi4abO4YVM"
                    st.video(url)
                elif location == "guttannen20":
                    url = "https://youtu.be/kcrvhU20OOE"
                    st.video(url)
                elif location == "gangles21":
                    st.error("No Timelapse recorded")
                elif location == "guttannen22":
                    st.error("No Timelapse recorded")

            if "Data Overview" in display:
                st.write("## Input variables")
                st.image("data/" + location + "/figs/Model_Input.png")
                st.write(
                    """
                Measurements at the AWS of %s were used as main model input
                data in 15 minute frequency.  Incoming shortwave and longwave radiation
                were obtained from ERA5 reanalysis dataset. Several data gaps
                and errors were also filled from the ERA5 dataset (shaded regions).  
                """
                    % (location)
                )
                st.write("## Output variables")
                st.image("data/" + location + "/figs/Model_Output.png")
                st.write(
                    """
                (a) Fountain discharge (b) energy flux components, (c) mass flux components (d)
                surface area and (e) volume of the Icestupa in daily time steps. qSW is the net
                shortwave radiation; qLW is the net longwave radiation; qL and qS are the
                turbulent latent and sensible heat fluxes. qF represents the interactions of
                the ice-water boundary during fountain on time steps. qG quantifies the heat
                conduction process between the Icestupa surface layer and the ice body.
                """
                )

            df = pd.read_hdf(FOLDER["output"] + spray + "/output" + ".h5", "df")

            if "Input" in display:
                st.write("## Input variables")
                variable1 = st.multiselect(
                    "Choose",
                    options=(input_cols),
                    default=["Discharge", "Temperature"],
                    # default=["Temperature"],
                )
                if not (variable1):
                    st.error("Please select at least one variable.")
                else:
                    variable_in = [input_vars[input_cols.index(item)] for item in variable1]
                    variable = variable_in
                    for v in variable:

                        meta = get_parameter_metadata(v)
                        st.header("%s" % (meta["name"] + " " + meta["units"]))
                        row4_1, row4_2 = st.columns((2, 5))
                        with row4_1:
                            st.write(df[v].describe())
                        with row4_2:
                            st.line_chart(df[v], use_container_width=True)

            if "Output" in display:
                st.write("## Output variables")

                variable2 = st.multiselect(
                    "Choose",
                    options=(output_cols),
                    default=["Frozen Discharge"],
                )
                if not (variable2):
                    st.error("Please select at least one variable.")
                else:
                    variable_out = [
                        output_vars[output_cols.index(item)] for item in variable2
                    ]
                    variable = variable_out
                    for v in variable:
                        meta = get_parameter_metadata(v)
                        st.header("%s" % (meta["name"] + " " + meta["units"]))
                        row5_1, row5_2 = st.columns((2, 5))
                        with row5_1:
                            st.write(df[v].describe())
                        with row5_2:
                            st.line_chart(df[v], use_container_width=True)

            if "Derived" in display:
                st.write("## Derived variables")
                variable3 = st.multiselect(
                    "Choose",
                    options=(derived_cols),
                    default=["Solar Surface Area Fraction"],
                )
                if not (variable3):
                    st.error("Please select at least one variable.")

                else:
                    variable_in = [
                        derived_vars[derived_cols.index(item)] for item in variable3
                    ]
                    variable = variable_in
                    for v in variable:
                        meta = get_parameter_metadata(v)
                        st.header("%s" % (meta["name"] + " " + meta["units"]))
                        row6_1, row6_2 = st.columns((2, 5))
                        with row6_1:
                            st.write(df[v].describe())
                        with row6_2:
                            st.line_chart(df[v], use_container_width=True)
