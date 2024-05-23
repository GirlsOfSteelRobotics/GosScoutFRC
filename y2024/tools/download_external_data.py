import os

from utils.statbotics_utils import (
    download_statbotics_matches,
    download_statbotics_event_teams,
)
from utils.tba_utils import download_tba_event_matches
from y2024.settings import EVENT


def download_external_data(event):
    """
    Downloads the external data (Statbotics, TBA, etc) for a specific event
    :param event: The event key
    """
    script_directory = os.path.dirname(os.path.realpath(__file__))

    data_directory = os.path.join(script_directory, "..", "data")

    statbotics_matches_file = os.path.join(
        data_directory, f"{event}_statbotics_matches.json"
    )
    download_statbotics_matches(event, statbotics_matches_file)

    statbotics_teams_file = os.path.join(
        data_directory, f"{event}_statbotics_teams.json"
    )
    download_statbotics_event_teams(event, statbotics_teams_file)

    tba_matches_file = os.path.join(data_directory, f"{event}_tba_matches.json")
    download_tba_event_matches(event, tba_matches_file)


if __name__ == "__main__":
    download_external_data(EVENT)
