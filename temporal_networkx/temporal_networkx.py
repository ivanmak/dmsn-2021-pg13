import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
from datetime import datetime, timedelta

# Includes REV2 algorithm from https://github.com/horizonly/Rev2-model
# @inproceedings{kumar2018rev2, title={Rev2: Fraudulent user prediction in rating platforms},
# author={Kumar, Srijan and Hooi, Bryan and Makhija, Disha and Kumar, Mohit and Faloutsos, Christos and Subrahmanian, VS},
# booktitle={Proceedings of the Eleventh ACM International Conference on Web Search and Data Mining},
# pages={333--341}, year={2018}, 321、 organization={ACM} }

class TemporalDiGraph():
    
    def __init__(self, df):
        '''
        This class takes the Pandas data frame created by the 
        read_csv() method with the option header=None.
        
        Parameters:
        df (pandas.DataFrame): A Pandas Data Frame containing the Bitcoin OTC data set
        '''
        df.columns = ['source', 'target', 'rating', 'time']
        df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')
        df = df.set_index('time')
        self.df = df

    def get_df(self, period=None, period_end=None):
        '''
        This method slices the data frame to the given period.
        
        Parameters:
        period (str): A string of the starting month in the format YYYY-MM to slice the data frame
        period_end (str): A string in the ending month format YYYY-MM to slice the data frame
        
        Returns:
        pandas.DataFrame: The sliced data frame
        '''
        if period is None:
            return self.df
        
        if period is not None and period_end is None:
            return self.df.loc[period]

        return self.df.loc[period:period_end]
    
    def get_DiGraph(self, period=None, period_end=None, run_REV2=False):
        '''
        This method creates a NetworkX MultiDiGraph sliced to the given period.
        
        If run_REV2 is set to True, it will calculate node fairness, node goodness,
        and edge fairness using REV2 algorithm from https://github.com/horizonly/Rev2-model
        
        Parameters:
        period (str): A string of the starting month in the format YYYY-MM to slice the data
        period_end (str): A string in the ending month format YYYY-MM to slice the data
        run_REV2 (boolean): Whether the fairness and goodness scores should be calculated
        
        Returns:
        networkx.MultiDiGraph: A directed graph representing the given period.
        '''
        this_df = self.get_df(period, period_end)
        
        G = nx.MultiDiGraph()
        edges = [(t.source, t.target, G.new_edge_key(t.source, t.target), {'weight': float(t.rating)})
                 for t in this_df.itertuples()]
        G.add_edges_from(edges)
        for node in G.nodes:
            G.nodes[node]['fairness'] = 0.0
            G.nodes[node]['goodness'] = 0.0
        
        if run_REV2:
            gamma = 0.01
            nodes = G.nodes()
            edges = G.edges(keys=True, data=True)
            iterations = 100
                
            i = 0
            while i < iterations:
                du, dp, dr = 0, 0, 0
                
                # Goodness of Nodes
                for node in nodes:
                    inedges = G.in_edges(node, keys=True, data=True)
                    ftotal = 0.0
                    gtotal = 0.0
                    for edge in inedges:
                        gtotal = gtotal + G.nodes[edge[0]]['fairness'] * edge[3]['weight']
                        ftotal = ftotal + 1.0

                    if ftotal > 0.0:
                        mean_rating_fairness = gtotal / ftotal
                    else:
                        mean_rating_fairness = 0.0

                    x = mean_rating_fairness

                    if x < -1.0:
                        x = -1.0
                    if x > 1.0:
                        x = 1.0

                    dp += abs(G.nodes[node]["goodness"] - x)
                    G.nodes[node]["goodness"] = x
                
                # Fairness of Edges
                for edge in edges:
                    rating_distance = 1 - \
                        (abs(edge[3]["weight"] - G.nodes[edge[1]]["goodness"])/2.0)

                    user_fairness = G.nodes[edge[0]]["fairness"]
                    ee = (edge[0], edge[1])
                    x = (gamma * rating_distance + gamma * user_fairness)/(gamma * 2)

                    if x < 0.00:
                        x = 0.0
                    if x > 1.0:
                        x = 1.0

                    if 'fairness' in edge[3]:
                        dr = dr + abs(edge[3]["fairness"] - x)
                    else:
                        dr = dr + abs(0.0 - x)

                    G.edges[edge[0], edge[1], edge[2]]["fairness"] = x
                
                # Fairness of Nodes
                for node in nodes:
                    outedges = G.out_edges(node, data=True)

                    f = 0.0
                    rating_fairness = []
                    for edge in outedges:
                        rating_fairness.append(edge[2]["fairness"])

                    mean_rating_fairness = 0
                    if len(rating_fairness) > 0:
                        mean_rating_fairness = np.mean(rating_fairness)

                    x = mean_rating_fairness  # *(kl_timestamp)
                    if x < 0.00:
                        x = 0.0
                    if x > 1.0:
                        x = 1.0

                    du = du + abs(G.nodes[node]["fairness"] - x)
                    G.nodes[node]["fairness"] = x
                i = i + 1
                if du < 0.01 and dp < 0.01 and dr < 0.01:
                    break

        return G
    
    def get_all_months(self):
        '''
        This method returns a list of months that are covered by the data set
        
        Returns:
        list: A list of months that are covered by the data set.
        '''
        return self.df.index.to_period('M').unique().to_list()

    def draw_network(self, period=None, period_end=None,
                     graph_type='average', save_filename=None):
        '''
        This methods draws a graph representation of the trust network of the given
        period. By default it will display the graph on-screen.
        
        If the parameter save_filename is provided, the method will instead save the 
        graph to local filesystem of the provided file name.
        
        If graph type is 'average', the node size will be proportional to the number of
        in-edges of the nodes, and the node colour will be relative to the average rating
        received by the nodes on a Red-Amber-Green scale.
        
        If graph type is 'rev2', the node size will be proportional to the REV2 fairness
        score of the nodes, and the node colour will be relative to the REV2 goodness score
        of the nodes on a Red-Amber-Green scale.
        
        Parameters:
        period (str): A string of the starting month in the format YYYY-MM to slice the data
        period_end (str): A string in the ending month format YYYY-MM to slice the data
        graph_type (str): Either 'average' or 'rev2', defaults to 'average'
        save_filename (str): File name to save the graph
        
        Returns:
        None - It will either display or save the graph.
        '''
        def get_node_size(input=0, rev2=False):
            if rev2:
                if input == 0:
                    return 100
                
                if input > 0:
                    return 100 * np.interp(input, (0, 1), (1.0, 5.0))
                
                if input < 0:
                    return 100 * np.interp(input, (-1, 0), (0.5, 1.0))
                
            else:
                if input > 0:
                    return 100 * input
                else:
                    return 50
        def get_node_colour(ratings, rev2=False):
            if rev2:
                try:
                    return np.interp(ratings, (-1, 1), (0, 1))
                except:
                    return 0.5
            else:
                try:
                    average_rating=0
                    if len(ratings) > 0:
                        average_rating = np.average(ratings)
                    return np.interp(average_rating, (-10, 10), (0, 1))
                except:
                    return 0.5
        
        graph_types = ['average','rev2']
        
        if graph_type is None:
            graph_type = 'average'
            
        if graph_type not in graph_types:
            raise RuntimeError('graph_type must be one of the following: {}'.format(', '.join(graph_types)))
        
        run_REV2 = False
        if graph_type == 'rev2':
            run_REV2 = True
            
        G = self.get_DiGraph(period, period_end, run_REV2=run_REV2)
        
        if period is None and period_end is None:
            title = "Bitcoin OTC Marketplace Trust Network - Whole Data Set"
        elif period is not None and period_end is None:
            title = "Bitcoin OTC Marketplace Trust Network - {}".format(str(period))
        else:
            title = "Bitcoin OTC Marketplace Trust Network - {} to {}".format(str(period), str(period_end))
                
        plt.figure(figsize=(10, 10))
        plt.title(title, fontsize=18)

        pos = nx.spring_layout(G, k=0.25)

        if graph_type == 'average':
            node_sizes = [get_node_size(len(G.in_edges(n))) for n in G]
            node_colours = [get_node_colour([x[2]['weight'] for x in G.in_edges(n, data=True)]) for n in G]
        
        if graph_type == 'rev2':
            node_sizes = [get_node_size(n[1]['fairness'], rev2=True) for n in G.nodes(data=True)]
            node_colours = [get_node_colour(n[1]['goodness'], rev2=True) for n in G.nodes(data=True)]
        
        nc = nx.draw_networkx_nodes(
            G, pos, nodelist=G.nodes(), node_size=node_sizes, linewidths=1.5,
            node_color=node_colours, cmap=plt.cm.RdYlGn, alpha=0.9
        )
        ec = nx.draw_networkx_edges(G, pos, arrows=True, alpha=0.25)
        ax = plt.axis('off')
        
        if save_filename is None:
            plt.show()
        else:
            plt.savefig(save_filename, facecolor='white', transparent=False)


