from django.db import models
from django.utils import timezone

class Action:
  def __init__(self, id, player, action_type, target_player=None, challenge_winner=None, timestamp=None):
    self.id = id
    self.player = player
    self.action_type = action_type
    self.target_player = target_player
    self.challenge_winner = challenge_winner
    self.timestamp = timestamp or timezone.now()

  def __str__(self):
    return f"Action {self.id} by {self.player}"
  

  
class Player:
  def __init__(self, id, name, cards=None, coins=2):
    self.id = id
    self.name = name
    self.cards = cards or []
    self.coins = coins
    
  def encode(self):
    return {
      'id': self.id, 
      'name': self.name,
      'cards': self.cards,
      'coins': self.coins,
    }

  def __str__(self):
    return f"Player {self.id}"
  
class Card:
  def __init__(self, id, name, color):
    self.id = id
    self.name = name
    self.color = color

  def __str__(self):
    return f"{self.name} ({self.color})"

class Challenge:
    def __init__(self, id, challenger, challenged_action, success=False):
        self.id = id
        self.challenger = challenger
        self.challenged_action = challenged_action
        self.success = success

    def __str__(self):
        return f"Challenge {self.id} by {self.challenger}"\
          
class Influence:
  def __init__(self, id, player, card, revealed=False):
    self.id = id
    self.player = player
    self.card = card
    self.revealed = revealed

  def __str__(self):
    return f"Influence of {self.card} for {self.player}"