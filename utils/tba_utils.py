import json
from pathlib import Path
import os

import pandas as pd
import requests
from typing import Dict, Any


def __get_api_key():
    app_dir = Path(__file__).parent
    api_key_file = os.path.join(app_dir.parent, ".tba_key")

    if not os.path.exists(api_key_file):
        raise FileNotFoundError(
            f"Could not find TBA API key at {api_key_file}. Please create this file and paste your API key. If you do not have an API key, create one at https://www.thebluealliance.com/account/"
        )

    with open(r"C:\Users\PJ\git\frc-utils\GosScouterDash\.tba_key", "r") as f:
        api_key = f.read()

    return api_key


def __make_request(url):
    headers = {"X-TBA-Auth-Key": __get_api_key()}

    response = requests.get(url, headers=headers)

    return response.json()


def request_event_matches(event_key: str) -> Dict[str, Any]:
    url = f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches"
    return __make_request(url)


def download_tba_event_matches(event_key: str, output_file: str):
    json_data = request_event_matches(event_key)

    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=4)


def load_event_matches(json_file: str) -> pd.DataFrame:
    with open(json_file, "r") as f:
        json_data = json.load(f)

    return event_matches_json_to_dataframe(json_data)


def event_matches_json_to_dataframe(json_data: Dict[str, Any]) -> pd.DataFrame:
    raw_df = pd.json_normalize(json_data)

    # Filter out elims matches for our purposes
    raw_df = raw_df[raw_df["comp_level"] == "qm"]

    # We like to be able to simply query teams. By default, they are embedded in the dataframe as a list
    red_teams = raw_df["alliances.red.team_keys"]
    blue_teams = raw_df["alliances.blue.team_keys"]

    # TODO(pj) There is surely a better way
    raw_df["red1"] = [t[0] for t in red_teams]
    raw_df["red2"] = [t[1] for t in red_teams]
    raw_df["red3"] = [t[2] for t in red_teams]
    raw_df["blue1"] = [t[0] for t in blue_teams]
    raw_df["blue2"] = [t[1] for t in blue_teams]
    raw_df["blue3"] = [t[2] for t in blue_teams]

    return raw_df
