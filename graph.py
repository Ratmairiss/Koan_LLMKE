from pyvis.network import Network

net_nodes_size = 55

net_config = f"""
{{
  "nodes": {{
    "shape": "circle",
    "widthConstraint": {{ "minimum": {net_nodes_size}, "maximum": {net_nodes_size} }},
    "heightConstraint": {{ "minimum": {net_nodes_size}, "maximum": {net_nodes_size} }},
    "font": {{ "size": 16, "color": "black" }}
  }},
  "edges": {{
    "width": 2,
    "font": {{ "size": 16, "color": "black" }},
    "color": "lightblue",
    "length": 160
  }}
}}
"""

info_text = """
    <div style="position:absolute; top:10px; right:10px; background:white; padding:5px; border:1px solid black; z-index:1000;">
    COLOR OF NODES: <br>
    <span style="
          display:inline-block;
          width:65px;
          height:65px;
          background:lightblue;
          color:black;
          text-align:center;
          line-height:60px;  
          font-weight:bold;
          margin-right:5px;
      ">Subject</span>
      <span style="
          display:inline-block;
          width:65px;
          height:65px;
          background:lightgreen;
          color:black;
          text-align:center;
          line-height:60px;  
          font-weight:bold;
          margin-right:5px;
      ">Object</span>
      <span style="
          display:inline-block;
          width:65px;
          height:65px;
          background:plum;
          color:black;
          text-align:center;
          line-height:60px;  
          font-weight:bold;
      ">S&O</span>
    </div>  
    """

subject_color = "lightblue"
object_color = "lightgreen"
predicate_color = "plum"

def truncate_label(label, max_len=10):
    if len(label) > max_len:
        return label[:max_len] + "…"
    return label

def add_info(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("</body>", info_text + "</body>")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def create_graph(triplets, path):

    net = Network(
        directed=True,
        height="600px",
        width="100%",
        notebook=True
    )

    net.set_options(net_config)

    seen_edges = set()
    added_nodes = {}

    for t in triplets:
        edge = (t['Subject'], t['Object'], t['Predicate'])
        if edge in seen_edges:
            continue

        if t['Subject'] in added_nodes:
            if added_nodes[t['Subject']]['type'] == 'object':
                net.nodes[added_nodes[t['Subject']]['id']]['color'] = predicate_color
                added_nodes[t['Subject']]['type'] = 'both'
        else:
            net.add_node(t['Subject'], label=truncate_label(t['Subject']), shape="circle", color=subject_color)
            added_nodes[t['Subject']] = {'id': len(net.nodes) - 1, 'type': 'subject'}

        if t['Object'] in added_nodes:
            if added_nodes[t['Object']]['type'] == 'subject':
                net.nodes[added_nodes[t['Object']]['id']]['color'] = predicate_color
                added_nodes[t['Object']]['type'] = 'both'
        else:
            net.add_node(t['Object'], label=truncate_label(t['Object']), shape="circle", color=object_color)
            added_nodes[t['Object']] = {'id': len(net.nodes) - 1, 'type': 'object'}

        net.add_edge(
            t['Subject'], t['Object'],
            title=t['Predicate'],
            label=truncate_label(t['Predicate'])
        )

        seen_edges.add(edge)

    net.show(path)
    add_info(path)
