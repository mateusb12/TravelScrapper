import dataclasses

from termcolor import colored
import pandas as pd

from apis.api_cruds.postgres_crud import postgres_get_all_flights_df, postgres_create_flight, postgres_update_flight
from database.fillers.data_skeleton import get_flight_dict_example, convert_flight_to_dict
from database.fillers.time_manipulations import get_today_date
from travel_analysis.dict_filler import flight_dict_filler
from travel_analysis.flight import get_flight_object_example, Flight


@dataclasses.dataclass
class FlightUpdater:
    """
    This class is used to update a dataset with new flights.
    """
    df: pd.DataFrame = None
    query: pd.DataFrame = None
    new_flight: Flight = None
    existing_flight: bool = None
    is_new_flight_cheaper: bool = False
    query_tag: str = "fortaleza_rio"
    cheapest_price: int = 50000
    cheapest_flight: Flight = None
    found_new_cheapest: bool = False
    repeated_flight: bool = False

    # cheapest_flights: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.df = self.get_df_from_postgres()
        self.trim_df()
        self.refresh_cheapest()

    def get_df_from_postgres(self) -> pd.DataFrame:
        output_df = postgres_get_all_flights_df()
        if output_df.empty:
            return self.append_filler_flight(output_df)
        return output_df

    def append_filler_flight(self, input_df: pd.DataFrame):
        filler_flight: dict = get_flight_dict_example()
        filler_flight["flight_tag"] = self.query_tag
        return input_df.append(filler_flight, ignore_index=True)

    def set_new_flight(self, input_flight: Flight) -> None:
        """
        This method sets the new flight.
        """
        self.new_flight = input_flight
        self.existing_flight = self.query_existing_flight(input_flight)
        if self.existing_flight:
            old_flight = self.query.iloc[0]
            old_flight_query_date = old_flight["queryDate"]
            old_price = old_flight.price
            today = get_today_date()
            if old_flight_query_date != today:
                self.insert_new_flight(old_flight, input_flight)
            # self.update_existing_flight(old_flight, input_flight)
        else:
            old_flight = self.cheapest_flight
            old_price = self.cheapest_price
            self.insert_new_flight(old_flight, input_flight)
        new_price = input_flight.price
        self.print_flight_price_diff(old_price, new_price)
        self.refresh_for_new_flight()

    def insert_new_flight(self, old_flight: Flight, input_flight: Flight):
        """
        This method inserts the new flight in the database.
        This method sets the new cheapest flight across the database.
        """
        new_flight_dict = convert_flight_to_dict(input_flight)
        new_flight_dict["flight_tag"] = self.query_tag
        self.new_flight_comparison(old_flight, input_flight)
        if self.is_new_flight_cheaper:
            self.cheapest_flight = input_flight
            self.cheapest_price = input_flight.price
            self.is_new_flight_cheaper = True
            self.found_new_cheapest = True
        postgres_create_flight(new_flight_dict)

    def export_new_cheapest(self) -> Flight or None:
        return self.cheapest_flight if self.found_new_cheapest else None

    def refresh_for_new_flight(self):
        self.repeated_flight = False

    def update_existing_flight(self, old_flight: Flight, new_flight: Flight):
        """
        If the new flight has a cheaper value than the current one, then the current one
         is updated at the postgres database.
        """
        new_flight_dict = convert_flight_to_dict(new_flight)
        new_flight_dict["flight_tag"] = self.query_tag
        self.new_flight_comparison(old_flight, new_flight)
        if self.is_new_flight_cheaper:
            postgres_update_flight(new_flight_dict)
        else:
            self.repeated_flight = True

    def new_flight_comparison(self, old_flight: Flight, new_flight: Flight):
        """
        This method compares the new flight with the current cheapest one.
        """
        old_price: int = old_flight.price if old_flight is not None else 50000
        new_price: int = new_flight.price
        self.is_new_flight_cheaper = new_price < old_price

    def trim_df(self):
        """
        This method trims the dataset according to the query_tag
        """
        self.df = self.df[self.df['flight_tag'] == self.query_tag]
        if self.df.empty:
            self.df = self.append_filler_flight(self.df)

    def query_existing_flight(self, input_flight: Flight) -> bool:
        """
        This method checks if a flight already exists in the dataset.
        """
        link = input_flight.link
        new_flight_row = convert_flight_to_dict(input_flight)
        new_price = new_flight_row["price"]
        new_departure = new_flight_row["departure"]
        new_arrival = new_flight_row["arrival"]
        new_date_departure = new_flight_row["dateDeparture"]
        new_date_arrival = new_flight_row["dateArrival"]
        self.query = self.df[
            (self.df['price'] == new_price) &
            (self.df['departure'] == new_departure) &
            (self.df['arrival'] == new_arrival) &
            (self.df['dateDeparture'] == new_date_departure) &
            (self.df['dateArrival'] == new_date_arrival)
            ]
        return len(self.query) > 0

    def get_cheapest_flight(self):
        return self.df.loc[self.df['price'].idxmin()]

    def refresh_cheapest(self):
        cheapest_row = self.get_cheapest_flight()
        cheapest_dict = cheapest_row.to_dict()
        del cheapest_dict["id"]
        cheapest_price = cheapest_dict["price"]
        flight_dict_filler(cheapest_dict)
        self.cheapest_flight = Flight(cheapest_dict)
        self.cheapest_price = cheapest_price
        # self.cheapest_flight = cheapest_flight

    @staticmethod
    def get_price_diff_tag(old_price: int, new_price: int) -> str:
        """
        This method returns the difference between the new flight price and the cheapest one.
        """
        diff = new_price - old_price
        return colored(f"+{diff}", "red") if diff >= 0 else colored(f"{diff}", "green")

    def print_flight_price_diff(self, old_price: int, new_price: int) -> None:
        """
        This method prints the difference between the new flight price and the cheapest one.
        """
        current_flight_color = 'red' if self.is_new_flight_cheaper else 'cyan'
        new_flight_color = 'green' if self.is_new_flight_cheaper else 'magenta'
        if self.repeated_flight:
            print(colored("Repeated flight. Not doing anything", "yellow"))
            return
        if self.existing_flight:
            print(f"Old price: {colored(str(old_price), current_flight_color)}")
        else:
            print(f"Current cheapest price: {colored(str(old_price), new_flight_color)}")
        print(f"New flight price: {colored(str(new_price), new_flight_color)}")
        print(f"Difference: {self.get_price_diff_tag(old_price, new_price)}")


def flight_pipeline(input_fu: FlightUpdater):
    flight = get_flight_object_example()
    input_fu.set_new_flight(flight)
    print("done")


def __main():
    q = FlightUpdater()
    flight_pipeline(q)
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
