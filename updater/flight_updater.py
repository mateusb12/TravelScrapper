import dataclasses
from pathlib import Path

from termcolor import colored
import pandas as pd

from queries.postgres_crud import postgres_get_flight_df
from references.paths import get_datasets_reference
from travel_analysis.flight import get_flight_example, Flight


@dataclasses.dataclass
class FlightUpdater:
    """
    This class is used to update a dataset with new flights.
    """
    df: pd.DataFrame = postgres_get_flight_df()
    query: pd.DataFrame = None
    new_flight: Flight = None
    existing_flight: bool = None
    query_tag: str = "fortaleza_rio"
    cheapest_price: int = 50000
    cheapest_flight: Flight = None
    # cheapest_flights: list = dataclasses.field(default_factory=list)

    def set_new_flight(self, input_flight: Flight) -> None:
        """
        This method sets the new flight.
        """
        self.new_flight = input_flight
        query = self.query_existing_flight(input_flight)
        self.existing_flight = len(self.query) > 0
        self.flight_comparison(input_flight)
        if self.existing_flight:
            self.flight_comparison(input_flight)

    def register_new_flight(self):
        pass

    def flight_comparison(self, new_flight: Flight):
        new_price = new_flight.price
        if new_price < self.cheapest_price:
            self.cheapest_price = new_price
            self.cheapest_flight = new_flight

    def trim_df(self):
        """
        This method trims the dataset according to the query_tag
        """
        self.df = self.df[self.df['flight_tag'] == self.query_tag]

    def query_existing_flight(self, input_flight: Flight) -> pd.DataFrame:
        """
        This method checks if a flight already exists in the dataset.
        """
        link = input_flight.link
        return self.df[self.df['link'] == link]

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
        return colored(f"+{diff}", "red") if diff >= 0 else colored(f"{diff}", "green")

    def print_flight_price_diff(self) -> None:
        """
        This method prints the difference between the new flight price and the cheapest one.
        """
        is_new_flight_cheaper = self.is_new_flight_cheaper()
        if is_new_flight_cheaper:
            self.cheapest_flights.append(self.new_flight)
        current_flight_color = 'red' if is_new_flight_cheaper else 'cyan'
        new_flight_color = 'green' if is_new_flight_cheaper else 'magenta'
        print(f"Current cheapest price: {colored(str(self.get_cheapest_price()), current_flight_color)}")
        print(f"New flight price: {colored(str(self.new_flight.price), new_flight_color)}")
        print(f"Difference: {self.get_price_diff_tag()}")

    @staticmethod
    def append_series(input_df: pd.DataFrame, input_new_row: pd.Series) -> pd.DataFrame:
        df_columns = input_df.columns
        df_list = list(input_df.values.tolist())
        new_row_list = input_new_row.values.tolist()
        df_list.append(new_row_list)
        return pd.DataFrame(df_list, columns=df_columns)

    def reorder_df(self):
        df = self.df
        df = df.assign(id=(df['cityFrom'] + '_' + df['cityTo']).astype('category').cat.codes)
        df.insert(0, "id", df.pop("id"))
        self.df = df.sort_values(by='id', inplace=False)

    def is_existing_flight(self, input_flight: pd.DataFrame) -> bool:
        row = input_flight.iloc[0]
        return self.df.isin([*row]).all(1).any()

    def append_new_flight(self) -> None:
        """
        This method appends the new flight to the dataset.
        """
        self.print_flight_price_diff()
        new_flight = self.new_flight.convert_to_series()
        if not self.is_existing_flight(new_flight):
            self.df = pd.concat([self.df, new_flight], axis=0)
            self.reorder_df()
            print(colored("New flight added to dataset!", "yellow"))
        else:
            print(colored("Flight already exists in dataset!", "red"))

    def get_new_cheapest(self) -> Flight:
        cheapest = None
        for flight in self.cheapest_flights:
            if cheapest is None or flight.price < cheapest.price:
                cheapest = flight
        return cheapest

    def save_df(self):
        """
        This method saves the dataset.
        """
        dataset_folder = get_datasets_reference()
        ref = Path(dataset_folder, self.filename)
        self.df.sort_values(by='price', inplace=True)
        self.df.to_csv(ref, index=False, encoding='utf-8')
        print(colored("Dataset saved!", "green"))


def flight_pipeline(input_fu: FlightUpdater):
    flight = get_flight_example()
    input_fu.set_new_flight(flight)
    input_fu.append_new_flight()


def __main():
    flight_pipeline(FlightUpdater())
    # filename = "1.csv"
    # dataset = pd.read_csv(Path(get_datasets_reference(), filename))
    # dataset.tag = filename
    # fu = FlightUpdater(df=dataset)
    # for _ in range(10):
    #     flight_pipeline(fu)
    # fu.reorder_df()
    # print("done")
    # fu.save_df()


if __name__ == "__main__":
    __main()
