import os
import json
import random
import graphviz
import time

def get_base_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def configure_graph():
    dot = graphviz.Digraph(format="png")
    dot.graph_attr.update(
        ranksep="1.5",
        nodesep="1.5",
        overlap="false",
        splines="ortho",
        fontsize="12"
    )
    dot.node_attr.update(
        shape="box",
        style="filled",
        fontname="Arial",
        fontsize="10"
    )
    return dot


def add_domain(dot, domain):
    dot.node(
        domain["id"],
        domain["name"],
        shape="folder",
        style="filled,rounded",
        fillcolor="lightgray"
    )


def add_systems_and_containers(dot, systems):
    for system in systems:
        system_id = system["id"]
        system_name = system["name"]

        with dot.subgraph(name=f"cluster_{system_id}") as sub:
            sub.attr(label=system_name, style="filled", fillcolor="white")

            for container in system["containers"]:
                label = f"{container['name']}\n({container['description']})"
                sub.node(container["id"], label, fillcolor=random_color())


def add_relationships(dot, relationships):
    for rel in relationships:
        dot.edge(
            rel["source"],
            rel["target"],
            xlabel=rel["description"],
            style="dashed",
            fontsize="10",
            labelfontsize="12"
***REMOVED***


def generate_architecture_diagram(data, output_file="architecture_diagram"):
    dot = configure_graph()
    add_domain(dot, data["domain"])
    add_systems_and_containers(dot, data["systems"])
    add_relationships(dot, data["relationships"])
    dot.render(output_file, format="png", cleanup=True)


def exe_file_generation():
    print("🔍 Starting architecture diagram generation...")
    output_file=f"architecture_diagram_{int(time.time())}"
    base_path = get_base_path()
    json_path = os.path.join(base_path, 'public', 'json', 'diagram.json')
    json_data = load_json_data(json_path)
    generate_architecture_diagram(json_data, output_file )
    print(f"""✅ Diagram generated successfully. with name : {output_file}""")
    return output_file

if __name__ == "__main__":
    exe_file_generation()
    
