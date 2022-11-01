from collections import namedtuple
from base64 import b64encode

SOUND_FX_SRC = (
    "data:audio/wav;base64," + b64encode(open("assets/sfx.wav", "rb").read()).decode()
)
SOUND_FX = f"""
<audio autoplay>
    <source src="{SOUND_FX_SRC}" type="audio/wav">
</audio>
"""

GD_KEY = "gd"
CRIT_KEY = "crit"
INC_KEY = "inc"
ITEM_KEY = "item"
PRES_KEY = "pres"
PRES_ITEM_KEY = "presitem"
ALL_KEYS_DICT = {
    GD_KEY: 0,
    CRIT_KEY: 1e-2,
    INC_KEY: 1,
    ITEM_KEY: dict(),
    PRES_KEY: 0,
    PRES_ITEM_KEY: dict(),
}


Item = namedtuple("Item", ["name", "cost", "inflate", "inc", "crit"])
ITEM_DICT = {
    "功德倍增器": Item("功德倍增器", 100, 0.1, 0, 1.01),
    "功德加成器": Item("功德加成器", 100, 0.01, 1, 1),
    "半自动木鱼": Item("半自动木鱼", 300, 0.015, 5, 1),
    "机械转经轮": Item("机械转经轮", 1000, 0.02, 20, 1),
    "硅晶圆佛珠": Item("硅晶圆佛珠", 5000, 0.025, 200, 1),
}

PRES_ITEM_DICT = {
    "义体升级": Item("义体升级", 1e5, 0.5, 10, 0.01),
}
