import pandas as pd

from references.paths import get_airports_reference


def export_codes(country_tag: str) -> dict:
    airports_folder = get_airports_reference()
    airport_codes_df_ref = airports_folder / "airport_codes.csv"
    airport_df = pd.read_csv(airport_codes_df_ref)
    query = airport_df[(airport_df['iso_country'] == country_tag) & (airport_df['iata_code'].notnull())]
    query_dict = query.set_index('municipality').to_dict()['iata_code']
    filtered_dict = {key: value for key, value in query_dict.items() if len(value) == 3
                     and key != "nan" and isinstance(key, str) and isinstance(value, str)}
    return dict(sorted(filtered_dict.items()))


def __main():
    aux = export_codes('BR')
    return


if __name__ == '__main__':
    __main()
