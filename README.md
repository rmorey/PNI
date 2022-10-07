
# My Solution
Use Dijksta's algorithm to find the shortest path between source and target, filtering edges based on provided arguments. Runing live on Replit [here](https://pni-coding-assignment.rmorey.repl.co/).

## Structure
- `main.py`: This is the Flask webserver which provides an UI to my implementation
- `util.py`: Contains just one function `load_csv` which loads the csv from disk into memory (and casts `min_weight` to `int`)
- `tests.py`: Contains a basic suite of tests, on both some toy data, as well as the provided sample data
- `pathfinder.py`: The main event. contains `find_path` and a helper function, which implement dijkstra's algorithm to find a shortest path between source and target, filtered by the given args

## Running 
Running live here: https://pni-coding-assignment.rmorey.repl.co/  Navigate to the root in order to upload a file, and select args, or navigate to `/test` to run the test suite.

You can also fork this, and just hit Run on Replit (or download, use poetry to install libs, and run the flask app)

## Performance
Canonically, Dijsktra's Alg has time complexity of O(E logV), which I definitely didn't just Google. Sounds pretty good. My particular implementaiton could be improved in the following ways:

- Use somthing more effecient than a Python dict for `tentative_distances` this structure is key to the algorithm, and we access it a lot. dict lookups in Python are a hashmap, and therefore O(1) but because we need to find the item out with the least distance, we end up sorting the dictionary a lot, and that's bad. I think we could use a min heap for this, which I think would be better. 
- Ensure we're not reading the CSV data from disk uncessarily. Currently we do this twice, the first time just to give the user the number of edges loaded before they submit args. We should be doing this exactly once, and caching the result. Done here as a quick nicety.

## Other Improvements
The web server is generally a little flaky and sensitive to correctly formatted inputs. Would be inmportant to add much more robust input handling/error handling/input sanitizing. The hardcoded HTML strigns should be proper Jinja templates. Also, it's ugly!


# Problem Statement
Given a graph / network with nodes and weighted & labeled edges, we'd like to build an app that takes as input a source node + a target node + minimum edge weight + set of edge labels, and calculates the shortest path from source node to target node, where the path consists of edges with the specified minimum weight and of specified labels.

Example input:
source: 'n1'
target: 'n2'
min_weight: 50
edge_labels: ['L1', 'L2', 'L2']

Example output:
2 (=path length, assuming the shortest path from n1 to n2 within these constraints goes thru one intermediate node)

Small sample input file is attached. Every row corresponds to an edge (from node, to node, weight and label). Actual graph size used for testing the solution will be larger (tens of thousands of nodes and millions of edges).

Make best effort to:
1. understand the requirements, and make most reasonable assumptions wherever there's ambiguity
2. optimize time and space complexity of the solution
3. make interface as clear as possible

Use any programming language, and any basic libraries for loading/processing data. However do not use graph algo libraries.

Bonus points: build a web app with a simple UI that takes an input file + parameters and prints out the output.


## my misc notes

allowed(edge) = (edge.weight >= min_weight) && (edge.label in edge_labels)

My questions:
- is min_weight *per edge* or cumulative ? (confirms)
  - Answer: per edge
- Is the required output the *path itself* (as indicated in problem statement) or the *path length* only (as indicated by the Example output)
  - Answer: path length only
- Is there a meaning, in the example input, to 'L2' being repeated? 
    - Assumption: no (confirmed)


Steps: 
    - import CSV
    - use dijkstra's alg, filtering edges which meet requirements

References:
    - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    - https://docs.python.org/3/library/csv.html