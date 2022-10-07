import csv

def load_csv(filename):
    nodes = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['edge_weight'] = int(row['edge_weight'])
            nodes.append(row)
    return nodes
    
