import pandas as pd
from matplotlib import pyplot as plt
import datetime

from apis.api_cruds.postgres_crud import postgres_get_all_flights_df


def get_flights() -> pd.DataFrame:
    flights = postgres_get_all_flights_df()
    flights = flights.iloc[1:]
    flights["formatDate"] = pd.to_datetime(flights["queryDate"], format="%d-%m-%Y")
    flights.sort_values(by=["formatDate", "price"], inplace=True, ascending=[False, True])
    return flights


def get_recent_flights(destination: str):
    flights = get_flights()
    flights = flights[flights["cityTo"] == destination]
    flights = flights.groupby(["queryDate", "price"]).first().reset_index()
    flights.sort_values(by=["queryDate"], inplace=True, ascending=[False])
    return flights


def line_format(label: datetime):
    """
    Convert time label to the format of pandas line plot
    """
    day = label.day
    month = label.month_name()[:3]
    return f"{day}-{month}"


def plot_graph(input_df: pd.DataFrame):
    plt.figure()
    plt.rcParams.update({'font.size': 16})
    ax = input_df.plot(x="formatDate", y="price", kind="line", figsize=(15, 8), fontsize=16)
    ax.set_xticklabels(map(line_format, input_df["formatDate"]))
    plt.show()


def __main():
    aux = get_recent_flights("Rio de Janeiro")
    plot_graph(aux)
    print("nice")


if __name__ == "__main__":
    __main()
