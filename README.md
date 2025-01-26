# Smoother_Roblox

Smoother_Roblox is a simple Flask-based service that fetches the top 5 servers with the lowest ping for a specific Roblox game using its **Game ID**.

## Features

- Returns server details, including ping, players, and maximum capacity.
- The `ReturnJobId` parameter allows fetching the server `JobId` when enabled.

## How It Works

The service uses Roblox's game API to gather available servers, filters out the top 5 servers with the lowest ping, and returns the information in JSON format.

## Endpoints

### `/get_top_servers`

#### Method: GET  
Fetch the top 5 servers with the lowest ping.

#### Parameters:
- **`game_id`** (required): The Roblox game ID.
- **`ReturnJobId`** (optional): If set to `true`, includes the `JobId` for each server in the response. Default is `false`.

#### Example Request:
```http
GET /get_top_servers?game_id=123456789&ReturnJobId=true

Example Response:
[
  {
    "ping": 50,
    "players": 10,
    "max_players": 30,
    "job_id": "abcdef123456"
  },
  {
    "ping": 55,
    "players": 15,
    "max_players": 30,
    "job_id": "ghijkl789012"
  }
]
```
# Setup and Usage
Prerequisites:

**Python 3.8+**

**Flask**

**Requests**

# Steps
**1**. Clone this repository:

```git clone https://github.com/ArthurJBR/Smoother_Roblox.git```

**2**. Navigate to the project directory:

```cd Smoother_Roblox```

**3**. Install dependencies:

```pip install flask requests```

**4**. Run the application:

```python app.py```

**Access the endpoint at Your Local Host/get_top_servers.**
