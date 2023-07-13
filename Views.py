import time

import streamlit as st



def up_step(new_step:str):
    st.session_state["step"]=new_step


def show_exercise(ex:dict, edit=False):
    show_title_col1, show_title_col2, show_title_col3 = st.columns(3)

    with show_title_col1:
        st.button("Go back", on_click=up_step,args=["all_records"])

    with show_title_col2:
        st.subheader(ex["Title"])
    show_col1,show_col2,show_col3, show_col4 = st.columns(4)
    with show_col1:
        st.text(f"ID:{ex['ID']}")
    with show_col2:
        st.text(f"Author:{ex['Author']}")
    with show_col3:
        st.text(f"Creation date:{ex['Creation_date']}")
    with show_col4:
        st.text(f"Modification date:{ex['Modification_Date']}")

    if edit:
        mod_content = st.text_input("Content",ex['Content'])
        def up_content():
            #main.temp_all_exercises[ex["ID"]]["Content"] = mod_content
            st.session_state["update_exercise"] = (ex["ID"],mod_content)
            with st.spinner('Wait for it...'):
                time.sleep(1)
            st.success('Done!')
            time.sleep(1)
            up_step("all_records")

        st.button("Save",on_click=up_content,args=[])
    else:
        st.text(f"Content:{ex['Content']}")

