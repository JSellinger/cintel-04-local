#Packaging imports
import plotly.express as px
import seaborn as sb
import palmerpenguins as pp
import shiny
from shiny.express import input, render, ui
from shiny import reactive
from shinywidgets import render_plotly

p_df = pp.load_penguins()

#Adding reactive block for global reactive functions - I am retarded and I hate this
#There are issues with PyShiny and filtering a data frame with more than one filter - need to figure out later
@reactive.calc
def filtered_data():
    if input.radio() == "Yes":
        filtered_df_species = p_df[p_df["species"].isin(input.check())]
        return filtered_df_species
    else:
        filtered_df = p_df
        return filtered_df

#Page options
ui.page_opts(title="Palmer Penguins Exploration", fillable=True)

#Sidebar layout
with ui.sidebar(bg = "#808080"):
    ui.h1("Settings and Selections")
    "You can select settings and interact with the data graphs through this sidebar. The link to the Git repo is below:"
    #Git repo link
    ui.a("Github", href="https://github.com/JSellinger", target="_blank")
    #General Settings Card
    with ui.card():
        ui.card_header("General Settings")
        ui.input_dark_mode()
        ui.input_radio_buttons("radio","Filter Data Frame", ["Yes","No"])
    #Selection Settings for Graphs
    with ui.card():
        ui.card_header("Graph Interaction")
        #Slider
        ui.input_slider("slider_numb", "Slider for Bins", 0, 100, 10)
        #Selectize
        ui.input_selectize("selectize", "Select Island for Scatterplot", ["Dream","Biscoe","Torgersen"])
        #Numeric Input
        ui.input_numeric("numeric", "To be Determined", 0)
        #Check Box
        ui.input_checkbox_group("check", "Species for Data Grid/Table", ["Adelie", "Gentoo", "Chinstrap"])

#Function Block for Main Layout

#Main Layout Column
"Graphs and Data Visualization"
with ui.layout_columns():

    #It took me awhile to figure out what exactly the reactive.calc was doing but I figured it out.
    #The reactive.calc function is simply turning it into a special return value that we are supposed to be returning in all our other functions that work with other react decorators and functions - this was not explained very well
    #This means that we have to filter the data before we graph it though - which means it would change everything?
    #Reactive Calc Function
    
    
    #Data Table
    with ui.card():
        ui.card_header("Data Table")
        @render.data_frame
        def table_frame():
            return render.DataTable(filtered_data())
    #Data Grid
    with ui.card():
        ui.card_header("Data Grid")
        @render.data_frame
        def table_grid():
            return render.DataGrid(filtered_data())
    #Histogram Plotly
    with ui.card():
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotly_hist():
            return px.histogram(filtered_data(), y= "species", nbins = input.slider_numb())
    #Histogram Seaborn
    with ui.card():
        ui.card_header("Seaborn Histogram")
        @render.plot
        def seaborn_hist():
            return sb.histplot(filtered_data(), y = "species", bins = input.slider_numb())
    #Scatterplot
    with ui.card():
        ui.card_header("Scatterplot")
        @render_plotly
        def scatter_plot():
            return px.scatter(filtered_data(), x="body_mass_g", y="flipper_length_mm", color="species")