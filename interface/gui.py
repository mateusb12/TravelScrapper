import tkinter as tk
from tkinter import ttk


class TravelGui:
    def __init__(self):
        self.root = tk.Tk()
        style = ttk.Style()
        style.theme_use("clam")
        self.__window_operations()
        self.__instantiate_elements()
        self.root.mainloop()

    def __window_operations(self):
        self.__centralize_window_at_screen()
        self.root.title("Flight Search")
        self.root.geometry("300x500")

    def __instantiate_elements(self):
        self.__create_input_folder_name(pad_x=10, pad_y=10)
        self.__create_input_departure_airport()
        self.__create_input_arrival_airport()
        # self.__create_input_maximum_price()
        # self.__create_input_maximum_duration()

    def __centralize_window_at_screen(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (self.root.winfo_reqwidth() / 2)
        y_coordinate = (screen_height / 2) - (self.root.winfo_reqheight() / 2)
        self.root.geometry(f"+{int(x_coordinate)}+{int(y_coordinate)}")

    def __create_input_folder_name(self, pad_x: int = 0, pad_y: int = 0):
        self.folder_name_entry = tk.Entry(self.root)
        self.folder_name_entry.pack()
        label = tk.Label(self.root, text="Folder Name")
        label.pack(side="top", fill="x", expand=False, before=self.folder_name_entry, pady=10)

    def __create_airport_dropdown(self, airport_type: str) -> (tk.StringVar, tk.OptionMenu):
        label = tk.Label(self.root, text=f"{airport_type} Airport")
        label.pack(side="top", after=self.folder_name_entry, pady=10)
        options = ["JFK", "ORD", "ATL", "LAX", "DFW"]
        first_option = options[0]
        var = tk.StringVar(self.root)
        var.set(first_option)
        dropdown = ttk.OptionMenu(self.root, var, first_option, *options)
        dropdown.pack(side="top", after=label, pady=5)
        return var, dropdown

    def __create_input_departure_airport(self):
        self.departure_airport_var, self.departure_airport_dropdown = self.__create_airport_dropdown("Departure")

    def __create_input_arrival_airport(self):
        self.arrival_airport_var, self.arrival_airport_dropdown = self.__create_airport_dropdown("Arrival")

    def __create_input_maximum_price(self, pad_x: int = 0, pad_y: int = 0):
        # Text input field for maximum price
        tk.Label(self.root, text="Maximum Price").grid(row=3, column=0)
        self.maximum_price_entry = tk.Entry(self.root)
        self.maximum_price_entry.grid(row=3, column=1, padx=pad_x, pady=pad_y)

    def __create_input_maximum_duration(self, pad_x: int = 0, pad_y: int = 0):
        # Labels and dropdowns for maximum duration
        tk.Label(self.root, text="Maximum Duration").grid(row=4, column=0)
        tk.Label(self.root, text="Hours").grid(row=4, column=1)
        tk.Label(self.root, text="Minutes").grid(row=4, column=2)
        self.hours_var = tk.StringVar(self.root)
        self.hours_dropdown = tk.OptionMenu(self.root, self.hours_var, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                                            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                                            "22", "23")
        self.hours_dropdown.grid(row=5, column=1)
        self.minutes_var = tk.StringVar(self.root)
        self.minutes_dropdown = tk.OptionMenu(self.root, self.minutes_var, "0", "15", "30", "45")
        self.minutes_dropdown.grid(row=5, column=2, padx=pad_x, pady=pad_y)


def __main():
    tg = TravelGui()


if __name__ == "__main__":
    __main()
