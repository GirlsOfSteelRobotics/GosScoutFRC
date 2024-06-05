from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
from utils.statbotics_utils import get_red_teams_in_match
from y2024.data_container import data_container
import plotly.express as px


app_ui = ui.page_fluid(
    ui.navset_pill(
        ui.nav_panel("Pit Scouting Data", "Panel A content"),
        ui.nav_panel(
            "Match Data",
            ui.page_fluid(
                ui.card(
                    ui.card_header("red melody contribution"),
                    output_widget("melody_plot"),
                ),
                ui.card(
                    ui.card_header("red harmony contribution"),
                    output_widget("harmony_plot"),
                ),
            ),
        ),
        ui.nav_panel("Team Data", "Panel C content"),
        ui.nav_panel(
            "Averages",
            ui.page_fluid(
                ui.card(
                    ui.card_header("Team Averages"), ui.output_data_frame("avgs_df")
                )
            ),
        ),
    )
)


def server(input, output, session):
    @render.data_frame
    def avgs_df():
        all_averages = data_container.scouted_data.groupby("Team_Number").mean(
            numeric_only=True
        )
        all_averages = all_averages.reset_index()
        return render.DataGrid(all_averages, filters=True)

    @render_widget
    def melody_plot():
        plot = px.bar(
            red(),
            x="team num fr",
            y=[
                "tele_speaker_scored",
                "tele_amp_scored",
                "auto_speaker_scored",
                "auto_amp_Scored",
            ],
            title="red melody contribution",
            labels={"value": "notes", "team num fr": "team number"},
        )
        return plot

    def red():
        match_num = 6
        all_averages = (
            data_container.scouted_data.groupby("Team_Number")
            .mean(numeric_only=True)
            .reset_index()
        )

        statbotics_match = data_container.statbotics_matches[
            data_container.statbotics_matches["match_number"] == match_num
        ]
        red_teams = get_red_teams_in_match(statbotics_match)
        red_data = all_averages[all_averages["Team_Number"].isin(red_teams)]
        red_data.insert(1, "index", [1, 2, 3])
        red_data.insert(
            2, "team num fr", [str(red_teams[0]), str(red_teams[1]), str(red_teams[2])]
        )
        return red_data

    @render_widget
    def harmony_plot():
        red_data = red()
        plot = px.scatter(
            red_data,
            x="total notes",
            y="scouted score",
            text=red_data["Team_Number"],
            hover_name=red_data["Team_Number"],
        )
        return plot


app = App(app_ui, server)
