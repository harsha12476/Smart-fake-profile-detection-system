
from app import app

print("=== User Panel Routes ===")
for rule in app.url_map.iter_rules():
    endpoint = rule.endpoint
    # Skip admin routes
    if "admin" not in endpoint and "index" not in endpoint:
        print("  %-45s   %s" % (rule.rule, endpoint))
