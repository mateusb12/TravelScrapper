def generate_sql_update_line(input_values: dict, table_name: str) -> str:
    first_header = f"update {table_name} set "
    value_headers = "".join(f"{item}='{input_values[item]}', " for item in input_values)[:-2]
    second_header = f"where flight_tag='{input_values['flight_tag']}';"
    return f"{first_header}{value_headers}{second_header}"


def get_sql_line_create(dict_example: dict, values: tuple, table_name: str) -> str:
    columns = list(dict_example.keys())
    if "id" in columns:
        columns.remove("id")
    column_str = "".join(f"{item}, " for item in columns)[:-2]
    header = f"insert into {table_name} ({column_str}) values ("
    for value in values:
        header += f"'{value}', " if isinstance(value, str) else f"{value}, "
    return f"{header[:-2]});"
