from abc import ABC, abstractmethod
import threading

import pygame
import time
from pydantic import BaseModel, Field
from player import Player

class BoostEffect(BaseModel):
    
    player: Player
    duration: float = Field(default=5.0)
    collection_time: float = Field(default=0.0)
    active: bool = Field(default=False)

    def activate(self):

        if not self.active:
            self.collection_time = time.time()
            self.active = True
            self.apply_effect()


    def deactivate(self):
        if self.active:
            self.active = False
            self.remove_effect()

    def check_duration(self):

        if time.time() - self.collection_time > self.duration:
            self.deactivate()

    def apply_effect(self):
        pass

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
