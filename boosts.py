import pygame
import time
from pydantic import BaseModel, Field


class BoostEffect(BaseModel):

    duration: float = Field(default=5.0)
    collection_time: float = Field(default=0.0)
    active: bool = Field(default=False)

    def activate(self):

        if not self.active:
            self.collection_time = time.time()
            self.apply_effect()

    def deactivate(self):
        if self.active:
            self.remove_effect()

    def check_duration(self):

        if time.time() - self.collection_time > self.duration:
            self.deactivate()
            return True

    def apply_effect(self):
        pass

    def remove_effect(self):
        pass


class Parachute(BoostEffect):

    def apply_effect(self):
        self.active = True

    def remove_effect(self):
        self.active = False


class Shield(BoostEffect):

    duration: float = Field(default=10.0)

    def apply_effect(self):
        self.active = True

    def remove_effect(self):
        self.active = False


class DoubleJump(BoostEffect):

    def apply_effect(self):
        self.active = True

    def remove_effect(self):
        self.active = False
