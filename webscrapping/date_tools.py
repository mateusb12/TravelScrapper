def strip_date(input_date: str = "01/01/2021") -> str:
    month_table = {"01": "janeiro", "02": "fevereiro", "03": "março", "04": "abril", "05": "maio", "06": "junho",
                   "07": "julho", "08": "agosto", "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"}
    day, month, year = input_date.split("/")
    return f"{month_table[month]} de {year}"
