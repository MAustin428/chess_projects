import requests
import json
import re
import sys
import copy


# Get input user
# Get top wins from bullet, blitz, rapid
# Concatenate opponents from these wins into a single sorted list, removing duplicates
# Check to see if any of them are Magnus Carlsen
# While the depth is less than five:
    # Get the top wins from these opponents, and concatenate into a list of opponents
    # Do the above for each player on that list (recursive call)
    # If the current player is Magnus Carlsen, return the player name
    # When depth of five is reached, return null
    # If a function call returns something besides null, append the returned player name to a list with the current player, and return


def get_starting_game(game_id=None):
    if game_id is None:
        print('Which chess game do you want data on?')
        return input()
    else:
        return game_id


def get_top_oppos(username):
    def get_oppo_id(oppo):
        return oppo['opId']['id']
    def request_top_games_by_game_speed(game_speed):
        return requests.request("GET", 'https://lichess.org/api/user/' + username + '/perf/' + game_speed).json()
    def build_top_oppos_dict_from_best_wins(game_speed):
        try:
            oppo_names = {}
            user_json = request_top_games_by_game_speed(game_speed)
            bw = user_json['stat']['bestWins']['results']
            for oppo in bw[:3]:
                if get_oppo_id not in oppo_names:
                    oppo_names.update({get_oppo_id(oppo):oppo})
                elif oppo['opRating'] > oppo_names[get_oppo_id(oppo)]['opRating']:
                    oppo_names.update({get_oppo_id(oppo):oppo})
#            f = lambda *x: None
#            f( *(print(x,' : ',y, '\n') for x,y in oppo_names.items()))
            return oppo_names

        except:
            print('user ', username, ' not found')
            return None
    def combine_game_speed_oppo_dicts(list_of_game_speeds=['bullet','blitz']):
        top_oppos_combined_dict = {}

        for gm in list_of_game_speeds:
            t = build_top_oppos_dict_from_best_wins(gm)
            if t:
                for op in t:
                    top_oppos_combined_dict.update({op:t[op]})

        #f = lambda *x: None
        #f( *(print(x,' : ',y, '\n') for x,y in top_oppos_combined_dict.items()))

        # **TBD: Sort this list of opponents by rating to optimize for successful lookups***
        #top_oppos_combined_dict.sort(key=lambda t: t['opRating'])

        return top_oppos_combined_dict

    return combine_game_speed_oppo_dicts()
def recursive_search_player_best_wins(player_chain, depth, target):
    print('Depth: ',len(player_chain))
    print('Player chain: ',player_chain)
    username = player_chain[len(player_chain)-1]
    carlsen_chain = []
    if username.lower() == target.lower():
        return player_chain
    elif len(player_chain)>depth:
        return None
    else:
        for opponent in get_top_oppos(username):
            pc_ext = copy.copy(player_chain)
            pc_ext.append(opponent)
            ret_player_chain = recursive_search_player_best_wins(pc_ext, depth, target)
            print('Returned player chain: ',ret_player_chain)
            if ret_player_chain and ret_player_chain[len(ret_player_chain)-1].lower() == target.lower():
                if len(carlsen_chain)==0 or len(carlsen_chain) > len(ret_player_chain):
                    print('Carlsen chain of length ',len(carlsen_chain),' found: ',carlsen_chain)
                    carlsen_chain = ret_player_chain
    if len(carlsen_chain) > 0:
        return carlsen_chain
    else:
        return None

def request_starting_game(game_id):
    request_url = 'https://lichess.org/game/export/'+game_id+''
    return requests.request("GET", request_url, params = {'moves':'false', 'tags':'false', 'clocks':'false', 'evals':'false', 'division':'false', 'literate':'false'}, headers = {'Accept': 'application/json'})

def start_search_by_game(game_id, depth=5, target='drnykterstein'):
    def get_winner_and_loser(game_json):
        def get_white_player(gj):
            return gj['players']['white']['user']['id']
        def get_black_player(gj):
            return gj['players']['black']['user']['id']
        
        if 'winner' in game_json:
            if game_json['winner'] == 'white':
                return [get_white_player(game_json), get_black_player(game_json)]
            elif game_json['winner'] == 'black':
                return [get_black_player(game_json), get_white_player(game_json)]
            else:
                print('Something went wrong determining the winner of this game.')
                return None
        else:
            print('You must choose a game with a winner')
            return None
    winner_and_loser_list = get_winner_and_loser(request_starting_game(game_id).json())
    result_chain = recursive_search_player_best_wins(winner_and_loser_list, depth, target)
    if result_chain:
        print(winner_and_loser_list[0], '\'s Carlsen Number is ',len(result_chain)-1,'. The path of victories is ', result_chain)
    else:
        print(winner_and_loser_list[0], ' does not have a Carlsen number lower than', depth+1)


if len(sys.argv) == 1:
    starting_game = get_starting_game()
else:
    starting_game = get_starting_game(sys.argv[1])
    if len(sys.argv) == 2:
        start_search_by_game(starting_game)
    else:
        depth = sys.argv[2]
        if len(sys.argv) == 3:
            start_search_by_game(starting_game, depth)
        else:
            target = sys.argv[3]
            if len(sys.argv) == 4:
                start_search_by_game(starting_game, depth, target)
            else:
                print('Too many command line variables.')