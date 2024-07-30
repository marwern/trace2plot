import os
import matplotlib.pyplot as plt
import numpy as np

def parse_file(path_dir, filename):
    # Initialize data storage
    data = {}
    current_step = -1

    with open(os.path.join(path_dir, filename), "r") as file:
        for line in file:
            line = line.strip()
            if "SIMULATION STEP" in line:
                current_step += 1
                continue

            if ':' in line and not line.startswith('__') and ' : ' in line:
                var_name, value = line.split(' : ')
                # Convert value appropriately
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit():
                    value = float(value)
                elif value in ['true', 'false']:
                    value = True if value == 'true' else False

                if var_name not in data:
                    data[var_name] = []
                # Extend lists if needed
                while len(data[var_name]) < current_step:
                    data[var_name].append(None)
                data[var_name].append(value)

    # Ensure all lists are of equal length
    max_length = max(len(values) for values in data.values())
    for values in data.values():
        while len(values) < max_length:
            values.append(None)

    return data, max_length

def plot_data(data, max_length):
    # Split data into groups of 5 for plotting
    variable_names = list(data.keys())
    num_plots = (len(variable_names) + 4) // 5  # Calculate how many plots are needed

    for i in range(num_plots):
        plt.figure(figsize=(10, 10))
        start_index = i * 5
        end_index = min(start_index + 5, len(variable_names))

        for j in range(start_index, end_index):
            var_name = variable_names[j]
            values = data[var_name]
            ax = plt.subplot(5, 1, j - start_index + 1)
            ax.step(range(max_length), values, where='post', label=var_name)
            ax.set_ylabel(var_name)
            ax.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

def main():
    path_dir: str = r"C:\Users\marce\OneDrive\Tools\averest\averest\examples\PhDExamples\DEBOUNCE"  # add your local path
    filename: str = r"DEBOUNCE.trace.txt"
    data, max_length = parse_file(path_dir, filename)
    plot_data(data, max_length)

if __name__ == '__main__':
    main()