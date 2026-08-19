
import networkx as nx
import logging
from datetime import datetime, timedelta
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialNetworkAnalyzer:
    def __init__(self):
        self.graph = nx.Graph()
        self.suspicious_nodes = set()
        self.bot_communities = []
        
    def validate_parameters(self, num_nodes):
        """Validate input parameters before network generation."""
        errors = []
        
        if not isinstance(num_nodes, int):
            try:
                num_nodes = int(num_nodes)
            except (ValueError, TypeError):
                errors.append("Number of nodes must be an integer")
                return False, errors
        
        if num_nodes < 10:
            errors.append("Number of nodes must be at least 10")
        if num_nodes > 500:
            errors.append("Number of nodes cannot exceed 500")
        
        return len(errors) == 0, errors
        
    def generate_sample_network(self, num_nodes=50):
        """Generate a sample social network with validation and error handling."""
        try:
            # Validate input
            is_valid, validation_errors = self.validate_parameters(num_nodes)
            if not is_valid:
                return {
                    'success': False,
                    'error': 'Parameter validation failed',
                    'details': validation_errors
                }
            
            num_nodes = int(num_nodes)
            
            # Reset state
            self.graph.clear()
            self.suspicious_nodes.clear()
            self.bot_communities.clear()
            
            np.random.seed(42)
            
            logger.info(f"Generating network with {num_nodes} nodes")
            
            node_types = ['legitimate', 'bot', 'fake_follower', 'scammer']
            type_probs = [0.5, 0.25, 0.15, 0.1]
            
            for i in range(num_nodes):
                node_type = np.random.choice(node_types, p=type_probs)
                followers = np.random.randint(10, 10000)
                following = np.random.randint(10, 5000)
                posts = np.random.randint(0, 500)
                
                risk_score = 0
                if node_type == 'bot':
                    risk_score = np.random.randint(80, 100)
                elif node_type == 'fake_follower':
                    risk_score = np.random.randint(60, 85)
                elif node_type == 'scammer':
                    risk_score = np.random.randint(75, 100)
                else:
                    risk_score = np.random.randint(0, 40)
                
                self.graph.add_node(
                    f'user_{i}',
                    type=node_type,
                    followers=followers,
                    following=following,
                    posts=posts,
                    risk_score=risk_score,
                    created_at=datetime.now() - timedelta(days=np.random.randint(1, 1000))
                )
            
            num_edges = int(num_nodes * 2.5)
            for _ in range(num_edges):
                u = f'user_{np.random.randint(0, num_nodes)}'
                v = f'user_{np.random.randint(0, num_nodes)}'
                if u != v and not self.graph.has_edge(u, v):
                    edge_type = np.random.choice(['follow', 'like', 'comment', 'mention'], p=[0.5, 0.25, 0.15, 0.1])
                    self.graph.add_edge(u, v, type=edge_type, weight=np.random.uniform(0.1, 1.0))
            
            self._detect_bot_communities()
            self._calculate_network_metrics()
            
            network_data = self._get_network_summary()
            
            # Validate the generated data
            is_data_valid, data_errors = self.validate_network_data(network_data)
            if not is_data_valid:
                logger.error(f"Network data validation failed: {data_errors}")
                return {
                    'success': False,
                    'error': 'Generated network data is invalid',
                    'details': data_errors
                }
            
            logger.info("Network generated successfully")
            return {
                'success': True,
                **network_data
            }
            
        except Exception as e:
            logger.exception(f"Failed to generate network: {str(e)}")
            return {
                'success': False,
                'error': 'Network generation failed',
                'details': [str(e)]
            }
    
    def validate_network_data(self, network_data):
        """Validate the structure and content of generated network data."""
        errors = []
        
        if not network_data:
            errors.append("Network data is empty")
            return False, errors
        
        # Check required fields
        required_fields = ['summary', 'nodes', 'edges']
        for field in required_fields:
            if field not in network_data:
                errors.append(f"Missing required field: {field}")
        
        if 'summary' in network_data:
            summary = network_data['summary']
            if not isinstance(summary.get('total_nodes'), int) or summary['total_nodes'] <= 0:
                errors.append("Invalid total_nodes in summary")
            if not isinstance(summary.get('total_edges'), int) or summary['total_edges'] < 0:
                errors.append("Invalid total_edges in summary")
        
        if 'nodes' in network_data:
            if not isinstance(network_data['nodes'], list):
                errors.append("Nodes must be a list")
            else:
                for i, node in enumerate(network_data['nodes']):
                    if not isinstance(node, dict):
                        errors.append(f"Node {i} must be an object")
                    else:
                        required_node_fields = ['id', 'risk_score', 'color']
                        for field in required_node_fields:
                            if field not in node:
                                errors.append(f"Node {i} missing field: {field}")
        
        if 'edges' in network_data:
            if not isinstance(network_data['edges'], list):
                errors.append("Edges must be a list")
            else:
                for i, edge in enumerate(network_data['edges']):
                    if not isinstance(edge, dict):
                        errors.append(f"Edge {i} must be an object")
                    else:
                        required_edge_fields = ['source', 'target']
                        for field in required_edge_fields:
                            if field not in edge:
                                errors.append(f"Edge {i} missing field: {field}")
        
        return len(errors) == 0, errors
    
    def _detect_bot_communities(self):
        """Detect bot communities with error handling."""
        try:
            if len(self.graph.nodes) == 0:
                return
            
            communities = nx.community.greedy_modularity_communities(self.graph)
            
            for community in communities:
                high_risk_count = 0
                for node in community:
                    if self.graph.nodes[node]['risk_score'] > 60:
                        high_risk_count += 1
                
                if high_risk_count >= len(community) * 0.6 and len(community) >= 3:
                    self.bot_communities.append({
                        'nodes': list(community),
                        'size': len(community),
                        'high_risk_count': high_risk_count,
                        'avg_risk_score': float(np.mean([self.graph.nodes[n]['risk_score'] for n in community]))
                    })
                    self.suspicious_nodes.update(community)
        except Exception as e:
            logger.exception(f"Error detecting bot communities: {str(e)}")
    
    def _calculate_network_metrics(self):
        """Calculate network metrics with error handling."""
        try:
            if len(self.graph.nodes) == 0:
                return {}
            
            betweenness = nx.betweenness_centrality(self.graph)
            eigenvector = nx.eigenvector_centrality(self.graph, max_iter=1000)
            
            for node in self.graph.nodes:
                self.graph.nodes[node]['betweenness'] = float(betweenness.get(node, 0))
                self.graph.nodes[node]['eigenvector'] = float(eigenvector.get(node, 0))
        except Exception as e:
            logger.exception(f"Error calculating network metrics: {str(e)}")
            for node in self.graph.nodes:
                self.graph.nodes[node]['betweenness'] = 0.0
                self.graph.nodes[node]['eigenvector'] = 0.0
    
    def _get_network_summary(self):
        """Generate network summary with error handling."""
        try:
            if len(self.graph.nodes) == 0:
                return {}
            
            total_nodes = len(self.graph.nodes)
            total_edges = len(self.graph.edges)
            avg_degree = float(np.mean([d for n, d in self.graph.degree()]))
            density = float(nx.density(self.graph))
            num_communities = len(self.bot_communities)
            suspicious_count = len(self.suspicious_nodes)
            
            risk_distribution = {
                'low': 0,
                'medium': 0,
                'high': 0,
                'critical': 0
            }
            
            for node in self.graph.nodes:
                score = self.graph.nodes[node]['risk_score']
                if score < 30:
                    risk_distribution['low'] += 1
                elif score < 60:
                    risk_distribution['medium'] += 1
                elif score < 80:
                    risk_distribution['high'] += 1
                else:
                    risk_distribution['critical'] += 1
            
            nodes_data = []
            for node, attrs in self.graph.nodes(data=True):
                nodes_data.append({
                    'id': node,
                    'type': attrs['type'],
                    'risk_score': attrs['risk_score'],
                    'followers': attrs['followers'],
                    'following': attrs['following'],
                    'posts': attrs['posts'],
                    'betweenness': float(attrs.get('betweenness', 0)),
                    'eigenvector': float(attrs.get('eigenvector', 0)),
                    'color': self._get_node_color(attrs['risk_score'])
                })
            
            edges_data = []
            for u, v, attrs in self.graph.edges(data=True):
                edges_data.append({
                    'source': u,
                    'target': v,
                    'type': attrs['type'],
                    'weight': float(attrs['weight'])
                })
            
            return {
                'summary': {
                    'total_nodes': total_nodes,
                    'total_edges': total_edges,
                    'avg_degree': round(avg_degree, 2),
                    'density': round(density, 4),
                    'num_bot_communities': num_communities,
                    'suspicious_count': suspicious_count,
                    'risk_distribution': risk_distribution,
                    'bot_communities': self.bot_communities
                },
                'nodes': nodes_data,
                'edges': edges_data
            }
        except Exception as e:
            logger.exception(f"Error generating network summary: {str(e)}")
            return {}
    
    def _get_node_color(self, risk_score):
        """Get color based on risk score."""
        if risk_score < 30:
            return '#10b981'
        elif risk_score < 60:
            return '#f59e0b'
        elif risk_score < 80:
            return '#ef4444'
        else:
            return '#dc2626'
    
    def analyze_profile_relationships(self, profile_id, connections_data):
        """Analyze profile relationships with error handling."""
        try:
            subgraph = nx.Graph()
            subgraph.add_node(profile_id, type='target', risk_score=50)
            
            for conn in connections_data:
                subgraph.add_node(conn['id'], **conn)
                subgraph.add_edge(profile_id, conn['id'], type=conn.get('relation', 'follow'))
            
            metrics = {
                'degree': subgraph.degree(profile_id),
                'clustering': float(nx.clustering(subgraph, profile_id)) if len(subgraph) > 2 else 0.0,
                'suspicious_connections': sum(1 for n, d in subgraph.nodes(data=True) if d.get('risk_score', 0) > 60)
            }
            
            return metrics
        except Exception as e:
            logger.exception(f"Error analyzing profile relationships: {str(e)}")
            return {
                'degree': 0,
                'clustering': 0.0,
                'suspicious_connections': 0,
                'error': str(e)
            }

analyzer = SocialNetworkAnalyzer()
