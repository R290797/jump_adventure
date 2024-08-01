from abc import ABC, abstractmethod
import threading

class BoostEffect(ABC):
    def __init__(self, player, duration=5):
        self.player = player
        self.duration = duration
        self.active = False

    def activate(self):
        if not self.active:
            self.active = True
            self.apply_effect()
            threading.Timer(self.duration, self.deactivate).start()

    def deactivate(self):
        if self.active:
            self.active = False
            self.remove_effect()

    @abstractmethod
    def apply_effect(self):
        pass

    @abstractmethod
    def remove_effect(self):
        pass


class Parachute(BoostEffect):
    def apply_effect(self):
        # Reduce the player's gravity more significantly to slow down falling
        self.original_gravity = self.player.gravity  # Store the original gravity
        self.player.gravity *= 0.5 # Reduce gravity to 20% of its original value

    def remove_effect(self):
        # Restore the player's gravity to its original value
        self.player.gravity = self.original_gravity


class Shield(BoostEffect):
    def apply_effect(self):
        self.player.shield_active = True

    def remove_effect(self):
        self.player.shield_active = False

class DoubleJump(BoostEffect):
    def apply_effect(self):
        self.player.double_jump_active = True

    def remove_effect(self):
        self.player.double_jump_active = False
