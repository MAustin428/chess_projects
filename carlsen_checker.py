import requests
import json
import re
import sys


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


def get_top_oppo_list(username):
    def get_oppo_id(oppo):
        return oppo['opId']['id']
    def get_top_games_by_gametype(gametype):



        response = requests.request("GET", 'https://lichess.org/api/user/' + username + '/perf/' + gametype).json()

        try:
            bw = response['stat']['bestWins']['results']
            oppo_names = {}

            for oppo in bw:
                if get_oppo_id not in oppo_names:
                    oppo_names.update({get_oppo_id(oppo):oppo})
                elif oppo['opRating'] > oppo_names[get_oppo_id(oppo)]['opRating']:
                    oppo_names.update({get_oppo_id(oppo):oppo})
            #f = lambda *x: None
            #f( *(print(x,' : ',y, '\n') for x,y in oppo_names.items()))
            return oppo_names

        except:
            print('user ', username, ' not found')
            return None

    bullet_dict = get_top_games_by_gametype('bullet')
    blitz_dict = get_top_games_by_gametype('blitz')
    rapid_dict = get_top_games_by_gametype('rapid')
    
    print('Bullet: ',bullet_dict,'\n', 'Blitz: ',blitz_dict,'\n','Rapid: ',rapid_dict,'\n')
    top_oppos_combined_list = []
    for oppo in bullet_dict, blitz_dict, rapid_dict:
        top_oppos_combined_list.append(oppo)
    top_oppos_combined_list.sort(key=lambda oppo_rating name: oppo[name]['opRating'])


username = get_starting_player(sys.argv[1]) if len(sys.argv)>1 else get_starting_player()
print('Data on ' + username + '...')
get_top_oppo_list(username)


