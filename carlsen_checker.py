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
    def request_top_games_by_gametype(gametype):
        return requests.request("GET", 'https://lichess.org/api/user/' + username + '/perf/' + gametype).json()
    def build_top_oppos_dict_from_best_wins(gametype):
        try:
            oppo_names = {}
            user_json = request_top_games_by_gametype(gametype)
            bw = user_json['stat']['bestWins']['results']
            for oppo in bw:
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
    def combine_gametype_oppo_dicts(list_of_gametypes=['bullet','blitz','rapid']):
        top_oppos_combined_dict = {}

        for gm in list_of_gametypes:
            t = build_top_oppos_dict_from_best_wins(gm)
            for op in t:
                top_oppos_combined_dict.update({op:t[op]})

        #f = lambda *x: None
        #f( *(print(x,' : ',y, '\n') for x,y in top_oppos_combined_dict.items()))

        # **TBD: Sort this list of opponents by rating to optimize for successful lookups***
        #top_oppos_combined_dict.sort(key=lambda t: t['opRating'])

        return top_oppos_combined_dict

    return combine_gametype_oppo_dicts()
def recursive_search_player_best_wins(player_chain, target, depth):
    username = player_chain[len(player_chain)-1]
    if username is target:
        return player_chain
    elif len(player_chain)>depth:
        return None
    else:
        for opponent in get_top_oppos(username):
        #add opponent to player chain
        #recursive search
        #if returned chain ends in carlsen, compare to current carlsen chain, else discard
            #if new chain shorter, replace current carlsen chain, else discard

            pc_ext = copy.copy(player_chain)
            pc_ext.append(opponent)
            ret_player_chain = recursive_search_player_best_wins(pc_ext)
            if ret_player_chain[len(ret_player_chain)-1] is target:
                if !carlsen_chain or len(carlsen_chain) > len(ret_player_chain):
                    carlsen_chain = ret_player_chain
    if carlsen_chain:
        return carlsen_chain
    else return None
def start_search(player, target='DrNykterstein', depth=5):
    result_chain = recursive_search_player_best_wins(player, target, depth):
    if result_chain:
        print(player, '\'s Carlsen Number is ',len(result_chain),'. The path of victories is ', result_chain)
    else:
        print(player, ' does not have a Carlsen number lower than', depth+1)


username = get_starting_player(sys.argv[1]) if len(sys.argv)>1 else get_starting_player()
print('Data on ' + username + '...')
start_search(username)