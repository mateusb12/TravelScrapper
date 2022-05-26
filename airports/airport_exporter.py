import pandas as pd


def export_codes(country_tag: str) -> dict:
    airport_df = pd.read_csv('airport_codes.csv')
    query = airport_df[(airport_df['iso_country'] == country_tag) & (airport_df['iata_code'].notnull())]
    return query.set_index('municipality').to_dict()['iata_code']


if __name__ == '__main__':
    print(export_codes('US'))
