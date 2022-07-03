import dataclasses
from pathlib import Path

from termcolor import colored
import pandas as pd

from references.reference import get_datasets_reference
from travel_analysis.flight import get_flight_example, Flight


@dataclasses.dataclass
class FlightUpdater:
    """
    This class is used to update a dataset with new flights.
    """
    df: pd.DataFrame
    query: pd.DataFrame = None
    new_flight: Flight = None
    existing_flight: bool = None

    def set_new_flight(self, input_flight: Flight) -> None:
        """
        This method sets the new flight.
        """
        self.new_flight = input_flight
        self.query = self.query_existing_flight(input_flight)
        self.existing_flight = len(self.query) > 0

    def query_existing_flight(self, input_flight: Flight) -> pd.DataFrame:
        """
        This method checks if a flight already exists in the dataset.
        """
        city_from = input_flight.flight_from
        city_to = input_flight.flight_to
        return self.df.loc[(self.df['cityFrom'] == city_from) & (self.df['cityTo'] == city_to)]

    def get_cheapest_price(self) -> float:
        """
        This method returns the cheapest price of the current query.
        """
        return self.query['price'].min()

    def is_new_flight_cheaper(self) -> bool:
        """
        This method checks if the new flight is cheaper than the cheapest one.
        """
        return self.new_flight.price < self.get_cheapest_price()

    def get_price_diff_tag(self) -> str:
        """
        This method returns the difference between the new flight price and the cheapest one.
        """
        diff = self.new_flight.price - self.get_cheapest_price()
        return colored(f"+{diff}", "red") if diff > 0 else colored(f"{diff}", "green")

    def print_flight_price_diff(self) -> None:
        """
        This method prints the difference between the new flight price and the cheapest one.
        """
        is_new_flight_cheaper = self.is_new_flight_cheaper()
        current_flight_color = 'red' if is_new_flight_cheaper else 'cyan'
        new_flight_color = 'green' if is_new_flight_cheaper else 'magenta'
        print(f"Current cheapest price: {colored(str(self.get_cheapest_price()), current_flight_color)}")
        print(f"New flight price: {colored(str(self.new_flight.price), new_flight_color)}")
        print(f"Difference: {self.get_price_diff_tag()}")

    def append_new_flight(self) -> None:
        """
        This method appends the new flight to the dataset.
        """
        self.print_flight_price_diff()
        new_row = self.new_flight.convert_to_series()
        df = self.df
        df = pd.concat([df, new_row], ignore_index=True)
        df = df.assign(id=(df['cityFrom'] + '_' + df['cityTo']).astype('category').cat.codes)
        df.insert(0, "id", df.pop("id"))
        df = df.sort_values(by='id', inplace=False)
        self.df = df
        print(colored("New flight added to dataset!", "green"))
        print(new_row)


def __main():
    dataset = pd.read_csv(Path(get_datasets_reference(), 'test_df.csv'))
    flight = get_flight_example()
    fu = FlightUpdater(df=dataset)
    fu.set_new_flight(flight)
    fu.append_new_flight()


if __name__ == "__main__":
    __main()
