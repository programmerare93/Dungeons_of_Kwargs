import winsound
import random


class SoundHandler:
    def __init__(self) -> None:
        self.SOUND_PATH = "assets\sounds\\"
        self.sword_sound_dict = {
            1: "sword_hit.wav",
            2: "sword_hit2.wav",
            3: "sword_hit3.wav",
            4: "sword_hit4.wav",
            5: "sword_hit5.wav",
        }
        self.player_hit_dict = {
            1: "player_hit.wav",
            2: "player_hit2.wav",
            3: "player_hit3.wav",
            4: "player_hit4.wav",
            5: "player_hit5.wav",
        }
        self.attack_dodged_dict = {
            1: "attack_dodged.wav",
            2: "attack_dodged2.wav",
            3: "attack_dodged3.wav",
            4: "attack_dodged4.wav",
            5: "attack_dodged5.wav",
        }

        self.monster_death_dict = {
            1: "monster_dead.wav",
            2: "monster_dead2.wav",
            3: "monster_dead3.wav",
            4: "monster_dead4.wav",
            5: "monster_dead5.wav",
            6: "monster_dead6.wav",
            7: "monster_dead7.wav",
            8: "monster_dead8.wav",
        }

    def sword_sound(self):
        winsound.PlaySound(
            self.SOUND_PATH + self.sword_sound_dict[random.randint(1, 5)],
            winsound.SND_FILENAME,
        )

    def player_hit(self):
        winsound.PlaySound(
            self.SOUND_PATH + self.player_hit_dict[random.randint(1, 5)],
            winsound.SND_FILENAME,
        )

    def attack_dodged(self):
        winsound.PlaySound(
            self.SOUND_PATH + self.attack_dodged_dict[random.randint(1, 5)],
            winsound.SND_FILENAME,
        )

    def monster_death(self):
        winsound.PlaySound(
            self.SOUND_PATH + self.monster_death_dict[random.randint(1, 8)],
            winsound.SND_FILENAME,
        )
