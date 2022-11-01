import sys

sys.path.append("..")
import streamlit as st
from utils import *

st.session_state.update({**ALL_KEYS_DICT, **st.session_state.to_dict()})

st.title("功德祈福")

_, C, _ = st.columns([5, 2, 5])
with C:
    st.metric("功德量", st.session_state[GD_KEY])
for item in ITEM_LIST:
    if item.name not in st.session_state[ITEM_KEY]:
        st.session_state[ITEM_KEY][item.name] = 0
    cost = int(
        item.cost ** (1 + st.session_state[ITEM_KEY].get(item.name, 0) * item.inflate)
    )
    st.metric(
        item.name,
        st.session_state[ITEM_KEY][item.name],
        f"消 {cost} 功德，大悲咒效果加 {item.inc} ，运气乘 {item.crit}",
    )
    if st.button(f"请佛赐我 {item.name}") and st.session_state[GD_KEY] >= cost:
        st.session_state[GD_KEY] -= cost
        st.session_state[ITEM_KEY][item.name] += 1
        st.session_state[INC_KEY] += item.inc
        st.session_state[CRIT_KEY] *= item.crit
        st.experimental_rerun()
