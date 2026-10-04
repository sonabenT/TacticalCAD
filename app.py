from flask import Flask, render_template, jsonify, request
import networkx as nx

app = Flask(__name__)

# Coordinates for Chennai Map Region
NODES = {
    'HOSPITAL': {'name': 'Central City Hospital', 'lat': 13.0827, 'lng': 80.2707, 'type': 'hospital'},
    'JUNCTION_A': {'name': 'Anna Salai Intersection', 'lat': 13.0850, 'lng': 80.2750, 'type': 'junction'},
    'JUNCTION_B': {'name': 'Central Flyover East', 'lat': 13.0900, 'lng': 80.2780, 'type': 'junction'},
    'JUNCTION_C': {'name': 'Mount Road Crossing', 'lat': 13.0800, 'lng': 80.2820, 'type': 'junction'},
    'SECTOR_4': {'name': 'Residential Sector 4', 'lat': 13.0750, 'lng': 80.2700, 'type': 'junction'},
    'EMERGENCY_SITE': {'name': 'Accident Location (Highway 9)', 'lat': 13.0950, 'lng': 80.2850, 'type': 'emergency'}
}

BASE_ROADS = [
    ('HOSPITAL', 'JUNCTION_A', 1.2, 50),
    ('HOSPITAL', 'SECTOR_4', 1.5, 40),
    ('JUNCTION_A', 'JUNCTION_B', 1.8, 60),
    ('JUNCTION_A', 'JUNCTION_C', 1.4, 45),
    ('SECTOR_4', 'JUNCTION_C', 2.0, 50),
    ('JUNCTION_B', 'EMERGENCY_SITE', 1.1, 55),
    ('JUNCTION_C', 'EMERGENCY_SITE', 2.5, 60),
    ('JUNCTION_B', 'JUNCTION_C', 1.3, 40)
]

def build_dynamic_graph(blocked_edges=None):
    if blocked_edges is None:
        blocked_edges = []
        
    G = nx.Graph()
    for u, v, dist, speed in BASE_ROADS:
        edge_id = f"{u}-{v}"
        alt_edge_id = f"{v}-{u}"
        
        if edge_id in blocked_edges or alt_edge_id in blocked_edges:
            continue
            
        travel_time_min = (dist / speed) * 60
        G.add_edge(u, v, weight=travel_time_min, distance=dist, speed=speed)
        
    return G

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    return jsonify(NODES)

@app.route('/api/route', methods=['POST'])
def calculate_realtime_route():
    data = request.get_json(silent=True) or {}
    source = data.get('source', 'HOSPITAL')
    target = data.get('target', 'EMERGENCY_SITE')
    blocked_roads = data.get('blocked_roads', [])

    G = build_dynamic_graph(blocked_roads)

    try:
        path = nx.dijkstra_path(G, source=source, target=target, weight='weight')
        total_time_min = nx.dijkstra_path_length(G, source=source, target=target, weight='weight')
        
        total_distance_km = 0
        turn_by_turn = []

        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            edge_data = G[u][v]
            dist = edge_data['distance']
            total_distance_km += dist
            
            turn_by_turn.append({
                'from': NODES[u]['name'],
                'to': NODES[v]['name'],
                'distance_km': round(dist, 2),
                'segment_time_min': round(edge_data['weight'], 1)
            })

        route_coords = [[NODES[node]['lat'], NODES[node]['lng']] for node in path]

        return jsonify({
            'success': True,
            'path': path,
            'route_coords': route_coords,
            'eta_minutes': round(total_time_min, 1),
            'total_distance_km': round(total_distance_km, 2),
            'navigation_log': turn_by_turn
        })
    except nx.NetworkNoPath:
        return jsonify({'success': False, 'error': 'No available road corridor! Blockade restricts access.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)