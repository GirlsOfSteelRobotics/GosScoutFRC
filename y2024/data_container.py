import pandas as pd
import os

from y2024.settings import EVENT
from utils.tba_utils import load_event_matches
from utils.statbotics_utils import load_statbotics_matches, load_statbotics_teams


class DataContainer:
    """
    This is a utility class that loads all of our data of interest.

    It contains:
        scouted_data       : A dataframe containing our scouted information
        statbotics_matches : A dataframe from the statbotics API that contains information on all the matches at the current event,
                             regardless of if they have been run yet
        statbotics_teams   : A dataframe from the statbotics API that contains information on all the teams at the current event,
                             including their EPA information
        tba_matches        : A dataframe from the Blue Alliance API that contains information on all the matches at the current event,
                             regardless of if they have been run yet. This includes the detailed scoring breakdown for a match if it has been completed
    """

    def __init__(self, event):
        self.event = event

        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_directory = os.path.join(this_dir, "data")

        # Load the GOS scouted data
        self.scouted_data = self.__load_gos_data()

        # Load the statbotics matches json
        statbotics_file = os.path.join(
            self.data_directory, f"{self.event}_statbotics_matches.json"
        )
        self.statbotics_matches = load_statbotics_matches(statbotics_file)

        # Load the statbotics team info json
        statbotics_file = os.path.join(
            self.data_directory, f"{self.event}_statbotics_teams.json"
        )
        self.statbotics_teams = load_statbotics_teams(statbotics_file)

        # Load the TBA json
        tba_file = os.path.join(self.data_directory, f"{self.event}_tba_matches.json")
        self.tba_matches = load_event_matches(tba_file)

        # Precalculate the team numbers for this event. We use statbotics as our source of truth.
        self.team_numbers = sorted(
            pd.unique(
                pd.concat(
                    [
                        self.statbotics_matches["red_1"],
                        self.statbotics_matches["red_2"],
                        self.statbotics_matches["red_3"],
                        self.statbotics_matches["blue_1"],
                        self.statbotics_matches["blue_2"],
                        self.statbotics_matches["blue_3"],
                    ]
                )
            )
        )

        # Precalculate the match numbers for this event. We use statbotics as our source of truth.
        self.match_numbers = pd.unique(self.statbotics_matches.match_number)

    def __load_gos_data(self) -> pd.DataFrame:
        """
        Loads the scouted data from our CSV file
        :return: The scouting data, including name re-mappings and precalculated aggregate data
        """

        if self.event == "2024new":
            filename = os.path.join(self.data_directory, f"{self.event}_scouting.csv")
            data_frame = pd.read_csv(filename)
        else:
            filename = os.path.join(self.data_directory, f"{self.event}_scouting.txt")
            data_frame = pd.read_csv(filename, delimiter="\t")

        data_frame = self.__sanitize_gos_field_names(data_frame)
        data_frame = self.__amend_calculated_data(data_frame)

        return data_frame

    def __sanitize_gos_field_names(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        # TODO - Think about renaming some of the fields, especially in Buckeye Data
        return data_frame

    def __amend_calculated_data(self, data_frame):
        # TODO - consider pre-calculating aggregated data, like "Total Notes"
        return data_frame


"""
Singleton instantiation of the data container. You should treat this as an immutable object
"""
data_container = DataContainer(EVENT)
