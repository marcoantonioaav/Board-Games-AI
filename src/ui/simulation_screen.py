from ui.util import clear_terminal


def print_simulating_text():
    print(" Simulating ")

def get_number_of_bars(simulation, max_simulations):
    return min(int((10*(simulation+1))/max_simulations), 10)

def get_loading_bar_string(simulation, max_simulations):
    bar = ""
    bar_number = get_number_of_bars(simulation, max_simulations)
    for i in range(bar_number):
        bar += "="
    for i in range(10 - bar_number):
        bar += " "
    return f"[{bar}]"

def print_loading_bar(simulation, max_simulations):
    print(get_loading_bar_string(simulation, max_simulations))

def print_expected_time_left(simulation, max_simulations, spent_time_avg):
    expected_time = max_simulations*spent_time_avg - (simulation+1)*spent_time_avg
    print(f"Time left: {int(expected_time)}s")

def print_simulation_frame(simulation, max_simulations, spent_time_avg):
    clear_terminal()
    print_simulating_text()
    print_loading_bar(simulation, max_simulations)
    print_expected_time_left(simulation, max_simulations, spent_time_avg)