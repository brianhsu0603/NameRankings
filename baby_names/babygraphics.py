"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui
from scrape import scrape_names

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    return float((width-2*GRAPH_MARGIN_SIZE)/len(YEARS)) * year_index + GRAPH_MARGIN_SIZE


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################

    canvas.create_line(GRAPH_MARGIN_SIZE, 0, GRAPH_MARGIN_SIZE, CANVAS_HEIGHT)
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    for index in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, index) 
        canvas.create_line(x , 0, x, CANVAS_HEIGHT)
        canvas.create_text(x+TEXT_DX , CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text = YEARS[index], anchor = tkinter.NW)  

def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    color_index = 0
    for name in lookup_names:
        color = COLORS[color_index]
        for year_index in range(len(YEARS)):
            if year_index == len(YEARS)-1:
                start_point_x = get_x_coordinate(CANVAS_WIDTH, year_index)
                if str(YEARS[year_index]) not in name_data[name]:
                    start_point_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                    canvas.create_text(start_point_x + TEXT_DX, start_point_y, text = name + " *", anchor = tkinter.SW, fill = color)
                else:
                    start_point_y = int(name_data[name][str(YEARS[year_index])])/200 * (CANVAS_HEIGHT - 2*GRAPH_MARGIN_SIZE) + GRAPH_MARGIN_SIZE
                    rank = name_data[name][str(YEARS[year_index])]
                    canvas.create_text(start_point_x + TEXT_DX, start_point_y, text = name + " " + rank, anchor = tkinter.SW, fill = color)

            else:
                start_point_x = get_x_coordinate(CANVAS_WIDTH, year_index)
                if str(YEARS[year_index]) not in name_data[name]:
                    start_point_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                    canvas.create_text(start_point_x + TEXT_DX, start_point_y, text = name + " *", anchor = tkinter.SW, fill = color)
                else:
                    start_point_y = int(name_data[name][str(YEARS[year_index])])/200 * (CANVAS_HEIGHT - 2*GRAPH_MARGIN_SIZE) + GRAPH_MARGIN_SIZE
                    rank = name_data[name][str(YEARS[year_index])]
                    canvas.create_text(start_point_x + TEXT_DX, start_point_y, text = name + " " + rank, anchor = tkinter.SW, fill = color)

                end_point_x = get_x_coordinate(CANVAS_WIDTH, year_index+1)
                if str(YEARS[year_index+1]) not in name_data[name]:
                    end_point_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE 
                else:
                    end_point_y = int(name_data[name][str(YEARS[year_index+1])])/200 * (CANVAS_HEIGHT - 2*GRAPH_MARGIN_SIZE) + GRAPH_MARGIN_SIZE
            
                canvas.create_line(start_point_x, start_point_y, end_point_x, end_point_y, fill = color, width = LINE_WIDTH)

        color_index += 1
        if color_index > 3:
            color_index = 0





# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    #scrape data
    files = []
    for year in YEARS:
        file = scrape_names(year)
        files.append(file)

    # Load data
    name_data = babynames.read_files(files)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
