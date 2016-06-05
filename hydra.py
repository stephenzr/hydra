import os
from flask import Flask, render_template, request, jsonify
from org import OrgGraph

app =       Flask(__name__)
org_chart = OrgGraph(os.environ.get('ORG_INPUT'))

@app.route("/get_dimension",methods=['POST'])
def get_dimension():
    data = request.json['data']
    dimension = data['dimension']
    nodes = org_chart.get_nodes_for_dimension(dimension)
    edges = org_chart.get_edges_for_dimension(dimension)
    return jsonify( nodes=nodes.values(), edges=edges.values())

@app.route('/')
def default_route():
    dimensions = org_chart.nodes.keys()
    nodes = org_chart.get_division_nodes().values()
    edges = org_chart.get_division_edges().values()

    return render_template('hydra.html',
                           dimensions=dimensions,
                           nodes=nodes,
                           edges=edges)

if __name__ == '__main__':
    app.run()
