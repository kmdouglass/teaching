from manim import *
from manim.typing import Vector3D

from settings import *


def by(
    scene: Scene,
) -> None:
        author = Text("by Kyle M. Douglass", font_size=24)
        scene.play(Write(author))

        scene.wait(BY_WAIT_TIME_S)


def debug(
    text: str,
    scene: Scene,
    wait_time_s: float = 5.0,
) -> None:
    debug_text = Text(
        text,
        font_size=32,
        color=YELLOW,
    )

    scene.add(debug_text)
    scene.wait(wait_time_s)
    scene.remove(debug_text)


def explain(
    text: str,
    scene: Scene,
    edge: Vector3D = UP,
    font_size: int = EXPLANATION_FONT_SIZE,
    wait_time_s: float = EXPLANATION_WAIT_TIME_S,
) -> None:
    explanation = Text(
        text,
        font_size=font_size,
    )
    explanation.to_edge(edge)

    scene.play(Write(explanation))
    scene.wait(wait_time_s)
    scene.play(FadeOut(explanation))
