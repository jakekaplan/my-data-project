"""
WitchCraft-ETL (artifact edition)
Requires Prefect ≥ 2.18.0  # create_markdown_artifact lives here
Run with:  python witchcraft_etl.py
"""

from random import randint, random
from time import sleep
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact

INGREDIENTS = [
    "eye of 🦎 newt",
    "toe of 🐸 frog",
    "wool of 🐏 bat",
    "tongue of 🐶 dog",
    "adder's 🐍 fork",
    "blind-worm’s 🐛 sting",
    "lizard-leg 🦎",
    "howlet’s 🦉 wing",
]

@task
def gather_ingredients(batch: int = 4) -> list[str]:
    stash = INGREDIENTS[:batch]
    print(f"🧺  Foraged: {', '.join(stash)}")
    return stash

@task
def chant_incantation(stash: list[str]) -> str:
    print("🎶  BUBBLE  BUBBLE  BOIL  AND  TROUBLE  🎶")
    sleep(1)
    mixture = " | ".join(stash) + " | dragon-breath steam"
    print(f"🪄  Chanting over: {mixture}")
    return mixture

@task
def stir_cauldron(mixture: str, clockwise: bool = False, stirs: int = 3) -> str:
    direction = "clockwise" if clockwise else "counter-clockwise"
    for i in range(1, stirs + 1):
        print(f"🌀  Stir {i}/{stirs} ({direction})")
        sleep(0.4)
    return f"{mixture} + foam-layer"

@task
def taste_test(potion: str) -> str:
    verdict = "😋 perfectly witchy" if random() < 0.5 else "😻 cat-approved delicious"
    print(f"👅  Taste test on [{potion[:30]}…]: {verdict}")
    return verdict

@task
def bottle_potion(potion: str, verdict: str, destination: str = "warehouse.spells") -> int:
    potions_bottled = randint(5_000, 20_000)
    print(f"🧪  Bottled {potions_bottled:,} vials (taste: '{verdict}') → {destination}")
    return potions_bottled



@flow(log_prints=True)
def witchcraft_etl(batch: int = 4):
    stash = gather_ingredients(batch)
    mixture = chant_incantation(stash)
    potion = stir_cauldron(mixture)
    verdict = taste_test(potion)
    potions_bottled = bottle_potion(potion, verdict)

    print("✨  Potions bottled! Creating summary... ✨")
    artifact_md = f"🧪 **Potion Batch:** {potions_bottled:,} vials bottled! 🔮"
    create_markdown_artifact(
        markdown=artifact_md,
        key="witchcraft-etl-batch",
        description="Quick summary of tonight’s potion output",
    )

if __name__ == "__main__":
    witchcraft_etl()
