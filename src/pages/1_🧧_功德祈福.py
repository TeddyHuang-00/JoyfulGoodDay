import sys

sys.path.append("..")
import streamlit as st
from utils import *

if GD_KEY not in st.session_state:
    st.session_state[GD_KEY] = 0

if CRIT_KEY not in st.session_state:
    st.session_state[CRIT_KEY] = 1e-2

if INC_KEY not in st.session_state:
    st.session_state[INC_KEY] = 1

if ITEM_KEY not in st.session_state:
    st.session_state[ITEM_KEY] = dict()

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
        f"花费 {cost} 功德，每次积累功德加 {item.inc} ，暴击率系数 {item.crit}",
    )
    if st.button(f"购买 {item.name}") and st.session_state[GD_KEY] >= cost:
        st.session_state[GD_KEY] -= cost
        st.session_state[ITEM_KEY][item.name] += 1
        st.session_state[INC_KEY] += item.inc
        st.session_state[CRIT_KEY] *= item.crit
        st.experimental_rerun()
