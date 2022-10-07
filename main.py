# webserver imports
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# for filesystem access
import os
import shutil

# my code
from tests import test_all
from pathfinder import find_path
from util import load_csv

app = Flask(__name__)

# we store uploads in /tmp and clear them every time the app starts
UPLOAD_FOLDER = '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
os.mkdir(UPLOAD_FOLDER)

# we just keep track of the current run in this global var
# in production this would be db-backed
runs = []


# Index page, where we ask the user to upload a CSV file
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # boilerplate upload handling
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # if we succesfully upload a file, we redirect the user to submit arguments
            return redirect(url_for('run_pathfinder_for_file', name=filename))
    return '''
    <!doctype html>
    <title>PathFinder</title>
    <h1>Upload CSV Graph File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Here, upon having uploaded the file, we ask the user for arguments
@app.route('/uploads/<name>', methods=['GET', 'POST'])
def run_pathfinder_for_file(name):
    if request.method == 'POST':
        if request.form:
            runs.append({
                'filename': name,
                'args': request.form
            })
            runid = len(runs) - 1
            return redirect(url_for('show_results', runid=runid))

    # we do this here just to help confirm to the user the file has uploaded properly, not strictly neccesary
    edges = load_csv(f"{UPLOAD_FOLDER}/{name}")

    
    return f'''
    <!doctype html>
    <title>PathFinder</title>
    <h1>Find Shortest Path Length</h1>
    <p>Received {len(edges)} edges from {name}</p>
    <form method=post enctype=multipart/form-data>
        <label for=source>Source Node (example: "n1")</label>
        <input type=text name=source id=source required>
        <br/>
        <label for=target>Target Node (example: "n2")</label>
        <input type=text name=target id=target required>
        <br/>
        <label for=min_weight>Min Weight (example: "50")</label>
        <input type=number name=min_weight id=min_weight required>
        <br/>
        <label for=edge_labels>A space separated (no commas!) list of edge labels (example: "L1 L2")</label>
        <input type=text name=edge_labels id=edge_labels required>
        <br/>
        <input type=submit value=Find Shortest Path Length>
    </form>
    '''


# here we collect arguents
@app.route('/results/<runid>')
def show_results(runid):
    runid = int(runid)
    if runid >= len(runs):
        return redirect(url_for('upload_file'))
    
    run = runs[int(runid)]
    source = run['args']['source']
    target = run['args']['target']
    min_weight = int(run['args']['min_weight'])
    edge_labels = run['args']['edge_labels'].split()

    csv_edges = load_csv(f"{UPLOAD_FOLDER}/{run['filename']}")
    result = find_path(source=source, target=target, min_weight=min_weight, edge_labels=edge_labels, edges=csv_edges)    
    if result is None:
        return "No path found!"
    return str(result)





@app.route('/test')
def test():
    return test_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


