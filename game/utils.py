import time
from django.shortcuts import redirect

# 0
def initial_action(game, coup, steal, assassinate, other):
    if coup:
        game.action.do_action(game, "coup", coup)
    elif steal:
        game.action.do_action(game, "steal", steal)
    elif assassinate:
        game.action.do_action(game, "assassinate", assassinate)
    else:
        game.action.do_action(game, other)

# 1
def challenge(user, game, is_challenged):
  is_challenged = True if is_challenged == "yes" else False
  game.action.do_challenge_action(game, user.name, is_challenged)

# 2
def block(user, game, value):
  if value == "no":
      game.action.do_block(game, False, user.name)
  elif value == "yes":
      action_word = game.action.action_to_word[game.action.action[0]]
      if action_word == "assassinate":
          card = game.deck.reverse_mapping("Contessa")
      elif action_word == "foreign aid":
          card = game.deck.reverse_mapping("Duke")
      game.action.do_block(game, True, user.name, card)
  else:
      card = game.deck.reverse_mapping(value)
      game.action.do_block(game, True, user.name, card)

# 3
def challenge_block(user, game, reply):
  reply = True if reply == "yes" else False
  game.action.do_challenge_block(game, reply, user.name) 

# 4
def lost_influence(user, game, card_name):
    if game.action.lose_life[0] == user.name:
        card_type = game.deck.reverse_mapping(card_name)  
        game.action.do_lose_life(game, card_type)

# 6
def complete_change_turn(name, game):
    if name not in game.action.notified:
      game.action.notified.append(name)

    if len(game.action.notified) == len(game.get_alive_players()):
      game.action.completed = 1
      is_continued = game.next_move()
      if not is_continued:
          game.save()
          return redirect("winning")
      
# 7
def ambassador_card_selection(user, game, selected_cards):
    discarded = game.action.ambassador_cards[: 2 + len(user.playing_cards)]
    for c in selected_cards:
        discarded.remove(c)
    user.playing_cards = selected_cards
    for c in discarded:
        game.deck.add_card(c)
    game.action.status = 6

def ai_turn(game, name = "AI Player"):
  # context ={}
  game.cur_player = name
  user = game.get_user(name)

  if game is None:
      return redirect("index")

  if game.action.status == 0:
    # coup = request.POST.get("coup", "")
    # steal = request.POST.get("steal", "")
    # assassinate = request.POST.get("assassinate", "")
    # other = request.POST.get("submit", "")
    target = game.all_users[0]
    
    initial_action(game, target, None, None, None)
  if game.action.status == 1:
    # implement yes or no
    is_challenged = "no"
    challenge(user, game, is_challenged)
  elif game.action.status == 2:
    # implement yes or no
    block(user, game, "no")
  elif game.action.status == 3:
    # implement reply logic
    reply = "no"
    challenge_block(user, game, reply)
  elif game.action.status == 4:
    # implement random card selection from AI cards
    card_name = "Duke"
    lost_influence(user, game, card_name)
  elif game.action.status == 5:
        game.action.do_perform_action(game)
  elif game.action.status == 6:
    complete_change_turn(name, game)
  elif game.action.status == 7:
    # int(c) for c in request.POST.getlist("card") implement logic for selected cards
    selected_cards = []
    ambassador_card_selection(user, game, selected_cards)

  time.sleep(1)
  game.save()