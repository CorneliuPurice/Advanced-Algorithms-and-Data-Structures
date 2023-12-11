# Import necessary libraries and modules for data handling and graph operations
import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from bfs import bfs
from mst import kruskal


# Define a function to load data from an Excel file
def load_data(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


# Define a function to clean and standardize station names from the data
def clean_station_names(data):
    # Strip leading/trailing whitespace from station names
    data['Station (from)'] = data['Station (from)'].str.strip()
    data['Station (to)'] = data['Station (to)'].str.strip()


# Define a function to extract a set of unique stations and create a mapping to indices
def get_unique_stations(data):
    # Create a set of all unique station names and sort them
    stations_set = set(data['Station (from)']).union(set(data['Station (to)']))
    stations_sorted_list = sorted(stations_set)
    # Map each station name to a unique index
    station_map = {station: index for index, station in enumerate(stations_sorted_list)}
    return station_map


# Define a function to map station pairs to their corresponding indices and associated data
def map_stations_to_indices(data, station_map):
    edges_dict = {}
    for _, row in data.iterrows():
        # Extract station names and journey time from the row
        from_station, to_station, time = row['Station (from)'], row['Station (to)'], row['Time (minutes)']
        # Retrieve indices for the stations
        from_index = station_map[from_station]
        to_index = station_map[to_station]
        # Create a sorted tuple key to represent the edge
        edge_key = tuple(sorted((from_index, to_index)))

        # If the edge already exists, retain the minimum time; otherwise, add the new edge
        if edge_key in edges_dict:
            edges_dict[edge_key] = {
                'time': min(time, edges_dict[edge_key]['time']),  # keep the minimum time
                'stops': 1  # constant for a single stop
            }
        else:
            edges_dict[edge_key] = {
                'time': time,  # initial time
                'stops': 1  # constant for a single stop
            }

    return edges_dict


# Define a function to orchestrate the data preparation steps
def prepare_data(file_path):
    data = load_data(file_path)
    if data is None:
        print("Failed to load data.")
        return None

    # Clean station names and generate mappings and edge data
    clean_station_names(data)
    station_map = get_unique_stations(data)
    edges_dict = map_stations_to_indices(data, station_map)

    return data, station_map, edges_dict


# Define a function to create a graph from the station and edge data
def create_graph(station_map, edges_dict, weight_type):
    if weight_type not in ['time', 'stops']:
        raise ValueError("weight_type must be either 'time' or 'stops'")

    # Instantiate a new AdjacencyListGraph with the size based on the station map
    graph = AdjacencyListGraph(len(station_map), directed=False, weighted=True)
    # Insert edges with the appropriate weights into the graph
    for (from_index, to_index), weights in edges_dict.items():
        try:
            graph.insert_edge(from_index, to_index, weight=weights[weight_type])
        except Exception as e:
            print(f"Error inserting edge: {e}")

    return graph


# Define a function to perform reverse lookup from index to station name
def reverse_lookup(station_map, index):
    for station, idx in station_map.items():
        if idx == index:
            return station
    return None  # Return None if the station was not found


# Define a function to reconstruct the path from predecessor indices
def reconstruct_path(predecessors, station_map, start_index, end_index):
    path = []
    current_index = end_index
    # Backtrack from the destination index to the start index using the predecessors
    while current_index != start_index:
        current_station = reverse_lookup(station_map, current_index)
        if current_station:
            path.insert(0, current_station)
            current_index = predecessors[current_index]
        else:
            print("Station index not found in map.")
            return []
    # Insert the start station at the beginning of the path
    path.insert(0, reverse_lookup(station_map, start_index))
    return path


# Define a function to find the shortest path between two stations using a specified algorithm
def find_shortest_path(graph, station_map, start_station, end_station, algorithm):
    if start_station not in station_map or end_station not in station_map:
        print("One or both of the stations are invalid.")
        return [], 0

    # Determine the indices for the start and end stations
    start_index = station_map[start_station]
    end_index = station_map[end_station]

    # Execute the appropriate algorithm to find the shortest path
    if algorithm == dijkstra:
        distances, predecessors = dijkstra(graph, start_index)
    elif algorithm == bfs:
        distances, predecessors = bfs(graph, start_index)
    else:
        raise ValueError("Unsupported algorithm")

    # Verify that a path exists
    if predecessors[end_index] is None:
        print(f"No path exists between {start_station} and {end_station}.")
        return [], 0

    # Construct the path using the predecessor information
    path = reconstruct_path(predecessors, station_map, start_index, end_index)
    # Determine the total distance or stops based on the shortest path found
    total_value = distances[end_index]

    return path, total_value


# Define a function to calculate all journey metrics across the graph for either time or stops
def calculate_all_journeys(graph_time, graph_stops, station_map, algorithm, calculation_type):
    all_journey_times = set()
    all_journey_stops = set()

    for start_station, start_index in station_map.items():
        if calculation_type in ['time', 'both']:
            # Calculate distances for journey times
            distances_time, *_ = algorithm(graph_time, start_index)
            for end_index in range(len(distances_time)):
                if end_index != start_index and distances_time[end_index] != float('inf'):
                    journey = tuple(sorted([start_index, end_index]))
                    all_journey_times.add((journey, distances_time[end_index]))

        if calculation_type in ['stops', 'both']:
            # Calculate distances for journey stops
            distances_stops, *_ = algorithm(graph_stops, start_index)
            for end_index in range(len(distances_stops)):
                if end_index != start_index and distances_stops[end_index] != float('inf'):
                    journey = tuple(sorted([start_index, end_index]))
                    all_journey_stops.add((journey, distances_stops[end_index]))

    if calculation_type == 'time':
        return [time for journey, time in all_journey_times]
    elif calculation_type == 'stops':
        return [stops for journey, stops in all_journey_stops]
    else:
        return [time for journey, time in all_journey_times], [stops for journey, stops in all_journey_stops]


"""   Functions just for task 4   """


# Function to generate a minimum spanning tree (MST) of a graph using Kruskal's algorithm
def generate_mst(graph):
    # The MST is generated to ensure connectivity with the minimum possible total edge weight
    return kruskal(graph)


# Function to identify which edges can be removed from the graph based on the MST
def identify_edges_to_remove(graph, mst):
    # Initialize an empty list to keep track of the edges that can be removed
    edges_to_remove = []
    # Iterate through all edges in the graph
    for u, v in graph.get_edge_list():
        # If an edge is not present in the MST, it is not crucial for connectivity and can be removed
        if not mst.has_edge(u, v):
            edges_to_remove.append((u, v))
    # Return the list of removable edges
    return edges_to_remove


# Function to simulate the closure of certain edges in the graph
def simulate_closure(graph, edges_to_remove):
    # Iterate through the list of edges to remove
    for u, v in edges_to_remove:
        # Remove the edge from the graph to simulate its closure
        graph.delete_edge(u, v)


# Function to print out the list of edges (stations) that will be removed from the graph
def print_edges_to_remove(edges_to_remove, station_map):
    print("Edges to remove:")
    # Iterate through the removable edges
    for u, v in edges_to_remove:
        # Look up station names from the station indices
        station_u = [name for name, index in station_map.items() if index == u][0]
        station_v = [name for name, index in station_map.items() if index == v][0]
        # Print the stations corresponding to the removable edge
        print(f"{station_u} -- {station_v}")


# Function to plot a histogram of data with customizations for title and axes labels
def plot_single_histogram(data, title, xlabel, bin_size=None):
    # Set up the figure size for the histogram
    plt.figure(figsize=(8, 6))

    # Determine the bin size for the histogram; default to range if bin_size is not specified
    bins = bin_size if bin_size is not None else range(int(min(data)), int(max(data)) + 1, 1)

    # Plot the histogram with the specified bin settings and formatting
    plt.hist(data, bins=bins, color='blue', edgecolor='black')
    plt.title(title)  # Set the title of the histogram
    plt.xlabel(xlabel)  # Set the x-axis label
    plt.ylabel('Frequency')  # Set the y-axis label
    plt.grid(axis='y', alpha=0.75)  # Enable grid lines for the y-axis with specified opacity
    plt.show()  # Display the histogram


# Function to plot multiple histograms before and after a certain simulation or event
def plot_multiple_histograms(before, after, title, xlabel, plot_type='regular'):
    # Set up the figure size to accommodate three subplots side by side
    plt.figure(figsize=(20, 6))

    # Determine bin settings based on whether a range of values is specified
    bin_setting = 30 if plot_type != 'range' else range(int(min(before + after)), int(max(before + after)) + 1, 1)

    # Subplot for the histogram of data before the event or simulation
    plt.subplot(1, 3, 1)  # Position the subplot in a 1x3 grid, at position 1
    plt.hist(before, bins=bin_setting, color='blue', alpha=0.7, edgecolor='black')
    plt.title(f'Before Closure - {title}')  # Set the title for this subplot
    plt.xlabel(xlabel)  # Set the x-axis label
    plt.ylabel('Frequency')  # Set the y-axis label

    # Subplot for the histogram of data after the event or simulation
    plt.subplot(1, 3, 2)  # Position the subplot in a 1x3 grid, at position 2
    plt.hist(after, bins=bin_setting, color='red', alpha=0.7, edgecolor='black')
    plt.title(f'After Closure - {title}')  # Set the title for this subplot
    plt.xlabel(xlabel)  # Set the x-axis label
    plt.ylabel('Frequency')  # Set the y-axis label

    # Subplot for the overlapping comparison of data before and after the event or simulation
    plt.subplot(1, 3, 3)  # Position the subplot in a 1x3 grid, at position 3
    plt.hist(before, bins=bin_setting, color='blue', alpha=0.5, edgecolor='black', label='Before')
    plt.hist(after, bins=bin_setting, color='red', alpha=0.5, edgecolor='black', label='After')
    plt.title(f'Comparison - {title}')  # Set the title for this subplot
    plt.xlabel(xlabel)  # Set the x-axis label
    plt.ylabel('Frequency')  # Set the y-axis label
    plt.legend(loc='upper right')  # Add a legend to distinguish between the two datasets

    plt.tight_layout()  # Adjust the layout so that plots do not overlap
    plt.show()  # Display the histograms
