import random
import uuid
from Datahub import temp_all_exercises
from Views import show_exercise
import streamlit as st

st.set_page_config(page_title=f"Exercise generator",layout="wide")#, page_icon = st.image(image))

temp_login_data={"admin":"admin"}
all_exercise_categories = ["arrays", "2D arrays","objects","loops"]




def up_step(new_step:str):
    st.session_state["step"]=new_step

if "logged" not in st.session_state:
    st.session_state["logged"] = ""

if "step" not in st.session_state:
    st.session_state["step"] = "main"
#Logging

if st.session_state["logged"]=="":

    def login_action():
        if login =="" and password=="":
            return
        if login in temp_login_data.keys() and password==temp_login_data[login]:
            #st.success("Login succesfull")
            st.session_state["logged"]=login
            up_step("logged")
        else:
            st.error("Login or password are incorrect")

    log_col1,log_col2,log_col3 = st.columns(3)
    with log_col2:
        st.title("Exercise generator", )
        st.markdown("<br><br>", unsafe_allow_html=True)

        login = st.text_input("Login:")
        password = st.text_input("Password:")


        login_btn = st.button("Login",on_click=login_action)

if st.session_state["step"]=="logged":

    gen_col1,gen_col2,gen_col3 = st.columns(3)
    with gen_col2:
        st.title(f"Hello {st.session_state['logged']}")
        st.markdown("<br><br>", unsafe_allow_html=True)
        all_records_btn = st.button("All records")
        if all_records_btn:
            up_step("all_records")
            st.experimental_rerun()


        add_new_ex_btn = st.button("Add new exercise")
        if add_new_ex_btn:
            up_step("add_new")

        add_new_ex_btn = st.button("Generate new pack")
        if add_new_ex_btn:
            up_step("generate_pack")

elif st.session_state["step"]=="all_records":

    #checking for any updates
    if "update_exercise" in st.session_state and st.session_state["update_exercise"] != ():
        temp_all_exercises[st.session_state["update_exercise"][0]]["Content"]=st.session_state["update_exercise"][1]


    st.markdown(
        """
    <style>
     button[kind]{
        height: 5px;
        display: inline-block;
        font-size: 5px; !important;
        padding-top: -10px !important;
        padding-bottom: -10px !important;
        margin: -10px;
    }
    </style>
    """,
        unsafe_allow_html=True
    )
    with st.sidebar:

        search_id_input = st.number_input("Exercise ID:",step=1,format="%d")


        all_search_checkboxes = []
        for cat in all_exercise_categories:
            temp_search_checkbox = st.checkbox(cat)
            all_search_checkboxes.append(temp_search_checkbox)

        search_author = st.text_input("Author:")

    st.subheader("List of all exercises")
    # exercises_df = {
    #     "Id" :[x["ID"] for x in temp_all_exercises],
    #     "Titles":[x["Title"] for x in temp_all_exercises],
    #     "Author":[x["Author"] for x in temp_all_exercises],
    #     "Mod Date": [x["Modification_Date"] for x in temp_all_exercises],
    #
    # }
    #
    # st.dataframe(exercises_df)

    #todo add filters

    filtered_temp_all_exercises = temp_all_exercises
    to_drop_ids_general=[]
    to_drop_ids_idnum = []
    if search_id_input != 0:
        print("Filtering")
        try:
            #filtered_temp_all_exercises={search_id_input:temp_all_exercises[search_id_input]}
            to_drop_ids_idnum = list(filtered_temp_all_exercises.keys())
            to_drop_ids_idnum.remove(search_id_input)
            print("Filtered")
        except:
            pass
    else:
        to_drop_ids=[]


    #filtering by checkboxes
    choosen_cats = []
    to_drop_ids_cats = []
    if any(all_search_checkboxes):
        for check, num in zip(all_search_checkboxes,range(len(all_search_checkboxes))):
            if check:
                choosen_cats.append(all_exercise_categories[num])

        for key,val in filtered_temp_all_exercises.items():
            if not all([x in val["Categories"] for x in choosen_cats]):
                to_drop_ids_cats.append(key)

        # for todrop_id in to_drop_ids:
        #     del filtered_temp_all_exercises[todrop_id]

        print(f"Choosen: {choosen_cats}")

    else:
        to_drop_ids_cats=[]

    to_drop_ids_author=[]
    if search_author != "":
        for key,val in filtered_temp_all_exercises.items():
            if val["Author"] != search_author:
                to_drop_ids_author.append(key)
    else:
        to_drop_ids_author=[]


    to_drop_ids_general = []
    to_drop_ids_general.extend(to_drop_ids_cats)
    to_drop_ids_general.extend(to_drop_ids_idnum)
    to_drop_ids_general.extend(to_drop_ids_author)

    ex_col1, ex_col2,ex_col3 = st.columns(3)
    for key,ex in filtered_temp_all_exercises.items():
        st.text(" ")
        if len(to_drop_ids_general)==len(filtered_temp_all_exercises):
            st.warning("No records match your criteria")
            break
        if key in to_drop_ids_general:
            continue
        with ex_col1:
            ex_col_1_1,ex_col_1_2 = st.columns(2)
            with ex_col_1_1:
                st.text(ex["ID"])
            with ex_col_1_2:
                st.text(ex["Title"])
        with ex_col2:
            ex_col_2_1, ex_col_2_2 = st.columns(2)
            with ex_col_2_1:
                st.text(ex["Author"])
            with ex_col_2_2:
                #st.text(ex["Modification_Date"])
                st.markdown(ex["Modification_Date"],unsafe_allow_html=True)
        with ex_col3:
            ex_col_3_1, ex_col_3_2 = st.columns(2)
            pholer = ex_col_3_1.empty()

            def show_ex():
                up_step(f"edit_ex_{ex['ID']}")


            act_btn_show = pholer.button("show",key = uuid.uuid4(), on_click= up_step,args=[f"show_ex_{ex['ID']}"])

            pholer2 = ex_col_3_2.empty()

            def edit_ex():
                up_step(f"edit_ex_{ex['ID']}")


            act_btn_edit = pholer2.button("edit",on_click=up_step,args=[f"edit_ex_{ex['ID']}"],key = uuid.uuid4())
            #if pholer2.button:
            #    up_step(f"show_ex_{ex['ID']}")
            #    print("PRESS")
            #    st.experimental_rerun()

elif "show_ex" in st.session_state["step"]:
    print("TET")
    show_exercise(temp_all_exercises[int(st.session_state["step"].split("_")[-1])])

elif "edit_ex" in st.session_state["step"]:
    show_exercise(temp_all_exercises[int(st.session_state["step"].split("_")[-1])],True)
    #show_exercise([x for x in temp_all_exercises.values() if str(x["ID"])==st.session_state["step"].split("_")[2]][0])

    #todo here
            # with ex_col_3_1:
            #
            #     a = st.button(f"Show{random.randint(0,100)}")
            # with ex_col_3_2:
            #     b = st.button(f"Answer{random.randint(0,100)}")

