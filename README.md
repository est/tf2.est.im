# tf2.est.im


A tool to scan Team Fortress 2 servers using Python

## Steam protocol

[steam://connect/127.0.0.1:27018/password](https://developer.valvesoftware.com/wiki/Steam_browser_protocol)


## JSON format


    {
      "game_steam_id": 440,
      "server_name": "MY_SERVER",
      "server_type": 100,
      "ip": "127.0.0.1",
      "port": 27018,
      "bots_no": 0,
      "has_vac": 1,
      "players_no": 8,
      "rtt": 0.08315110206604004,
      "server_os": 119,
      "has_password": 0,
      "folder_name": "tf",
      "map_name": "dm_store_pro",
      "max_players": 24,
      "game_name": "Team Fortress"
    }


## ToDo


 [ ] Using a decorator for error 24 Too many open files intead of hard coded limit
 [ ] BUG: search does not terminate from master servers. 
 [ ] BUG: fix master server timeout in pool.map()