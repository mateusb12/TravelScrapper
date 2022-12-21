from matplotlib import pyplot as plt

from random_generated_flights.random_data_generator import FlightDataGenerator


class FlightChart:
    def __init__(self, list_of_flights: list[dict]):
        self.data = list_of_flights

    def plot(self):
        # extract the prices and query dates from the data
        prices = [flight["price"] for flight in self.data]
        dates = [flight["queryDate"] for flight in self.data]

        # set the figure size and create a figure and an axis
        plt.figure(figsize=(40, 35))
        fig, ax = plt.subplots()

        # plot the line chart with dot markers
        ax.plot(dates, prices, '-o')

        # set the y-axis label and the y-axis limits
        ax.set_ylabel("Price")
        ax.set_ylim(0, max(prices) * 1.1)

        # set the x-axis label and the x-axis limits
        ax.set_xlim(dates[0], dates[-1])

        # set the grid style and the tick frequency
        ax.grid(linewidth=0.5)
        plt.xticks(rotation=25, fontsize=9, fontname="Arial", y=+0.02, fontweight="bold")

        # add the horizontal line at price = 120
        ax.axhline(y=120, linewidth=1, color='red')

        # Set the graph title
        ax.set_title("Flight Prices over Time", fontsize=12, fontname="Arial")

        # show the plot
        plt.show()


def __main():
    fdg = FlightDataGenerator()
    aux = fdg.generate_multiple_simple_flights(10)
    fc = FlightChart(aux)
    fc.plot()
    return


if __name__ == "__main__":
    __main()
