from bokeh.plotting import figure, output_file, show

class visualization:
    def __init__(self, df):
        self.df = df

    def volume_plot(self):
        # define the data in x -axis
        x = [i for i in range(100)]
        y = self.df['Volume'].tolist()

        # create a new plot with a title and axis labels
        p = figure(title=f"Volume of transaction for IBM", x_axis_label="time", y_axis_label="Volume")

        # add a line renderer with legend and line thickness
        p.line(x, y, legend_label="Line", line_width=2)

        # output to a static HTML file
        output_file(f"line_volume_plot IBM.html")

        # show the plot
        show(p)

    
    def close_plot(self):
        # define the data in x -axis
        x = [i for i in range(100)]
        y = self.df['Close'].tolist()

        # create a new plot with a title and axis labels
        p = figure(title=f"Closing price for IBM", x_axis_label="time", y_axis_label="Closing Price")

        # add a line renderer with legend and line thickness
        p.line(x, y, legend_label="Line", line_width=2)

        # output to a static HTML file
        output_file(f"line_close_plot IBM.html")

        # show the plot
        show(p)
