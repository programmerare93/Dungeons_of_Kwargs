class Floor:
    floor: int
    max_rooms: int
    max_monsters_per_room: int

    def __init__(self):
        self.floor = 1
        self.max_rooms = 20
        self.max_monsters_per_room = 3

    def new_floor(self):
        self.floor += 1

        if self.max_monsters_per_room <= 10:
            self.max_monsters_per_room += 1

        if self.max_rooms <= 40:
            self.max_rooms += 2
