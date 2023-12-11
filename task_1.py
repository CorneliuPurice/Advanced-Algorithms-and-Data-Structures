# Import the utility functions
import functions


def main():
    # The path to the data file containing the London Underground information
    data_file = 'London Underground data.xlsx'

    # Attempt to prepare the data for use in the route planner
    preparation_result = functions.prepare_data(data_file)

    # Exit the program if the data could not be loaded properly
    if preparation_result is None:
        return

    # Unpack the preparation results into usable variables
    data, station_map, edges_dict = preparation_result

    # Construct the graph representation of the London Underground
    graph = functions.create_graph(station_map, edges_dict, 'time')

    # Prompt the user to enter the starting station and remove any leading/trailing whitespace
    start_station = input("Enter the start station: ").strip()

    # Prompt the user to enter the destination station and remove any leading/trailing whitespace
    end_station = input("Enter the end station: ").strip()

    # Utilize the Dijkstra algorithm to find the shortest path and the total journey time
    path, total_time = functions.find_shortest_path(graph, station_map, start_station, end_station, functions.dijkstra)

    # Display the results to the user
    if path:
        # If a path is found, print the path and total travel time
        print(f"The shortest path from {start_station} to {end_station} is: {' -> '.join(path)} "
              f"with a total travel time of {total_time} minutes.")
    else:
        # Inform the user if no path could be found
        print("No path could be found between the selected stations.")

    # Compute the journey times for all station pairs to be used in the histogram
    times = functions.calculate_all_journeys(graph, graph, station_map, functions.dijkstra, 'time')

    # Generate and display a histogram of journey times across the London Underground
    functions.plot_single_histogram(times, title='Histogram of Journey Times',
                                    xlabel='Journey Time (minutes)', bin_size=30)


# Standard Python idiom for invoking the main function
if __name__ == "__main__":
    main()
