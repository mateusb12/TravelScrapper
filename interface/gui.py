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
        self.root.geometry("300x450")

    def __instantiate_elements(self):
        self.__create_input_folder_name()
        self.__create_input_departure_airport()
        self.__create_input_arrival_airport()
        self.__create_input_maximum_price()
        self.__create_input_maximum_duration()
        self.__create_query_button()

    def __centralize_window_at_screen(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width * 0.5) - (self.root.winfo_reqwidth() / 2)
        y_coordinate = (screen_height * 0.4) - (self.root.winfo_reqheight() / 2)
        self.root.geometry(f"+{int(x_coordinate)}+{int(y_coordinate)}")

    def __create_input_folder_name(self):
        self.folder_name_entry = tk.Entry(self.root)
        self.folder_name_entry.pack()
        self.folder_name_entry.insert(0, "flight_data")
        label = tk.Label(self.root, text="Folder Name")
        label.pack(side="top", fill="x", expand=False, before=self.folder_name_entry, pady=10)

    def __create_airport_dropdown(self, airport_type: str, after=None) -> (tk.StringVar, tk.OptionMenu):
        label = tk.Label(self.root, text=f"{airport_type} Airport")
        if after is None:
            label.pack(side="top", after=self.folder_name_entry, pady=10)
        else:
            label.pack(side="top", after=after, pady=10)
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
        self.arrival_airport_var, self.arrival_airport_dropdown = \
            self.__create_airport_dropdown("Arrival", after=self.departure_airport_dropdown)

    def __create_input_maximum_price(self,):
        label = tk.Label(self.root, text="Maximum Price")
        label.pack(side="top", after=self.arrival_airport_dropdown, pady=10)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.insert(0, "300")
        self.price_entry.pack(side="top", after=label, pady=5)

    def __create_input_maximum_duration(self):
        # Create a frame to hold the hours and minutes dropdown menus
        self.duration_frame = tk.Frame(self.root)
        self.duration_frame.pack(side="top", after=self.price_entry, pady=15)

        # Create hours dropdown
        hours_label = tk.Label(self.duration_frame, text="Hours")
        hours_label.pack(side="left", pady=5)
        hours_options = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        first_hour_option = hours_options[0]
        self.hours_var = tk.StringVar(self.duration_frame)
        self.hours_var.set(first_hour_option)
        self.hours_dropdown = ttk.OptionMenu(self.duration_frame, self.hours_var, first_hour_option, *hours_options)
        self.hours_dropdown.pack(side="left", pady=5, padx=10)

        # Create minutes dropdown
        minutes_label = tk.Label(self.duration_frame, text="Minutes")
        minutes_label.pack(side="left", pady=5)
        minutes_options = ["0", "10", "20", "30", "40", "50"]
        first_minute_option = minutes_options[0]
        self.minutes_var = tk.StringVar(self.duration_frame)
        self.minutes_var.set(first_minute_option)
        self.minutes_dropdown = ttk.OptionMenu(self.duration_frame, self.minutes_var,
                                               first_minute_option, *minutes_options)
        self.minutes_dropdown.pack(side="left", pady=5)

        self.hours_dropdown.configure(width=2)
        self.minutes_dropdown.configure(width=2)

    def __create_query_button(self):
        self.query_button = tk.Button(self.root, text="Query", command=self.execute_query_button)
        self.query_button.pack(side="top", after=self.duration_frame, pady=10)
        self.query_button["background"] = "blue"
        self.query_button["foreground"] = "white"
        self.query_button["font"] = ("Helvetica", 14, "bold")
        self.query_button["relief"] = "groove"
        self.query_button["highlightbackground"] = "black"

    def execute_query_button(self):
        folder_name = self.folder_name_entry.get()
        departure_airport = self.departure_airport_var.get()
        arrival_airport = self.arrival_airport_var.get()
        maximum_price = self.price_entry.get()
        hours = self.hours_var.get()
        minutes = self.minutes_var.get()
        maximum_duration = f"{hours}h{minutes}m"
        print(f"Folder Name: {folder_name}")
        print(f"Departure Airport: {departure_airport}")
        print(f"Arrival Airport: {arrival_airport}")
        print(f"Maximum Price: {maximum_price}")
        print(f"Maximum Duration: {maximum_duration}")


def __main():
    tg = TravelGui()


if __name__ == "__main__":
    __main()
