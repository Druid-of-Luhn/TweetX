import random


class Environment:

    entities = []

    def __init__(self):
        # make a spaceship
        self.entities.append(self.spaceship)
        # function for generating entities

    def space_contains(self, x, y):
        for entity in self.entities:
            if (entity.x-(width/2) <= x <= entity.x+(entity.width/2)) and (entity.y-(entity.height/2) <= y <= entity.y+(entity.height/2)):
                return entity 
        return None
        
    def update_positions(self):
        for ent in self.entities:
            if ent != self.spaceship:
                ent.x -= spaceship.velocity_x - ent.velocity_x
                ent.y -= spaceship.velocity_y - ent.velocity_y
                entity = space_contains(ent.x, ent.y)
                if entity != None:
                    ent.velocity_x = -1*ent.velocity_x
                    ent.velocity_y = -1*ent.velocity_y
                    entity.velocity_x = -1*entity.velocity_x
                    entity.velocity_y = -1*entity.velocity_y
                if ent.x < 0 or ent.x > 10 or ent.y < 0 or ent.y > 10:
                    entities.remove(ent)
        # function for randomly generating new entities entering field

if __name__ == "__main__":
    environment = Environment()
