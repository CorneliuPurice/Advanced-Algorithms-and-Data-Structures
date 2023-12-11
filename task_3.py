# Import the functions module which contains necessary utilities for the operation
import functions


def main():
    # Define the path to the dataset which contains information about the London Underground
    data_file = 'London Underground data.xlsx'

    # Load and prepare the data from the provided dataset
    preparation_result = functions.prepare_data(data_file)

    # If the data could not be loaded properly, exit the function early
    if preparation_result is None:
        return  # Exit if data preparation is unsuccessful

    # Extract usable variables from the prepared data for graph construction
    data, station_map, edges_dict = preparation_result

    # Construct a graph representation of the tube system with 'stops' as edge weights
    graph = functions.create_graph(station_map, edges_dict, 'stops')

    # Request and process user input for the starting point of the journey
    start_station = input("Enter the start station: ").strip()
    # Request and process user input for the journey's destination
    end_station = input("Enter the end station: ").strip()

    # Determine the shortest path between the two stations using Breadth-First Search (BFS)
    path, total_stops = functions.find_shortest_path(graph, station_map, start_station, end_station, functions.bfs)

    # Provide the user with the outcome of their query
    if path:
        # If a path is found, print out the journey details
        print(f"The shortest path from {start_station} to {end_station} is: {' -> '.join(path)} "
              f"with a total of {total_stops} stops.")
    else:
        # Notify the user if no path is available between the selected stations
        print("No path could be found between the selected stations.")

    # Perform calculations on all journeys between each pair of stations using BFS
    stops = functions.calculate_all_journeys(graph, graph, station_map, functions.bfs, 'stops')
    # Visualize the distribution of the number of stops for all journeys with a histogram
    functions.plot_single_histogram(stops, title='Histogram of Journey Stops', xlabel='Number of Stops')


# Ensures this script runs only when executed directly and not when imported as a module
if __name__ == "__main__":
    main()
