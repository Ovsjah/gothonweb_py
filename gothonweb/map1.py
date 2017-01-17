from random import randint

class Room(object):   
       
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.guesses = 10
        self.code = '%d%d%d' % (randint(0,9), randint(0,9), randint(0,9))
        self.right_one = '%s' % randint(1,5)
        
    def go(self, direction):
        return self.paths.get(direction, None)

    def add_paths(self, paths):
        self.paths.update(paths)
        
    def open_lock(self, guess):
        self.guess = guess        
        
        if guess != self.code and self.guesses > 1:
            self.guesses -= 1           
        else:
            guess = '*'
            self.guesses = 10
            
        return guess
        
    def take_one(self, this):
        self.this = this
        
        if this != self.right_one:
            this = '*'
        else:
            this = this
            
        return this
        
        
place_of_crash = Room('Place of crash',
"""
The plane was flying above the tropic island. The weather was nasty.
So, the pilot decided to fly higher above the clouds.
Suddenly, he noticed a wierd cloud above others. It was strange...
These were the last of his thoughts... 
The lightnings stroke his plane...

You opened your eyes... 
Finding yourself laying on the ground...
You begin to inspect yourself... 
Thanks God you are alright!
""")

dungeon = Room('Dungeon',
"""
You are standing infront of the enterence to the dungeon...
For a while you can't decide do enter it...
At last you gather all your courage and enter the dungeon...
It's dark place you can't see anything...
There are lots of bats you hear them...
""")

dungeon_light = Room('Dungeon light',
"""
You use your torch and the bats fly away...
There is nothing interesting in the cave...
You see the path in front of you.
""")

death = Room('Death',
"""
You wake up the bats.
They are bloodsucking.
You are completely sucked.
You are dead!
""")

look_around = Room('Look around',
"""
There are lots of broken trees everywhere...
Also you see the place of plane crash...
There is a small path in the east among the trees...
""")

goods = Room('Goods',
"""
You find a pistol, a torch, a lighter
and a pack of cigarettes in the cabin of the crashed plane.
""")

place_of_crash.add_paths({
    'look around': look_around,
    'inspect plane': goods,
    'go east': dungeon
})

look_around.add_paths({
    'look around': look_around,
    'inspect plane': goods,
    'go east': dungeon
})

goods.add_paths({
    'look around': look_around,
    'go east': dungeon
})

dungeon.add_paths({
    'use torch': dungeon_light,
    '*': death
})

dungeon_light.add_paths({
    'move forward': altar
})
