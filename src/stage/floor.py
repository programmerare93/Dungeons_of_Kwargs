class Floor:
    floor: int
    room_max_size: int
    room_min_size: int
    max_rooms: int

    def __init__(self):
        self.floor = 1
        self.room_max_size = 10
        self.room_min_size = 5
        self.max_rooms = 20

    def new_floor(self):
        self.floor += 1
        if self.max_rooms <= 40:
            self.max_rooms += 2
