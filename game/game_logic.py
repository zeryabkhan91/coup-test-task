# game/logic.py
from random import choice
from .utils import create_initial_influences, perform_action, resolve_action

def start_game(players):
    initialize_game_state(players)

def get_random_player_action(player):
  available_actions = ["Tax", "Assassinate", "Steal"]
  return choice(available_actions)

def ai_take_turn(player):
  action_type = get_random_player_action(player)
  target_player = choose_target_player(player, action_type)  # Implement AI's target selection logic if needed
  perform_action(player, action_type, target_player)

def player_take_turn(player, action_type, target_player=None):
  perform_action(player, action_type, target_player)

def choose_target_player(player, action_type):
  if action_type == "Tax":
      return None
  elif action_type in ["Assassinate", "Steal"]:
      other_players = Player.objects.exclude(id=player.id)
      return choice(other_players)
  else:
      return None

def resolve_turns(players):
    for player in players:
        if player.is_ai:
            ai_take_turn(player)
        else:
            player_take_turn(player)

    resolve_challenges()

def resolve_challenges():
    challenges = Challenge.objects.all()

    for challenge in challenges:
        challenged_action = challenge.challenged_action
        challenged_player = challenged_action.player

        if challenge_successful(challenged_player, challenged_action):
            challenged_action.success = True
            resolve_action(challenged_action)
        else:
            resolve_challenge(challenge)

def challenge_successful(challenged_player, challenged_action):
    influences = Influence.objects.filter(player=challenged_player, revealed=False)
    return challenged_action.action_type not in [influence.card_name for influence in influences]

def resolve_challenge(challenge):
    challenged_action = challenge.challenged_action
    challenged_action.player.coins -= 1
    challenged_action.player.save()
    reveal_influence(challenged_action.player)
    challenge.success = True
    challenge.save()

def resolve_action(action):
    player = action.player
    action_type = action.action_type
    target_player = action.target_player

    if action_type == "Tax":
        player.coins += 3
    elif action_type == "Assassinate":
        target_player_loses_influence(target_player)
    elif action_type == "Steal":
        coins_stolen = steal_coins(player, target_player)
        player.coins += coins_stolen
    # Add more cases for other actions as per game rules

    player.save()

def reveal_influence(player):
    unrevealed_influences = Influence.objects.filter(player=player, revealed=False)
    if unrevealed_influences.exists():
        influence_to_reveal = unrevealed_influences.first()
        influence_to_reveal.revealed = True
        influence_to_reveal.save()

def target_player_loses_influence(target_player):
    unrevealed_influences = Influence.objects.filter(player=target_player, revealed=False)
    if unrevealed_influences.exists():
        influence_to_lose = unrevealed_influences.first()
        influence_to_lose.revealed = True
        influence_to_lose.save()

def steal_coins(player, target_player):
    coins_stolen = min(target_player.coins, 2)  # Assuming stealing a maximum of 2 coins
    target_player.coins -= coins_stolen
    target_player.save()
    return coins_stolen

def is_game_over(players):
    # Check if the game is over based on the number of remaining players
    return len(players) == 1
