# src/graphics/generate.py

import json
import graphviz
import random

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def generate_architecture_diagram(json_data: dict, output_path="architecture_diagram"):
    # Crear el objeto Digraph de Graphviz
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

    # Añadir el dominio
    domain_id = json_data["domain"]["id"]
    domain_name = json_data["domain"]["name"]
    dot.node(domain_id, domain_name, shape="folder", style="filled,rounded", fillcolor="lightgray")

    # Sistemas y contenedores
    for system in json_data["systems"]:
        system_id = system["id"]
        system_name = system["name"]

        with dot.subgraph(name=f"cluster_{system_id}") as sub:
            sub.attr(label=system_name, style="filled", fillcolor="white")

            for container in system["containers"]:
                container_id = container["id"]
                container_name = container["name"]
                container_desc = container["description"]
                label = f"{container_name}\n({container_desc})"
                sub.node(container_id, label, fillcolor=random_color())

    # Relaciones
    for relation in json_data["relationships"]:
        source = relation["source"]
        target = relation["target"]
        description = relation["description"]
        dot.edge(source, target, xlabel=description, style="dashed", fontsize="10", labelfontsize="12")

    # Renderizar el diagrama
    dot.render(output_path, format="png", cleanup=True)
