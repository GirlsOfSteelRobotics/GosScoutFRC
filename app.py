from shiny import App, reactive, ui

app_ui = ui.page_fluid(ui.input_text("text", label="Enter some text"))


def server(input):
    @reactive.effect
    def _():
        print(input.text())


app = App(app_ui, server)
