import sys

sys.path.append("..")
import streamlit as st
from utils import *

st.session_state.update({**ALL_KEYS_DICT, **st.session_state.to_dict()})

st.title("机械化佛")

with st.expander("佛曰", expanded=True):
    st.write("🦾 化佛是下一段的修行")
    st.write("🙏 需要一定的功德量")
    st.write("❗️ 注意化佛前备份存档")


def recal():
    st.session_state[INC_KEY] = ALL_KEYS_DICT[INC_KEY]
    st.session_state[CRIT_KEY] = ALL_KEYS_DICT[CRIT_KEY]
    for name, item in ITEM_DICT.items():
        st.session_state[ITEM_KEY][item.name] = 0
    for name, item in PRES_ITEM_DICT.items():
        st.session_state[INC_KEY] *= st.session_state[ITEM_KEY][item.name] * item.inc
        st.session_state[CRIT_KEY] += item.crit


_, C, _ = st.columns([5, 2, 5])
with C:
    st.metric("功德量", st.session_state[GD_KEY])
for name, item in PRES_ITEM_DICT.items():
    if item.name not in st.session_state[ITEM_KEY]:
        st.session_state[ITEM_KEY][item.name] = 0
    cost = int(
        item.cost ** (1 + st.session_state[ITEM_KEY].get(item.name, 0) * item.inflate)
    )
    st.metric(
        item.name,
        st.session_state[ITEM_KEY][item.name],
        f"消 {cost} 功德，大悲咒效果重置并乘 {item.inc} ，运气重置并加 {item.crit}",
    )
    if st.button(f"请佛赐我 {item.name}") and st.session_state[GD_KEY] >= cost:
        st.session_state[GD_KEY] = 0
        st.session_state[ITEM_KEY][item.name] += 1
        recal()
        st.experimental_rerun()
