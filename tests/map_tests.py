from nose.tools import *
from gothonweb.map import *


def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""")
    assert_equal(gold.name, "GoldRoom")
    assert_equal(gold.paths, {})
    
def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")
    
    center.add_paths({'north': north, 'south': south})
    assert_equal(center.go('north'), north)
    assert_equal(center.go('south'), south)
    
def test_map():
    start = Room("Start", "You can go west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")
    
    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})
    
    assert_equal(start.go('west'), west)
    assert_equal(start.go('west').go('east'), start)
    assert_equal(start.go('down').go('up'), start)
    
def test_gothon_game_map():
    assert_in(generic_death.description, quips)
    
    assert_equal(START.go('shoot!'), generic_death)
    assert_equal(START.go('dodge!'), generic_death)
    
    room = START.go('tell a joke')
    assert_equal(room, laser_weapon_armory)
    
    room = laser_weapon_armory
    room.guesses = 1
    assert_equal(room.open_lock('111'), '*')
    
    room = laser_weapon_armory.go('*')
    assert_equal(room, generic_death)
        
    room = laser_weapon_armory.go(laser_weapon_armory.code)
    assert_equal(room, the_bridge)
    
    room = the_bridge.go('throw the bomb')
    assert_equal(room, generic_death)
    
    room = the_bridge.go('slowly place the bomb')
    assert_equal(room, escape_pod)
    
    room = escape_pod.go('*')
    assert_equal(room, the_end_loser)
    
    room = escape_pod.go(escape_pod.right_one)
    assert_equal(room, the_end_winner)
