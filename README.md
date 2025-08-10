# Smoother_Roblox

Smoother_Roblox is a simple Flask-based service that fetches the closest server for a specific Roblox game using its **Game ID**.

## Features

- Returns server details, including distance, players, and maximum capacity.

## How It Works

The service uses Roblox's game API to gather available servers, filters out the closest server, and returns the information in JSON format.

## Endpoints

### `/getip`

#### Method: GET  
Fetch the closest server

#### Parameters:
- **`game_id`** (required): The Roblox game ID.

#### Example Request:
```http
GET /get_top_servers?game_id=123456789

Example Response:
{
  "allServersCount": 300,
  "closestServer": {
    "distance_km": 100,
    "gameId": "abcdefgh-ijkl-mnop-qrst-uvwxyz123456",
    "ip": "128.116.45.33",
    "location": {
      "city": "Miami",
      "country": "United States",
      "flag": "https://ipgeolocation.io/static/flags/us_64.png",
      "ip": "128.116.45.33",
      "latitude": 25.77481,
      "longitude": -80.19773,
      "state": "Florida"
    },
    "maxPlayers": 16,
    "playing": 16,
    "port": 55934
  },
  "thumbnailUrl": "https://tr.rbxcdn.com/180DAY-7f5a4cc032558a51b3cacf8a25c9a992/512/512/Image/Png/noFilter"
}
```
# Setup and Usage
Prerequisites:

**Python 3.8+**

**Flask**

**Requests**

**python-dotenv**

**concurrent-log-handler**

# Steps
**1**. Clone this repository:

```git clone https://github.com/ArthurJBR/Smoother_Roblox.git```

**2**. Navigate to the project directory:

```cd Smoother_Roblox```

**3**. Install dependencies:

```pip install flask requests python-dotenv concurrent-log-handler```

**4**. Create a file called .env:

Create a file .env in the script directory with the following variables:
NODE_ENV=production
PORT=8000
ROBLOX_COOKIE={YOUR ROBLOX .ROBLOSECURITY}

**4**. Run the application:

```python app.py```

**Access the endpoint at Your Local Host/getip.**
