import json
from base64 import b64decode, b64encode
from hashlib import md5

import streamlit as st

st.set_page_config(initial_sidebar_state="expanded", page_title="功德簿", page_icon="📖")


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


st.title("功德簿")

FORM_NAME = "向佛诉说你的前世功德"
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
