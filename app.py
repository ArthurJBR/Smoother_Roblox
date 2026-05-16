import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from math import radians, sin, cos, sqrt, atan2
import time
import concurrent.futures

MTUwNDkzMTgzOTMxMDE3MjI1MA.G88VzI.mHWkLGKjqmPVNFzX-8TTC2rWOs90CyXRHtFLbQ

load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

IPGEO_API_KEY = "ca92ae8841f0463f8ba0948524e200c5"

def format_cookie(cookie):
    return f".ROBLOSECURITY={cookie}; path=/; domain=.roblox.com;"

def get_thumbnail(place_id):
    try:
        res = requests.get(
            "https://thumbnails.roblox.com/v1/places/gameicons",
            params={
                "placeIds": place_id,
                "returnPolicy": "PlaceHolder",
                "size": "512x512",
                "format": "Png",
                "isCircular": "false"
            },
            timeout=10
        )
        data = res.json().get("data", [])
        if not data or data[0].get("state") != "Completed":
            return None
        return data[0].get("imageUrl")
    except Exception as e:
        print(f"[ERROR] get_thumbnail: {e}")
        return None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def get_ip_location(ip):
    try:
        res = requests.get(
            f"https://api.ipgeolocation.io/v2/ipgeo?apiKey={IPGEO_API_KEY}&ip={ip}",
            timeout=10
        )
        data = res.json()
        if not data.get("ip"):
            return None
        
        location_data = {
            "ip": data["ip"],
            "city": data.get("location", {}).get("city"),
            "state": data.get("location", {}).get("state_prov"),
            "country": data.get("location", {}).get("country_name"),
            "latitude": float(data.get("location", {}).get("latitude", 0)),
            "longitude": float(data.get("location", {}).get("longitude", 0)),
            "flag": data.get("location", {}).get("country_flag"),
        }
        return location_data
    except Exception as e:
        print(f"[ERROR] get_ip_location: {e}")
        return None
    
def get_public_ip():
    try:
        res = requests.get("https://api.ipify.org?format=json", timeout=5)
        return res.json().get("ip")
    except:
        return None

def process_server(place_id, server, my_lat, my_lon, custom_cookie):
    try:
        headers = {
            "Referer": f"https://www.roblox.com/games/{place_id}/",
            "Origin": "https://roblox.com",
            "Cookie": format_cookie(custom_cookie or os.getenv("ROBLOX_COOKIE")),
            "User-Agent": "Roblox/WinInet"
        }
        payload = {
            "placeId": place_id,
            "isTeleport": False,
            "gameId": server["id"],
            "gameJoinAttemptId": server["id"]
        }
        res = requests.post(
            "https://gamejoin.roblox.com/v1/join-game-instance",
            json=payload, headers=headers, timeout=10
        )
        
        data = res.json()

        if not data.get("jobId") or not data.get("joinScript"):
            return {
                "ip": None, "port": None, "distance_km": None,
                "playing": server.get("playing"),
                "maxPlayers": server.get("maxPlayers"),
                "gameId": server["id"]
            }

        udmux = data["joinScript"].get("UdmuxEndpoints") \
                 or data["joinScript"].get("Endpoints") \
                 or []

        if not udmux or not isinstance(udmux, list) or not udmux[0].get("Address"):
            return {
                "ip": None, "port": None, "distance_km": None,
                "playing": server.get("playing"),
                "maxPlayers": server.get("maxPlayers"),
                "gameId": server["id"]
            }

        ip = udmux[0].get("Address")
        port = udmux[0].get("Port")

        srv_location = get_ip_location(ip) if ip else None

        srv_lat = srv_location.get("latitude") if srv_location else None
        srv_lon = srv_location.get("longitude") if srv_location else None
        
        if srv_lat is not None and srv_lon is not None and my_lat is not None and my_lon is not None:
            dist = haversine(my_lat, my_lon, srv_lat, srv_lon)
        else:
            dist = None

        return {
            "ip": ip,
            "port": port,
            "location": srv_location,
            "distance_km": round(dist, 2) if dist is not None else None,
            "playing": server.get("playing"),
            "maxPlayers": server.get("maxPlayers"),
            "gameId": server["id"]
        }
    except Exception as e:
        print(f"[ERROR] process_server: {e}")
        return {
            "ip": None, "port": None, "distance_km": None,
            "playing": server.get("playing"),
            "maxPlayers": server.get("maxPlayers"),
            "gameId": server["id"]
        }
    
def fetch_all_servers(place_id, max_pages=10, delay=2):
    all_servers = []
    cursor = None
    
    for _ in range(max_pages):
        try:
            params = {
                "sortOrder": "Desc",
                "limit": 100
            }
            if cursor:
                params["cursor"] = cursor
            
            res = requests.get(
                f"https://games.roblox.com/v1/games/{place_id}/servers/Public",
                params=params,
                timeout=10
            )
            data = res.json()
            
            if "data" not in data or "errors" in data:
                break
            
            all_servers.extend(data["data"])
            cursor = data.get("nextPageCursor")
            
            if not cursor:
                break
            
            time.sleep(delay)
        except Exception as e:
            print(f"Error at search servers: {e}")
            break
    
    return all_servers

@app.route("/getip", methods=["GET"])
def get_ip():
    try:
        place_id = request.args.get("placeId", type=int)
        if not place_id:
            return "Invalid placeid.", 400
        
        try:
            my_ip = get_public_ip() or request.remote_addr
            location_data = get_ip_location(my_ip)
            my_lat = location_data.get("latitude") if location_data else None
            my_lon = location_data.get("longitude") if location_data else None
        except Exception as e:
            print(f"Error at get your location: {e}")
            return "Failed to get your location.", 500

        custom_cookie = request.headers.get("Authorization")
        if custom_cookie:
            try:
                res = requests.get(
                    "https://www.roblox.com/mobileapi/userinfo",
                    headers={"Cookie": format_cookie(custom_cookie)},
                    timeout=10
                )
                if not isinstance(res.json(), dict):
                    return "Invalid cookie.", 400
            except:
                return "Invalid cookie.", 400
            
        try:
            all_servers = fetch_all_servers(place_id, max_pages=10, delay=2)
        except Exception as e:
            print(f"Failed to get servers: {e}")
            return "Failed to get servers.", 500
        
        servers_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for server in all_servers:
                futures.append(
                    executor.submit(
                        process_server,
                        place_id,
                        server,
                        my_lat,
                        my_lon,
                        custom_cookie
                    )
                )
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        servers_data.append(result)
                except Exception as e:
                    print(f"Error at process server: {e}")

        servers_data.sort(
            key=lambda x: x["distance_km"] if x["distance_km"] is not None else float("inf")
        )

        return jsonify({
            "closestServer": servers_data[0] if servers_data else None,
            "allServersCount": len(servers_data),
            "thumbnailUrl": get_thumbnail(place_id)
        })
    except Exception as e:
        print(f"[ERROR] endpoint /getip: {e}")
        return str(e), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
