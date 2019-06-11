import unittest
import networkx as nx
import numpy as np
from cdlib.algorithms import louvain, label_propagation
from cdlib import evaluation


class PartitionsComparisonsTests(unittest.TestCase):

    def test_nmi(self):

        g = nx.karate_club_graph()
        louvain_communities = louvain(g)
        lp_communities = label_propagation(g)

        score = evaluation.normalized_mutual_information(louvain_communities, lp_communities)

        self.assertLessEqual(score, 1)
        self.assertGreaterEqual(score, 0)

    def test_onmi(self):

        g = nx.karate_club_graph()
        lp_communities = label_propagation(g)
        lp2_communities = label_propagation(g)

        score = evaluation.overlapping_normalized_mutual_information_MGH(lp2_communities, lp_communities)

        self.assertLessEqual(score, 1)
        self.assertGreaterEqual(score, 0)

        score = evaluation.overlapping_normalized_mutual_information_LFK(lp2_communities, lp_communities)

        self.assertLessEqual(score, 1)
        self.assertGreaterEqual(score, 0)

    def test_omega(self):

        g = nx.karate_club_graph()
        lp_communities = label_propagation(g)
        louvain_communities = louvain(g)

        score = evaluation.omega(louvain_communities, lp_communities)

        self.assertLessEqual(score, 1)
        self.assertGreaterEqual(score, 0)

    def test_f1(self):

        g = nx.karate_club_graph()
        lp_communities = label_propagation(g)
        louvain_communities = louvain(g)

        score = evaluation.f1(louvain_communities, lp_communities)

        self.assertIsInstance(score, evaluation.MatchingResult)

    def test_nf1(self):

        g = nx.karate_club_graph()
        lp_communities = label_propagation(g)
        louvain_communities = louvain(g)

        score = evaluation.nf1(louvain_communities, lp_communities)

        self.assertLessEqual(score, 1)
        self.assertGreaterEqual(score, 0)

    def test_adjusted_rand(self):
        g = nx.karate_club_graph()
        lp_communities = label_propagation(g)
        louvain_communities = louvain(g)

        score = evaluation.adjusted_rand_index(louvain_communities, lp_communities)

        self.assertLessEqual(score, 1)
        self.assertGreaterEqual(score, 0)

    def test_adjusted_mutual(self):
        g = nx.karate_club_graph()
        lp_communities = label_propagation(g)
        louvain_communities = louvain(g)

        score = evaluation.adjusted_mutual_information(louvain_communities, lp_communities)

        self.assertLessEqual(score, 1)
        self.assertGreaterEqual(score, 0)

    def test_variation_of_information(self):
        g = nx.karate_club_graph()
        lp_communities = label_propagation(g)
        louvain_communities = louvain(g)

        score = evaluation.variation_of_information(louvain_communities, lp_communities)

        self.assertLessEqual(score, np.log(g.number_of_nodes()))
        self.assertGreaterEqual(score, 0)
