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
]

if GD_KEY not in st.session_state:
    st.session_state[GD_KEY] = 0

if CRIT_KEY not in st.session_state:
    st.session_state[CRIT_KEY] = 1e-4

if INC_KEY not in st.session_state:
    st.session_state[INC_KEY] = 1

if ITEM_KEY not in st.session_state:
    st.session_state[ITEM_KEY] = dict()


def load_save(save):
    for key, val in save.items():
        if key in st.session_state:
            st.session_state[key] = val
    st.experimental_rerun()


def check_integrity(txt: str):
    try:
        data: dict = json.loads(b64decode(txt).decode())
        hash_val = data.pop("hash")
        data = {k: v for k, v in sorted(data.items())}
        st.write(data)
        if (
            md5((json.dumps(data) + st.secrets["E_KEY"]).encode()).hexdigest()
            == hash_val
        ):
            load_save(data)
        else:
            return False
    except Exception as e:
        st.warning(e)
        return False


st.title("Joyful Good Day")

JGD, SD, CD = st.tabs(["积功德", "功德兑换", "功德簿"])

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

with CD:
    FORM_NAME = "功德簿"
    FORM_BTN_LABEL = "大记忆恢复术"
    FORM_BTN_KEY = f"FormSubmitter:{FORM_NAME}-{FORM_BTN_LABEL}"
    curr_state = st.session_state.to_dict()
    curr_state = {k: v for k, v in sorted(curr_state.items())}
    if FORM_BTN_KEY in st.session_state:
        curr_state.pop(FORM_BTN_KEY)
    curr_state["hash"] = md5(
        (json.dumps(curr_state) + st.secrets["E_KEY"]).encode()
    ).hexdigest()

    save = b64encode((json.dumps(curr_state)).encode()).decode()

    with st.form(FORM_NAME):
        raw = st.text_area(FORM_NAME, placeholder=save)
        if st.form_submit_button(FORM_BTN_LABEL) and raw:
            if not check_integrity(raw.strip()):
                st.error("你的功德簿被偷了，赛博佛祖记不得你前世的功德了")

    st.subheader("你这一世的功德簿，好好保管！")
    st.write(save)
