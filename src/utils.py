from collections import namedtuple

GD_KEY = "gd"
CRIT_KEY = "crit"
INC_KEY = "inc"
ITEM_KEY = "item"
ALL_KEYS_DICT = {
    GD_KEY: 0,
    CRIT_KEY: 1e-2,
    INC_KEY: 1,
    ITEM_KEY: dict(),
}


Item = namedtuple("Item", ["name", "cost", "inflate", "inc", "crit"])
ITEM_LIST = [
    Item("功德倍增器", 100, 0.1, 0, 1.01),
    Item("功德加成器", 100, 0.01, 1, 1),
    Item("半自动木鱼", 300, 0.015, 5, 1),
    Item("机械转经轮", 1000, 0.02, 20, 1),
    Item("硅晶圆佛珠", 5000, 0.025, 200, 1),
]
