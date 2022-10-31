import json
from base64 import b64decode, b64encode
from collections import namedtuple

import numpy as np
import streamlit as st

Item = namedtuple("Item", ["name", "cost", "inc", "crit"])

GD_KEY = "gd"
CRIT_KEY = "crit"
INC_KEY = "inc"
ITEM_KEY = "item"
ITEM_LIST = [
    Item("功德加成器", 100, 1, 1),
    Item("功德倍增器", 100, 0, 0.9999),
]

if GD_KEY not in st.session_state:
    st.session_state[GD_KEY] = 0

if CRIT_KEY not in st.session_state:
    st.session_state[CRIT_KEY] = 1e-4

if INC_KEY not in st.session_state:
    st.session_state[INC_KEY] = 1

if ITEM_KEY not in st.session_state:
    st.session_state[ITEM_KEY] = dict()

st.title("Joyful Good Day")
st.subheader("积功德")

st.metric("功德量", st.session_state[GD_KEY])


if st.button("今日功德", key="jgd"):
    st.session_state[GD_KEY] += st.session_state[INC_KEY] * (
        1 + int(np.random.random() < st.session_state[CRIT_KEY])
    )

st.subheader("购买道具")

for item in ITEM_LIST:
    if item.name not in st.session_state[ITEM_KEY]:
        st.session_state[ITEM_KEY][item.name] = 0
    st.metric(
        item.name,
        st.session_state[ITEM_KEY][item.name],
        f"花费 {item.cost} 功德，每次积累功德加 {item.inc} ，暴击率系数 {item.crit}",
    )
    if (
        st.button(
            f"购买 {item.name}",
            key=item.name,
        )
        and st.session_state[GD_KEY] >= item.cost
    ):
        st.session_state[GD_KEY] -= item.cost
        st.session_state[ITEM_KEY][item.name] += 1
        st.session_state[INC_KEY] += item.inc
        st.session_state[CRIT_KEY] **= item.crit
