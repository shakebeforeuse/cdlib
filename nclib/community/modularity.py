import community as louvain_modularity
import leidenalg
from collections import defaultdict
import networkx as nx
import igraph as ig
from nclib import NodeClustering
from nclib.utils import convert_graph_formats


def louvain(g, weight='weight', resolution=1., randomize=False):
    """

    :param g:
    :param weight:
    :param resolution:
    :param randomize:
    :return:
    """

    g = convert_graph_formats(g, nx.Graph)

    coms = louvain_modularity.best_partition(g, weight=weight, resolution=resolution, randomize=randomize)

    # Reshaping the results
    coms_to_node = defaultdict(list)
    for n, c in coms.items():
        coms_to_node[c].append(n)

    coms_louvain = [tuple(c) for c in coms_to_node.values()]
    return NodeClustering(coms_louvain, g, "Louvain", method_parameters={"weight": weight, "resolution": resolution,
                                                                         "randomize": randomize})


def leiden(g, initial_membership=None, weights=None):
    """

    :param initial_membership:
    :param weights:
    :param g:
    :return:
    """

    g = convert_graph_formats(g, ig.Graph)

    part = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition,
                                    initial_membership=initial_membership, weights=weights
                                    )
    coms = [g.vs[x]['name'] for x in part]
    return NodeClustering(coms, g, "Leiden", method_parameters={"initial_membership": initial_membership,
                                                                "weights": weights})


def rb_pots(g, initial_membership=None, weights=None, resolution_parameter=1):
    """

    Reichardt, J., & Bornholdt, S. (2006).
    Statistical mechanics of community detection.
    Physical Review E, 74(1), 016110. 10.1103/PhysRevE.74.016110

    Leicht, E. A., & Newman, M. E. J. (2008).
    Community Structure in Directed Networks.
    Physical Review Letters, 100(11), 118703. 10.1103/PhysRevLett.100.118703

    :param initial_membership:
    :param weights:
    :param resolution_parameter:
    :param g:
    :return:
    """

    g = convert_graph_formats(g, ig.Graph)

    part = leidenalg.find_partition(g, leidenalg.RBConfigurationVertexPartition,
                                    resolution_parameter=resolution_parameter,
                                    initial_membership=initial_membership, weights=weights)
    coms = [g.vs[x]['name'] for x in part]
    return NodeClustering(coms, g, "RB Pots", method_parameters={"initial_membership": initial_membership,
                                                                 "weights": weights,
                                                                 "resolution_parameter": resolution_parameter})


def rber_pots(g, initial_membership=None, weights=None, node_sizes=None, resolution_parameter=1):
    """

    Reichardt, J., & Bornholdt, S. (2006).
    Statistical mechanics of community detection.
    Physical Review E, 74(1), 016110. 10.1103/PhysRevE.74.016110

    :param initial_membership:
    :param weights:
    :param node_sizes:
    :param resolution_parameter:
    :param g:
    :return:
    """

    g = convert_graph_formats(g, ig.Graph)

    part = leidenalg.find_partition(g, leidenalg.RBERVertexPartition,
                                    resolution_parameter=resolution_parameter,
                                    initial_membership=initial_membership, weights=weights,
                                    node_sizes=node_sizes,
                                    )
    coms = [g.vs[x]['name'] for x in part]
    return NodeClustering(coms, g, "RBER Pots", method_parameters={"initial_membership": initial_membership,
                                                                   "weights": weights, "node_sizes": node_sizes,
                                                                   "resolution_parameter": resolution_parameter})


def cpm(g, initial_membership=None, weights=None, node_sizes=None, resolution_parameter=1):
    """

    Traag, V. A., Van Dooren, P., & Nesterov, Y. (2011).
    Narrow scope for resolution-limit-free community detection.
    Physical Review E, 84(1), 016114. 10.1103/PhysRevE.84.016114

    :param initial_membership:
    :param weights:
    :param node_sizes:
    :param resolution_parameter:
    :param g:
    :return:
    """

    g = convert_graph_formats(g, ig.Graph)

    part = leidenalg.find_partition(g, leidenalg.CPMVertexPartition,
                                    resolution_parameter=resolution_parameter, initial_membership=initial_membership,
                                    weights=weights, node_sizes=node_sizes,)
    coms = [g.vs[x]['name'] for x in part]
    return NodeClustering(coms, g, "CPM", method_parameters={"initial_membership": initial_membership,
                                                             "weights": weights, "node_sizes": node_sizes,
                                                             "resolution_parameter": resolution_parameter})


def significance_communities(g,  initial_membership=None, node_sizes=None):
    """

    Traag, V. A., Krings, G., & Van Dooren, P. (2013).
    Significant scales in community structure.
    Scientific Reports, 3, 2930. 10.1038/srep02930

    :param initial_membership:
    :param node_sizes:
    :param g:
    :return:
    """

    g = convert_graph_formats(g, ig.Graph)

    part = leidenalg.find_partition(g, leidenalg.SignificanceVertexPartition, initial_membership=initial_membership,
                                    node_sizes=node_sizes)
    coms = [g.vs[x]['name'] for x in part]
    return NodeClustering(coms, g, "Significance", method_parameters={"initial_membership": initial_membership,
                                                                      "node_sizes": node_sizes})


def surprise_communities(g, initial_membership=None, weights=None, node_sizes=None):
    """

    Traag, V. A., Aldecoa, R., & Delvenne, J.-C. (2015).
    Detecting communities using asymptotical surprise.
    Physical Review E, 92(2), 022816. 10.1103/PhysRevE.92.022816

    :param initial_membership:
    :param weights:
    :param node_sizes:
    :param g:
    :return:
    """

    g = convert_graph_formats(g, ig.Graph)

    part = leidenalg.find_partition(g, leidenalg.SurpriseVertexPartition, initial_membership=initial_membership,
                                    weights=weights, node_sizes=node_sizes)
    coms = [g.vs[x]['name'] for x in part]
    return NodeClustering(coms, g, "Surprise", method_parameters={"initial_membership": initial_membership,
                                                                  "weights": weights, "node_sizes": node_sizes})


def greedy_modularity(g, weight=None):
    """

    :param g:
    :param weight:
    :return:
    """

    g = convert_graph_formats(g, nx.Graph)

    gc = nx.algorithms.community.greedy_modularity_communities(g, weight)
    coms = [tuple(x) for x in gc]
    return NodeClustering(coms, g, "Greedy Modularity", method_parameters={"weight": weight})
