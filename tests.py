from util import load_csv
from pathfinder import find_path

def test_all():

    # some test cases, using both a dummy graph of 3 nodes, as well as the provided test data
    
    csv_edges = load_csv('sample_graph.csv')
    
    test_edges = [{'from':'n1','to':'n2','edge_weight':1,'edge_label':'L1'},
              {'from':'n1','to':'n3','edge_weight':1,'edge_label':'L1'},
              {'from':'n2','to':'n3','edge_weight':1,'edge_label':'L1'},
              {'from':'n2','to':'n5','edge_weight':1,'edge_label':'L1'},
            ]

    test_cases = [
        (dict(source='n1', target='n3', min_weight=1, edge_labels=['L1', 'L2', 'L3'], edges=test_edges), 1),
        (dict(source='n1', target='n5',min_weight=1, edge_labels = ['L1', 'L2', 'L3'], edges=test_edges), 2),
        (dict(source='n1', target='n5',min_weight=1, edge_labels = ['L3'], edges=test_edges), None),
        (dict(source='n372', target='n357',min_weight=1, edge_labels = ['L5'], edges=csv_edges), 2),
        (dict(source='n1', target='n1', min_weight=1, edge_labels=['L1', 'L2', 'L3'], edges=test_edges), 0),
        (dict(source='n863', target='n992',min_weight=1, edge_labels = ['L68','L47'], edges=csv_edges), 2),
        (dict(source='n1_garbage', target='n5',min_weight=1, edge_labels = ['L3'], edges=test_edges), None),
    ]
                

    for test_case in test_cases:
        assert(find_path(**test_case[0]) == test_case[1])
            

    return "tests passed!"