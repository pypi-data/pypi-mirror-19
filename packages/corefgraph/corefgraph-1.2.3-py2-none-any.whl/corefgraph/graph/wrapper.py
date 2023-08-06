# coding=utf-8
""" The layer of code between the graph library and the linguistic graph manage
"""


import networkx as nx
from collections import defaultdict
from corefgraph.constants import ID, FORM, LABEL, LEMMA

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class GraphWrapper():
    """ The wrapper to access al graph task
    """

    @classmethod
    def blank_graph(cls):
        """ Get a new empty graph
        :return: a empty graph
        """
        graph = nx.MultiDiGraph()
        # List of nodes by type
        graph.graph["index"] = defaultdict(list)
        return graph

    @classmethod
    def link(cls, graph, origin, target, link_type=None, weight=None, label=None, value=None):
        """Link two nodes of the graph. The origin and target parameters  may be nodes ID or nodes if their ids if they
        contains their ID in an attribute called "id".

        :param graph: The operation graph
        :param origin: node or node ID where the link is originated
        :param target: node or node ID where the link ended
        :param link_type: the type of the link
        :param weight: A weight for the link
        :param label: A label of the link for representation
        :param value: A value for the link
        :return:
        """
        key = link_type
        properties = {}
        if link_type:
            properties['type'] = link_type
        if value:
            properties['value'] = value
        if weight:
            properties['weight'] = weight
        if label:
            properties['label'] = label
        if isinstance(origin, dict):
            origin = origin[ID]
        if isinstance(target, dict):
            target = target[ID]
        relation = graph.add_edge(origin, target, key=key, attr_dict=properties)
        return relation

    @classmethod
    def new_node(cls, graph, node_type, node_id, **narg):
        """
        :param graph: The graph
        :param node_type: A type for the node
        :param node_id: A unique ID for identify the node in the graph
        :param narg: Any additional parameter for the graph
        :return: the ID used to store the node
        """
        graph.add_node(node_id)
        node = graph.node[node_id]
        graph.graph["index"][node_type].append(node)
        node[ID] = node_id
        node["type"] = node_type
        for name, value in narg.items():
            if value is not None:
                node[name] = value
        return node

    @classmethod
    def get_graph_property(cls, graph, property_name):
        """ Get a graph property value
        :param graph: The graph
        :param property_name: The name of the property
        :return: The value of the graph porperty
        """
        return graph.graph[property_name]

    @classmethod
    def set_graph_property(cls, graph, property_name, value):
        """ Set a graph property value
        :param graph: The graph
        :param property_name: The name of the property
        :param value: The value to store in the property
        :return: The value of the graph property
        """
        graph.graph[property_name] = value

    @classmethod
    def get_out_neighbour_by_relation_type(cls, graph, node, relation_type, key=False):
        """ Return the first out neighbour linked with the type type of relation.
        :param graph: The graph of the search
        :param node: The origin node of the edge
        :param relation_type: The type of the relation
        :param key: Return the relation keys
        :return: The target node or nothing
        """
        if key:
            for source, target, relation in graph.out_edges_iter(node[ID], keys=True):
                if relation == relation_type:
                    return graph.node[target], graph[node[ID]][target][relation_type]
        else:
            for source, target, relation in graph.out_edges_iter(node[ID], keys=True):
                if relation == relation_type:
                    return graph.node[target]
        return None

    @classmethod
    def get_out_neighbours_by_relation_type(cls, graph, node, relation_type, key=False):
        """ Return the out neighbours of node linked with a relation of type.
        :param graph: The graph of the search
        :param node: The origin node of the edge
        :param relation_type: The type of the relation
        :param key: Return the relation keys
        :return: A list of the target nodes or empty list.
        """
        if key:
            return [(graph.node[target], graph[node[ID]][target][relation_type])
                    for source, target, relation in graph.out_edges_iter(node[ID], keys=True)
                    if relation == relation_type]

        return [graph.node[target] for source, target, relation in graph.out_edges_iter(node[ID], keys=True)
                if relation == relation_type]

    @classmethod
    def get_in_neighbour_by_relation_type(cls, graph, node, relation_type, key=False):
        """ Return the first in neighbour linked with the type type of relation.
        :param graph: The graph of the search
        :param node: The target node of the edge
        :param relation_type: The type of the relation
        :param key: Return the relation keys
        :return: The origin node or nothing
        """
        if key:
            for source, target, key in graph.in_edges_iter(node[ID], keys=True):
                    if key == relation_type:
                        return graph.node[source], graph[source][node[ID]][relation_type]

        else:
            for source, target, key in graph.in_edges_iter(node[ID], keys=True):
                if key == relation_type:
                    return graph.node[source]
        return None

    @classmethod
    def get_in_neighbours_by_relation_type(cls, graph, node, relation_type, key=False):
        """ Return the in neighbours of node linked with a relation of type.
        :param graph: The graph of the search
        :param node: The target node of the edge
        :param relation_type: The type of the relation
        :param key: Return the relation keys
        :return: The origin node or nothing
        """
        if key:
            return [(graph.node[source], graph[source][node[ID]][relation_type])
                    for source, target, key in graph.in_edges_iter(node[ID], keys=True)
                    if key == relation_type]

        return [graph.node[source] for source, target, key in graph.in_edges_iter(node[ID], keys=True)
                if key == relation_type]

    @classmethod
    def get_node_by_id(cls, graph, node_id):
        """Get the node that correspond to the ID of a :param graph.

        :param graph: The graph of the node
        :param node_id: The unique ID that represent the node
        :return: the node
        """
        return graph.node[node_id]

    @classmethod
    def get_all_node_by_type(cls, graph, node_type):
        """ Get all the nodes of a type from a graph.
        :param graph: The graph of the nodes
        :param node_type: The type of the nodes
        :return: The list of nodes
        """
        return graph.graph["index"][node_type]

    @classmethod
    def show_graph(cls, graph):
        """ Prints graph using grahpviz.
        :param graph: The graph to output.
        """

        import matplotlib.pyplot as plt

        s = graph.subgraph(graph)

        deg = graph.degree()
        to_remove = [n for n in deg if deg[n] == 0]
        s.remove_nodes_from(to_remove)
        #pos = nx.graphviz_layout(s, prog='dot')
        labels = dict(
            ((n, d['label'].decode("utf-8")) for n, d in s.nodes(data=True))
        )
        edge_labels = dict([((u, v), d["type"]) for u, v, d in s.edges(data=True)])
        nx.draw(s, labels=labels, edges_labels=edge_labels)
        #nx.draw(s, pos, labels=labels, edges_labels=edge_labels)
        plt.show()
        plt.savefig("out.png")

    @classmethod
    def show_sentence(cls, graph, root, node_type=None):
        """ Prints sentence using grahpviz.
        :param graph: The graph to output.
        """

        import pygraphviz

        nodes = graph.neighbors(root[ID])
        nodes.append(root[ID])
        if node_type:
            s = graph.subgraph(
                node for node in nodes if graph.node[node]["type"] == node_type)
        else:
            s = graph.subgraph(nodes)

        deg = s.degree()
        to_remove = [n for n in deg if deg[n] == 0]
        s.remove_nodes_from(to_remove)
        for node in nodes:
            graph.node[node][LABEL] = graph.node[node][LABEL].decode("utf-8")
            graph.node[node][FORM] = graph.node[node].get(FORM).decode("utf-8")
            graph.node[node][LEMMA] = graph.node[node].get(FORM).decode("utf-8")

        layout = nx.graphviz_layout(s, prog='dot', root=root[ID])
        labels = dict(
            ((n, d['label']) for n, d in s.nodes(data=True))
        )

        plt.clf()
        nx.draw_networkx(s, layout, labels=labels, node_size=0, width=0.4,)

        edge_chart = (
            ("ROOT", 'b'),
            ("order", 'b'),
            ("named_refers", 'g'),
            ("dependency", 'r'),
            ('word', 'c'),
            ("syntactic", 'm'),
            ("gold_mention", 'y'),
            ("refers", 'k'),
            ("is_head", "#ff8000"),
            ("is_head_word", "#ffbf00"))

        for edge_type, edge_color in edge_chart:
            edges = []
            edge_labels = {}
            for u, v, d in s.edges(data=True):
                if d['type'] == edge_type:
                    edges.append((u, v))
                    edge_labels[(u, v)] = d.get("value", "")
            nx.draw_networkx_edges(s, layout, edgelist=edges, edge_color=edge_color, label=edge_type)
            nx.draw_networkx_edge_labels(s, layout, edgelist=edges, edge_labels=edge_labels, label_pos=0.3, rotate=False)
        plt.legend()
        plt.show()
        #import time
        #plt.savefig("sentences/{0}_{1}out.png".format(time.time() + 0, root["id"]))

    @classmethod
    def unlink(cls, graph, origin, target):
        """  Remove all the edges between :param origin: and :param target in a :param graph.
        """
        for edge in graph.edge(origin, target, all_edges=True):
            graph.remove_edge(edge)

    @classmethod
    def remove(cls, graph, element):
        """ Remove a element from a graph.
        :param graph: The graph
        :param element:
        :return:
        """
        graph.remove_node(element[ID])

    # @classmethod
    # def get_gephi(cls, graph):
    #         nx.write_gexf(graph,)
