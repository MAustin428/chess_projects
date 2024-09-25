import requests
import re
import json

target = 'drnykterstein'

def get_all_games_for_player(player):
    params = {'moves':'false'}              # For debugging use params = {'max':'20', 'moves':'false'} 
    headers = {'Accept': 'application/x-ndjson'}
    resp = requests.get('https://lichess.org/api/games/user/' + player, params=params, headers=headers)
    return (json.loads(s) for s in resp.iter_lines())

def build_winner_list(games, target):
    winners_dict = {}

    def determine_winner(game_json, target):
        if 'winner' in game_json:
            game_id = game_json['id']
            white_player = game_json['players']['white']['user']['id'].lower()
            black_player = game_json['players']['black']['user']['id'].lower()
            target = target.lower()


            if game_json['winner'].lower() == 'white':
                if target == black_player:
                    return (white_player, game_id)
            elif game_json['winner'].lower() == 'black':
                if target == white_player:
                    return (black_player, game_id)
        else:
            return None
    
    for g in games:
        w = determine_winner(g, target)
        if w:
            w_player = w[0]
            w_id = w[1]
            winners_dict.update({w_player: w_id})
    return winners_dict




r = get_all_games_for_player(target)
w = build_winner_list(r, target)
print('\n\n',w)