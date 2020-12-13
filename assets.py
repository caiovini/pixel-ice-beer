import pygame as pg
import pymunk as pm

from json import loads
from os.path import join

_ball_path = join("assets", "ball1.png")
_coordinates_path = join("assets", "balls_coord.json")
_ball_scale = (30, 30)
_hole_width = _hole_height = 15
_mass = 10

class Ball(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(
                _ball_path).convert_alpha(), _ball_scale)
        self.radius = 15
        self.body = pm.Body(mass=_mass,
                            moment=pm.moment_for_circle(mass=_mass, inner_radius=0, outer_radius=self.radius))
        rect = self.image.get_rect()
        self.body.position = rect.x, rect.y

    def set_position(self, x: float, y: float) -> None:

        self.body.position = (x, y)


def fetch_hole_coordinates() -> list:

    """
        Retrieve data from json file
        create a list with the rect and the type of hole 
        
        score: bool
        x: float
        y: float
        
    """

    holes_coordinates_list = []
    with open(_coordinates_path, "r") as myfile:  # Open json file
        data = myfile.read()
        obj = loads(data)
        for hole in obj:
            holes_coordinates_list.append({"coord": pg.Rect(
                hole["x"], hole["y"], _hole_width, _hole_height), "score": hole["score"]})

    return holes_coordinates_list
