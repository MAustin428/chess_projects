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


def get_starting_player(player=None):
    if player is None:
        print('Which chess enthusiast do you want data on?')
        return input()
    else:
        return player


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
            for oppo in bw[:4]:
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
    def combine_game_speed_oppo_dicts(list_of_game_speeds=['bullet']):
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
    magnus_chain = []
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
                if len(magnus_chain)==0 or len(magnus_chain) > len(ret_player_chain):
                    print('Magnus chain of length ',len(magnus_chain),' found: ',magnus_chain)
                    magnus_chain = ret_player_chain
    if len(magnus_chain) > 0:
        return magnus_chain
    else:
        return None
def start_search(player, depth=5, target='drnykterstein'):
    print('Data on ' + player + '...')
    result_chain = recursive_search_player_best_wins([player], depth, target)
    if result_chain:
        print('\n\n', player, '\'s Magnus Number is ',len(result_chain)-1,'. The path of victories is:')
        for i in result_chain:
            print(i)
    else:
        print('\n\n', player, ' does not have a Magnus number lower than', depth+1)

if len(sys.argv) == 1:
    username = get_starting_player()
    start_search(username)
else:
    username = get_starting_player(sys.argv[1])
    if len(sys.argv) == 2:
        start_search(username)
    else:
        depth = sys.argv[2]
        if len(sys.argv) == 3:
            start_search(username, depth)
        else:
            target = sys.argv[3]
            if len(sys.argv) == 4:
                start_search(username, depth, target)
            else:
                print('Too many command line variables.')

# Accepts up to three command line arguments, all optional. Order is username, depth, target.
def process_command_line_arguments():
    def number_of_command_line_arguments():
        return len(sys.argv)-1

    if number_of_command_line_arguments() == 0:
        username = get_starting_player()
        start_search(username)
    else:
        username = get_starting_player(sys.argv[1])
        
        if number_of_command_line_arguments() == 1:
            start_search(username)
        else:
            depth = sys.argv[2]
            
            if number_of_command_line_arguments() == 2:
                start_search(username, depth)
            else:
                target = sys.argv[3]
                
                if number_of_command_line_arguments() == 3:
                    start_search(username, depth, target)
                else:
                    print('Too many command line variables.')