import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
from datetime import datetime, timedelta


class TemporalDiGraph():
    
    def __init__(self, df):
        df.columns = ['source', 'target', 'rating', 'time']
        df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')
        df = df.set_index('time')
        self.df = df

    def get_df(self, period=None):
        if period is None:
            return self.df
        else:
            return self.df.loc[period]
    
    def get_DiGraph(self, period=None):
        
        this_df = self.get_df(period)
        
        G = nx.MultiDiGraph()
        edges = [(t.source, t.target, float(t.rating))
                 for t in this_df.itertuples()]
        G.add_weighted_edges_from(edges)
        return G
    
    def get_all_months(self):
        return self.df.index.to_period('M').unique().to_list()

        
    def draw_network(self, period=None):
        
        def get_node_size(series, userid):
            try:
                count = series[userid]
                return 100 * count
            except:
                return 100


        def get_node_colour(series, userid):
            try:
                average = series[userid]
                return np.interp(average, (-10, 10), (0, 1))
            except:
                return 0.5
        
        this_df = self.get_df(period)
        G = self.get_DiGraph(period)

        rating_count = this_df.groupby('target').rating.count()
        rating_avg = this_df.groupby('target').rating.mean()
        
        plt.figure(figsize=(10, 10))
        plt.title(
            "Bitcoin OTC Marketplace Trust Network - {}".format(str(period)), fontsize=18)

        pos = nx.spring_layout(G, k=0.25)
        node_sizes = [get_node_size(rating_count, n) for n in G]
        node_colours = [get_node_colour(rating_avg, n) for n in G]
        
        nc = nx.draw_networkx_nodes(
            G, pos, nodelist=G.nodes(), node_size=node_sizes, linewidths=1.5,
            node_color=node_colours, cmap=plt.cm.RdYlGn, alpha=0.9
        )
        ec = nx.draw_networkx_edges(G, pos, arrows=True, alpha=0.25)
        ax = plt.axis('off')
        plt.show()
