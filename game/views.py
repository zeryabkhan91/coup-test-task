import json
import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
# from django.core.serializers import serialize

from .models import Game
from .utils import complete_change_turn, ai_turn, block, challenge
from .utils import lost_influence, challenge_block, ambassador_card_selection ,initial_action

events = dict()


def create_game(request):
    if request.method == "GET":
        try:
            game = Game.create()
            game.turn_id = 0
            game.save()

            response = redirect("game_board") 
            response.set_cookie("COUP_name", "Player1")
            response.set_cookie("COUP_game_id", game.id)
            return response
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def game_board(request):
    game_id = request.COOKIES.get("COUP_game_id")
    game = Game.load(game_id)
    context ={}

    if game is None:
        return redirect("index")
    name = request.COOKIES.get("COUP_name")
    user = game.get_user(name)

    if request.method == "GET":
        if game.action.status == 4:
            player = game.get_user(game.action.lose_life[0])
            if not player.playing_cards:
                # Flash messages can be added to the context and passed to the template
                context = {"flash_message": "Killing a player with no influence"}
            elif len(player.playing_cards) == 1:
                player.lose_life(player.playing_cards[0])
                game.action.message += f"{player.name} has no influence now.\n"
                game.action.status = game.action.lose_life[2]
                for user_ in game.all_users:
                    events[f"{game_id}:{user_.name}"] = {
                        "type": "reload",
                        "data": {
                            "url": "game_board",
                        },
                    }
                game.save()
        if game.action.status == 5:
            game.action.do_perform_action(game)

        if len(game.get_alive_players()) == 1:
            return redirect("winning")

        print({"game": game, "user": user, **context})
        return render(
            request, "game/game_board.html", {"game": game, "user": user, **context}
        )

    status = game.action.status
    if status == 0:
        coup = request.POST.get("coup", "")
        steal = request.POST.get("steal", "")
        assassinate = request.POST.get("assassinate", "")
        other = request.POST.get("submit", "")

        initial_action(game, coup, steal, assassinate, other)
    elif status == 1:
        if "challenge" not in request.POST:
            return render(request, "game/game_board.html", {"game": game, "user": user})

        is_challenged = request.POST["challenge"]
        challenge(user, game, is_challenged)
    elif status == 2:
        if "block" not in request.POST:
            return render(request, "game/game_board.html", {"game": game, "user": user})
        value = request.POST["block"]
        block(user, game, value)
    elif status == 3:
        if "submit" not in request.POST:
            return render(request, "game/game_board.html", {"game": game, "user": user})
    
        reply = request.POST["submit"]
        challenge_block(user, game, reply)
    elif status == 4:
        if "to_kill" not in request.POST:
            return render(request, "game/game_board.html", {"game": game, "user": user})
    
        card_name = request.POST["to_kill"]
        lost_influence(user, game, card_name)
    elif status == 5:
        game.action.do_perform_action(game)
    elif status == 7:
        selected_cards = [int(c) for c in request.POST.getlist("card")]
    
        if len(selected_cards) != len(user.playing_cards):
            context = {"flash_message": "Please select the right amount of cards!"}
            return render(
                request, "game/game_board.html", {"game": game, "user": user, **context}
            )
            
        ambassador_card_selection(user, game, selected_cards)
    elif status == 6:
        complete_change_turn(name, game)

    game.save()
    # ai_turn(game)
    for user_ in game.all_users:
        events[f"{game_id}:{user_.name}"] = {
            "type": "reload",
            "data": {
                "url": "game_board",
            },
        }
    return render(request, "game/game_board.html", {"game": game, "user": user})

def winning(request):
    game_id = request.COOKIES.get("COUP_game_id")
    game = Game.load(game_id)
    if game is None:
        return redirect("main")
    name = request.COOKIES.get("COUP_name")
    for user in game.all_users:
        if user.name == name:
            break
    return render(request, "game/winning.html", {"game": game, "user": user})


def long_polling(request):
    game_id = request.COOKIES.get("COUP_game_id")
    game = Game.load(game_id)
    if game is None:
        return redirect("index")

    name = request.COOKIES.get("COUP_name")
    event_target = f"{game_id}:{name}"

    while True:
        event = get_event(event_target)

        if event:
            return JsonResponse(event)
        time.sleep(1)


def get_event(event_target):
    try:
        return events.pop(event_target)
    except KeyError:
        return None
