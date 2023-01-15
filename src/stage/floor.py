class Floor:
    """Floor class som innehåller information om vilken våning spelaren befinner sig på och hur många rum som kan finnas på den våningen"""
    floor: int
    max_rooms: int
    max_monsters_per_room: int

    def __init__(self):
        self.floor = 0
        self.max_rooms = 20
        self.max_monsters_per_room = 3
