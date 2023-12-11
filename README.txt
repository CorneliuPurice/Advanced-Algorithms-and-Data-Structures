# London Underground Route Planner

This project contains a set of Python scripts and data files designed to model and analyze the London Underground tube system. The main functionality includes calculating the shortest journey times and the number of stops between stations, as well as simulating station closures and analyzing their impact on the network.

## Files Description

- `adjacency_list_graph.py`: Defines a graph data structure using adjacency lists.
- `adjacency_matrix_graph.py`: Defines a graph data structure using adjacency matrices.
- `bfs.py`: Implements the Breadth-First Search algorithm for traversing or searching graph data structures.
- `dijkstra.py`: Implements Dijkstra's algorithm for finding the shortest paths between nodes in a graph.
- `disjoint_set_forest.py`: Provides an implementation of a disjoint-set data structure also known as a union-find data structure.
- `dll_sentinel.py`: Implements a doubly linked list with sentinel nodes.
- `fifo_queue.py`: Implements a First In, First Out (FIFO) queue data structure.
- `functions.py`: Contains utility functions used across various tasks, including data loading, graph creation, and pathfinding.
- `heap_priority_queue.py`: Implements a priority queue using a heap data structure.
- `heap.py`: Provides basic heap operations used within the priority queue implementation.
- `London Underground data.xlsx`: Contains the dataset of the London Underground network including stations and journey times.
- `merge_sort.py`: Implements the merge sort algorithm for sorting data.
- `min_heap_priority_queue.py`: Implements a minimum heap priority queue.
- `mst.py`: Contains the implementation of Kruskal's algorithm to find the minimum spanning tree of a graph.
- `print_path.py`: Utility script for printing the path between two nodes in a graph.
- `single_source_shortest_paths.py`: General framework for single-source shortest paths algorithms.
- `task_1.py`: Executable script for calculating shortest journey durations using Dijkstra's algorithm.
- `task_2.py`: Executable script for calculating the shortest path in terms of stops using Dijkstra's algorithm.
- `task_3.py`: Executable script for calculating the shortest path in terms of stops using BFS.
- `task_4.py`: Executable script for simulating station closures and analyzing the impact on journey times and stops.

## Usage

Each task (`task_1.py`, `task_2.py`, `task_3.py`, and `task_4.py`) can be run independently to perform specific analyses.
All functions are stored in functions.py file.

## Dependencies

Make sure all dependencies are installed and the dataset file (London Underground data.xlsx) is present in the same directory as the scripts.

The project relies on the following Python libraries:

    'pandas': For data manipulation and analysis.
    'matplotlib': For generating histograms and other graphical data representations.
