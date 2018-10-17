#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction
import random
import logging

""" <<<Game Begin>>> """
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("Dracarys")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
ship_status = {}
""" <<<Game Loop>>> """

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map

    command_queue = []

    for ship in me.get_ships():
        # logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))
            
        maxHalite = game_map[ship.position].halite_amount;
        nextPos = ship.position;
        for x in ship.position.get_surrounding_cardinals():
            if game_map[x].halite_amount > maxHalite and game_map[x].is_empty:
                maxHalite = game_map[x].halite_amount
                nextPos = x;
        
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"
        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:
                if ship.halite_amount < 900 and ship.halite_amount+game_map[ship.position].halite_amount*0.25 > 900:
                    command_queue.append(ship.stay_still())
                    continue
                else:
                    move = game_map.naive_navigate(ship, me.shipyard.position)
                    command_queue.append(ship.move(move))
                    continue
        elif ship.is_full:
            ship_status[ship.id] = "returning"
        
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10:
            command_queue.append(ship.move(game_map.naive_navigate(ship, nextPos)))
        elif ship.is_full:
            ship_status[ship.id] = "returning"
        else:
            command_queue.append(ship.stay_still())

    if me.halite_amount >= 1500 and not game_map[me.shipyard].is_occupied and len(me.get_ships()) < 15:
        command_queue.append(me.shipyard.spawn())
    
    game.end_turn(command_queue)

