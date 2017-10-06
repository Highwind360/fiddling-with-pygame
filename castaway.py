#!/usr/bin/env python3
"""
castaway.py
Grayson Sinclair

A program for practicing writing games with pygame. You play as a person
stranded out in the wilderness. You must survive as long as possible.

TODO: create a configuration file
TODO: figure out how to set the framerate
    - At the end of each game loop, wait until enough time has passed before
        rendering. Before waiting, decide what the next moment in time that the
        following tick will have to wait until will be
    - allow the system to run gracefully even if the framerate is set too high
TODO: create a file format for storing levels
"""

import pygame


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.magnitude = math.sqrt((x**2) + (y**2))

    def to_tuple(self):
        return (self.x, self.y)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image=(255,255,255), dim=(10,10), coords=Vector(0,0)):
        """Creates a basic game object.
        
        image - accepts a tuple of length 3 as RGB values, or a pygame Surface
        dim - the dimensions of the object (width, height)
            note that this value is ignored in the case of image being a Surface
        coords - the coordinates to render at, as a Vector"""
        pygame.sprite.Sprite.__init__(self)
        if type(image) == pygame.Surface:
            self.image = image
        else:
            self.image = pygame.Surface(dim)
            self.image.fill(image)
        self.rect = self.image.get_rect(top_left=coords.to_tuple())
        self.speed = Vector(0, 0)

    def update(self):
        """Move the object according to its speed."""
        self.move(self.speed.to_tuple())

    def move(self, offset):
        """Move the object by some offset (x, y)."""
        self.rect = self.rect.move(offset)


def apply_gravity(group):
    """Cause all gameobjects in group to accelerate downwards."""
    for go in group.sprites():
        go.speed += config["physics"]["gravity"]

def handle_collisions(player, terrain):
    """Handler for how to respond when sprites collide."""

    # If the player has collided with an impassable object, stop player movement
    for barrier in pygame.sprite.spritecollisions(player, terrain, False):
        pass # TODO: HTF do I reliably detect which side collided?

def main():
    pygame.init()

    # load the configuration options
    global config
    config = { "physics": { "gravity": 2 } }
    
    # initialize all the groups
    world, fallable = [pygame.sprite.Group() for i in range(2)]

    # spawn the player
    player = GameObject(dim=(50,100))

    while True:
        # Process the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Add all engine forces
        apply_gravity(fallable)

        # Allow gameobjects to update themselves
        world.update()

        # Detect and respond to collisions
        handle_collisions(player, terrain)

        # Wait until next frame is due to render
        # TODO

        # Render
        world.clear(screen)
        world.draw(screen)


if __name__ == "__main__":
    main()
