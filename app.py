# Access the top 5 servers with the lowest ping for a Roblox game

from flask import Flask, jsonify, request
import requests
import time
import os

app = Flask(__name__)

def fetch_top_servers(game_id):
    url = f"https://games.roblox.com/v1/games/{game_id}/servers/Public"
    params = {
        "cursor": "",
        "sortOrder": "Desc",
        "excludeFullGames": "true",
        "limit": 100
    }

    all_servers = []

    try:
        while True:
            print(f"Requesting servers with cursor: {params['cursor']}")
            response = requests.get(url, params=params)

            if response.status_code == 429:
                print("Rate limit reached. Delivering the list of servers collected so far...")
                break

            if response.status_code != 200:
                print(f"Error in response: {response.status_code} - {response.text}")
                break

            data = response.json()

            servers = data.get("data", [])
            if not servers:
                print("No servers returned on this page.")
            else:
                print(f"{len(servers)} servers found on this page.")

            all_servers.extend(servers)

            next_cursor = data.get("nextPageCursor")
            if not next_cursor:
                print("No next cursor found. Finishing collection.")
                break

            params["cursor"] = next_cursor

            time.sleep(2)

        if not all_servers:
            return []

        top_servers = sorted(all_servers, key=lambda s: s["ping"])[:5]
        return top_servers

    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return []

@app.route('/get_top_servers', methods=['GET'])
def get_top_servers():
    game_id = request.args.get('game_id')
    return_job_id = request.args.get('ReturnJobId', 'false').lower() == 'true'

    if not game_id:
        return jsonify({"error": "Parameter 'game_id' is required"}), 400

    top_servers = fetch_top_servers(game_id)

    if not top_servers:
        return jsonify({"error": "Could not find servers for game with given ID"}), 404

    response_data = []
    for server in top_servers:
        server_data = {
            "ping": server['ping'],
            "players": server['playing'],
            "max_players": server['maxPlayers']
        }
        
        if return_job_id:
            server_data["job_id"] = server['id']

        response_data.append(server_data)

    return jsonify(response_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
