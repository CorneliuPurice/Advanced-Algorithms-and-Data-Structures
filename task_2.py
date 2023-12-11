# Import the necessary functions from the functions module
import functions


def main():
    # Specify the data source, which contains information about the London Underground stations
    data_file = 'London Underground data.xlsx'

    # Process the data file, ensuring that it is loaded correctly for further operations
    preparation_result = functions.prepare_data(data_file)

    # If the data preparation fails, exit the function to prevent further errors
    if preparation_result is None:
        return  # Data loading error handling

    # Unpack the returned tuple into separate variables for use in graph creation
    data, station_map, edges_dict = preparation_result

    # Build the graph structure for the stations, using stops as the weight type for edges
    graph = functions.create_graph(station_map, edges_dict, 'stops')

    # Collect the starting and destination station names from user input, with whitespace trimmed
    start_station = input("Enter the start station: ").strip()
    end_station = input("Enter the end station: ").strip()

    # Calculate the shortest path between the entered stations using the Dijkstra algorithm
    path, total_stops = functions.find_shortest_path(graph, station_map, start_station, end_station, functions.dijkstra)

    # Provide feedback to the user based on the path calculation results
    if path:
        # If a valid path is found, print the sequence of stations and the total number of stops
        print(f"The shortest path from {start_station} to {end_station} is: {' -> '.join(path)} "
              f"with a total of {total_stops} stops.")
    else:
        # If no path is found, inform the user accordingly
        print("No path could be found between the selected stations.")

    # Compute the count of stops for all possible journeys between station pairs
    stops = functions.calculate_all_journeys(graph, graph, station_map, functions.dijkstra, 'stops')

    # Generate and display a histogram that visualizes the distribution of stop counts
    functions.plot_single_histogram(stops, title='Histogram of Journey Stops', xlabel='Number of Stops')


# Entry point for script execution, ensuring that the script is being run directly
if __name__ == "__main__":
    main()
