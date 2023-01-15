import random
import asyncio
import winsound


class SoundPlayer:
    def __init__(self):
        self.sound_path = "assets\\sounds\\"

    async def play(self, sound):
        winsound.PlaySound(
            f"{self.sound_path}{sound}{random.randint(1,5)}", winsound.SND_FILENAME
        )
        await asyncio.sleep(0)
