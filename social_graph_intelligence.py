
import networkx as nx
import random
from datetime import datetime
import json

class SocialGraphIntelligence:
    def __init__(self):
        self.graph = nx.Graph()
        self.node_colors = {}
        self.risk_thresholds = {
            'safe': 30,
            'low': 50,
            'medium': 70,
            'high': 85
        }

    def add_profile(self, username, profile_data=None):
        """Add a profile node to the graph"""
        if profile_data is None:
            profile_data = {}
        self.graph.add_node(username, **profile_data)
        return username

    def add_connection(self, from_user, to_user, connection_type='follow', weight=1):
        """Add an edge between two profiles"""
        if not self.graph.has_node(from_user):
            self.add_profile(from_user)
        if not self.graph.has_node(to_user):
            self.add_profile(to_user)
        
        if self.graph.has_edge(from_user, to_user):
            # Update existing edge
            self.graph[from_user][to_user]['weight'] += weight
            if connection_type not in self.graph[from_user][to_user]['types']:
                self.graph[from_user][to_user]['types'].append(connection_type)
        else:
            # Add new edge
            self.graph.add_edge(from_user, to_user, 
                               weight=weight, 
                               types=[connection_type])
        return True

    def calculate_profile_risk(self, username):
        """Calculate risk score for a single profile"""
        if username not in self.graph:
            return 0
        
        score = 0
        node_data = self.graph.nodes[username]
        
        # High following count
        if node_data.get('following', 0) > 5000:
            score += 20
        
        # Low engagement
        if node_data.get('followers', 0) > 0:
            engagement_ratio = (node_data.get('total_likes', 0) + 
                               node_data.get('total_comments', 0)) / node_data.get('followers', 1)
            if engagement_ratio < 0.005:  # Less than 0.5% engagement
                score += 15
        
        # Check neighbors
        neighbors = list(self.graph.neighbors(username))
        high_risk_neighbors = 0
        for neighbor in neighbors:
            neighbor_risk = self._calculate_single_node_risk(neighbor)
            if neighbor_risk >= 50:
                high_risk_neighbors += 1
        
        if high_risk_neighbors > 0:
            score += (high_risk_neighbors / len(neighbors)) * 30
        
        # Similarity indicators
        similar_usernames = node_data.get('similar_usernames', 0)
        if similar_usernames >= 3:
            score += 15
        
        duplicate_pic = node_data.get('duplicate_profile_pic', False)
        if duplicate_pic:
            score += 20
        
        return min(score, 100)

    def _calculate_single_node_risk(self, username):
        """Helper for individual node risk"""
        node_data = self.graph.nodes.get(username, {})
        score = 0
        
        if node_data.get('following', 0) > 5000:
            score += 25
        if node_data.get('is_bot', False):
            score += 40
        if node_data.get('duplicate_profile_pic', False):
            score += 20
        
        return score

    def detect_communities(self):
        """Detect communities using Louvain method"""
        from networkx.algorithms import community
        try:
            communities_generator = community.louvain_communities(self.graph, resolution=1.0)
            return list(communities_generator)
        except Exception as e:
            # Fallback to connected components
            return list(nx.connected_components(self.graph))

    def detect_bot_clusters(self, communities=None):
        """Detect clusters likely to be bot networks"""
        if communities is None:
            communities = self.detect_communities()
        
        bot_clusters = []
        for i, community in enumerate(communities):
            community_risk = self._calculate_community_risk(community)
            if community_risk >= 50:
                bot_clusters.append({
                    'cluster_id': i,
                    'size': len(community),
                    'members': list(community),
                    'risk_score': community_risk,
                    'threat_level': self._get_threat_level(community_risk)
                })
        
        return bot_clusters

    def _calculate_community_risk(self, community):
        """Calculate risk score for a community"""
        if not community:
            return 0
        
        total_risk = 0
        high_risk_members = 0
        
        for member in community:
            risk = self.calculate_profile_risk(member)
            total_risk += risk
            if risk >= 50:
                high_risk_members += 1
        
        avg_risk = total_risk / len(community)
        
        # Bonus for large high-risk communities
        if high_risk_members >= 3:
            avg_risk += 20
        
        return min(avg_risk, 100)

    def _get_threat_level(self, risk_score):
        """Get threat level based on risk score"""
        if risk_score < self.risk_thresholds['safe']:
            return 'Safe'
        elif risk_score < self.risk_thresholds['low']:
            return 'Low Risk'
        elif risk_score < self.risk_thresholds['medium']:
            return 'Medium Risk'
        elif risk_score < self.risk_thresholds['high']:
            return 'High Risk'
        else:
            return 'Critical Risk'

    def get_graph_json(self):
        """Export graph to JSON for visualization"""
        nodes = []
        for node in self.graph.nodes(data=True):
            risk = self.calculate_profile_risk(node[0])
            color = '#22c55e'  # Green for safe
            if risk >= 85:
                color = '#ef4444'  # Red for critical
            elif risk >= 70:
                color = '#f97316'  # Orange for high
            elif risk >= 50:
                color = '#eab308'  # Yellow for medium
            elif risk >= 30:
                color = '#84cc16'  # Light green for low
            
            nodes.append({
                'id': node[0],
                'label': node[0],
                'risk': risk,
                'color': color,
                'data': node[1]
            })
        
        edges = []
        for edge in self.graph.edges(data=True):
            edges.append({
                'from': edge[0],
                'to': edge[1],
                'weight': edge[2].get('weight', 1),
                'types': edge[2].get('types', ['follow'])
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }

    def generate_report(self, username):
        """Generate a complete report for a profile"""
        if username not in self.graph:
            return {
                'username': username,
                'error': 'Profile not found in graph'
            }
        
        risk_score = self.calculate_profile_risk(username)
        threat_level = self._get_threat_level(risk_score)
        neighbors = list(self.graph.neighbors(username))
        communities = self.detect_communities()
        bot_clusters = self.detect_bot_clusters(communities)
        
        # Find which community user belongs to
        user_community = None
        user_cluster = None
        for i, comm in enumerate(communities):
            if username in comm:
                user_community = list(comm)
                break
        
        for cluster in bot_clusters:
            if username in cluster['members']:
                user_cluster = cluster
                break
        
        # Generate explanation
        explanations = []
        if risk_score >= 30:
            if self.graph.nodes[username].get('following', 0) > 5000:
                explanations.append(f"Very high following count ({self.graph.nodes[username].get('following', 0)})")
            if user_cluster:
                explanations.append(f"Connected to {user_cluster['size'] -1} accounts in a suspicious cluster")
            high_risk_neighbors = sum(1 for n in neighbors if self.calculate_profile_risk(n) >= 50)
            if high_risk_neighbors > 0:
                explanations.append(f"Connected to {high_risk_neighbors} high-risk accounts")
        
        return {
            'username': username,
            'risk_score': risk_score,
            'threat_level': threat_level,
            'connected_accounts': len(neighbors),
            'suspicious_connections': sum(1 for n in neighbors if self.calculate_profile_risk(n) >= 50),
            'community': user_community,
            'community_size': len(user_community) if user_community else 0,
            'in_bot_cluster': user_cluster is not None,
            'cluster': user_cluster,
            'total_bot_clusters': len(bot_clusters),
            'explanations': explanations,
            'generated_at': datetime.now().isoformat()
        }

    def add_sample_data(self):
        """Add sample data for testing"""
        # Real profiles
        real_users = [
            ('johndoe_social', {'followers': 2500, 'following': 300, 'is_bot': False}),
            ('janedoe_photos', {'followers': 1800, 'following': 250, 'is_bot': False}),
            ('tech_explorer', {'followers': 5000, 'following': 400, 'is_bot': False}),
        ]
        
        # Bot network 1
        bot_net1 = [
            ('bot_fake_001', {'followers': 50, 'following': 7500, 'is_bot': True, 'duplicate_profile_pic': True}),
            ('bot_fake_002', {'followers': 45, 'following': 7200, 'is_bot': True, 'duplicate_profile_pic': True}),
            ('bot_fake_003', {'followers': 55, 'following': 7100, 'is_bot': True, 'duplicate_profile_pic': True}),
            ('bot_fake_004', {'followers': 48, 'following': 6800, 'is_bot': True, 'duplicate_profile_pic': False}),
            ('bot_fake_005', {'followers': 60, 'following': 7000, 'is_bot': True, 'duplicate_profile_pic': True}),
        ]
        
        # Bot network 2
        bot_net2 = [
            ('scam_account_111', {'followers': 30, 'following': 5000, 'is_bot': True}),
            ('scam_account_222', {'followers': 25, 'following': 4800, 'is_bot': True}),
            ('scam_account_333', {'followers': 35, 'following': 5100, 'is_bot': True}),
        ]
        
        # Add all nodes
        all_profiles = real_users + bot_net1 + bot_net2
        for username, data in all_profiles:
            self.add_profile(username, data)
        
        # Connect real users
        self.add_connection('johndoe_social', 'janedoe_photos', 'follow', 1)
        self.add_connection('johndoe_social', 'tech_explorer', 'follow', 1)
        self.add_connection('janedoe_photos', 'tech_explorer', 'follow', 1)
        
        # Connect bot network 1
        for i in range(len(bot_net1)):
            for j in range(i+1, len(bot_net1)):
                self.add_connection(bot_net1[i][0], bot_net1[j][0], 'follow', 1)
                self.add_connection(bot_net1[i][0], bot_net1[j][0], 'like', 2)
        
        # Connect bot network 2
        for i in range(len(bot_net2)):
            for j in range(i+1, len(bot_net2)):
                self.add_connection(bot_net2[i][0], bot_net2[j][0], 'follow', 1)
        
        # Connect a real user to a bot (to test risk)
        self.add_connection('johndoe_social', 'bot_fake_001', 'follow', 1)
        
        return True

# Initialize global engine instance
social_graph_engine = SocialGraphIntelligence()
social_graph_engine.add_sample_data()
