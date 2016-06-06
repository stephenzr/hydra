import os
from flask import Flask, render_template, request, jsonify
from org import OrgGraph

app =       Flask(__name__)
org_chart = OrgGraph(os.environ.get('ORG_INPUT'))

@app.route("/get_dimension",methods=['POST'])
def get_dimension():
    data      = request.json['data']
    dimension = data['dimension']
    nodes     = org_chart.get_nodes_for_dimension(dimension)
    edges     = org_chart.get_edges_for_dimension(dimension)
    options   = org_chart.get_options(dimension, len(nodes), len(edges))
    print "return dimension %s with %d nodes, %d edges" % ( dimension, len(nodes), len(edges))
    return jsonify( nodes=nodes, edges=edges, dimension=dimension,options=options)

@app.route('/')
def default_route():
    dimensions = org_chart.nodes.keys()
    nodes      = org_chart.get_default_nodes()
    edges      = org_chart.get_default_edges()
    options    = org_chart.get_division_options()


    return render_template('hydra.html',
                           dimensions=dimensions,
                           dimension={'data':org_chart.get_default_dimension()},
                           nodes=nodes,
                           edges=edges,
                           options=options)

if __name__ == '__main__':
    app.run()
