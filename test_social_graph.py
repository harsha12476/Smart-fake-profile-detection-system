
from social_graph_intelligence import social_graph_engine

print("Testing Social Graph Intelligence Engine...")
print()

# Test graph data
graph = social_graph_engine.get_graph_json()
print(f"Total nodes in graph: {len(graph['nodes'])}")
print(f"Total edges in graph: {len(graph['edges'])}")
print()

# Test bot cluster detection
clusters = social_graph_engine.detect_bot_clusters()
print(f"Detected {len(clusters)} bot clusters:")
for cluster in clusters:
    print(f"  - Cluster {cluster['cluster_id']}: {len(cluster['members'])} accounts, {cluster['risk_score']:.1f}% risk")
print()

# Test report for sample user
for username in ['johndoe_social', 'bot_fake_001', 'tech_explorer']:
    report = social_graph_engine.generate_report(username)
    print(f"Report for '{username}':")
    print(f"  Risk Score: {report['risk_score']}")
    print(f"  Threat Level: {report['threat_level']}")
    print(f"  Connected to: {report['connected_accounts']} accounts")
    print(f"  Suspicious connections: {report['suspicious_connections']}")
    print(f"  In bot cluster: {report['in_bot_cluster']}")
    if report['explanations']:
        print(f"  Explanations: {', '.join(report['explanations'])}")
    print()

print("✅ All tests passed!")
