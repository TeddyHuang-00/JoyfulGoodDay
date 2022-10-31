import json
from base64 import b64decode, b64encode
from collections import namedtuple
from hashlib import md5

import numpy as np
import streamlit as st

Item = namedtuple("Item", ["name", "cost", "inflate", "inc", "crit"])

GD_KEY = "gd"
CRIT_KEY = "crit"
INC_KEY = "inc"
ITEM_KEY = "item"
ITEM_LIST = [
    Item("功德倍增器", 100, 0.1, 0, 1.01),
    Item("功德加成器", 100, 0.01, 1, 1),
    Item("半自动木鱼", 300, 0.015, 5, 1),
    Item("机械转经轮", 1000, 0.02, 20, 1),
]

if GD_KEY not in st.session_state:
    st.session_state[GD_KEY] = 0

if CRIT_KEY not in st.session_state:
    st.session_state[CRIT_KEY] = 1e-2

if INC_KEY not in st.session_state:
    st.session_state[INC_KEY] = 1

if ITEM_KEY not in st.session_state:
    st.session_state[ITEM_KEY] = dict()


st.title("Joyful Good Day")

JGD, SD = st.tabs(["积功德", "功德兑换"])

with JGD:
    _, C, _ = st.columns([5, 2, 5])
    with C:
        st.metric("功德量", st.session_state[GD_KEY])
        if st.button("大悲咒"):
            st.session_state[GD_KEY] += st.session_state[INC_KEY] * (
                1 + int(np.random.random() < st.session_state[CRIT_KEY])
            )

with SD:
    _, C, _ = st.columns([5, 2, 5])
    with C:
        st.metric("功德量", st.session_state[GD_KEY])
    for item in ITEM_LIST:
        if item.name not in st.session_state[ITEM_KEY]:
            st.session_state[ITEM_KEY][item.name] = 0
        cost = int(
            item.cost
            ** (1 + st.session_state[ITEM_KEY].get(item.name, 0) * item.inflate)
        )
        st.metric(
            item.name,
            st.session_state[ITEM_KEY][item.name],
            f"花费 {cost} 功德，每次积累功德加 {item.inc} ，暴击率系数 {item.crit}",
        )
        if st.button(f"购买 {item.name}") and st.session_state[GD_KEY] >= cost:
            st.session_state[GD_KEY] -= cost
            st.session_state[ITEM_KEY][item.name] += 1
            st.session_state[INC_KEY] += item.inc
            st.session_state[CRIT_KEY] *= item.crit
            st.experimental_rerun()
