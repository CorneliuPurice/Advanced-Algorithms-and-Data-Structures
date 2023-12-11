# Import the custom functions module for the London Underground route planner
import functions


def main():
    # Path to the data source containing the London Underground stations and connections
    data_file = 'London Underground data.xlsx'

    # Load and prepare the data; exit if unsuccessful
    preparation_result = functions.prepare_data(data_file)
    if preparation_result is None:
        return  # Early exit if data preparation fails

    # Unpack the data into a station map and edges dictionary for graph construction
    data, station_map, edges_dict = preparation_result

    # Update the edges dictionary to reflect both time and stops data
    edges_dict = functions.map_stations_to_indices(data, station_map)

    # Create two separate graph representations of the tube system
    # One graph is weighted by journey time, and the other by the number of stops
    graph_time = functions.create_graph(station_map, edges_dict, 'time')
    graph_stops = functions.create_graph(station_map, edges_dict, 'stops')

    # Compute initial journey metrics (times and stops) for all station pairs using Dijkstra's algorithm
    times_before, stops_before = functions.calculate_all_journeys(graph_time, graph_stops, station_map,
                                                                  functions.dijkstra, 'both')

    # Generate a Minimum Spanning Tree (MST) from the time-weighted graph to determine essential connections
    mst = functions.generate_mst(graph_time)
    # Identify which edges can be removed without disconnecting the graph, based on the MST
    edges_to_remove = functions.identify_edges_to_remove(graph_time, mst)

    # Output the list of connections that can be potentially closed
    functions.print_edges_to_remove(edges_to_remove, station_map)

    # Simulate the closure of identified edges in both the time and stops graphs
    functions.simulate_closure(graph_time, edges_to_remove)
    functions.simulate_closure(graph_stops, edges_to_remove)

    # Calculate new journey metrics (times and stops) after the simulated closures
    times_after, stops_after = functions.calculate_all_journeys(graph_time, graph_stops, station_map,
                                                                functions.dijkstra, 'both')

    # Plot and compare histograms before and after the simulated closures
    # Histograms provide a visual representation of journey times and the number of stops distribution
    functions.plot_multiple_histograms(times_before, times_after, 'Journey Times', 'Time (minutes)')
    functions.plot_multiple_histograms(stops_before, stops_after, 'Number of Stops', 'Stops', plot_type='range')


# Ensure that the main function is called only when the script is executed directly (not when imported)
if __name__ == "__main__":
    main()
