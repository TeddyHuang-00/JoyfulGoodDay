import numpy as np
import streamlit as st

from utils import *

st.set_page_config(initial_sidebar_state="expanded", page_title="积功德", page_icon="🙏")

st.session_state.update({**ALL_KEYS_DICT, **st.session_state.to_dict()})

st.title("积功德")

_, C, _ = st.columns([5, 2, 5])
with C:
    st.metric("功德量", st.session_state[GD_KEY])
    if st.button("大悲咒", type="primary"):
        st.session_state[GD_KEY] += st.session_state[INC_KEY] * (
            1 + int(np.random.random() < st.session_state[CRIT_KEY])
        )

with st.expander("佛曰"):
    st.write("🙏 功德无量，善心无边。")
    st.write("❔ 若不知道要干什么，就来这里念大悲咒积功德吧。")
    st.write("🧧 功德可以用来祈福兑换一些装备，让你的功德量更快地增长。")
    st.write("📖 侧边栏的功德簿可以保存你的数据，切记勤备份，佛不会记得你前世的功德。")
