import datetime
import random
import time
import uuid
from Datahub import temp_all_exercises
from Views import show_exercise
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title=f"Exercise generator",layout="wide")#, page_icon = st.image(image))

temp_login_data={"admin":"admin"}
all_exercise_categories = ["arrays", "2D arrays","objects","loops"]
all_classes_names = ["GUI","PPJ","ABC"]




def up_step(new_step:str):
    st.session_state["step"]=new_step

if "logged" not in st.session_state:
    st.session_state["logged"] = ""

if "step" not in st.session_state:
    st.session_state["step"] = "main"
#Logging

if "logged" not in st.session_state or st.session_state["logged"]=="":

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
            up_step("add_exercise")
            st.experimental_rerun()

        add_new_ex_btn = st.button("Generate new pack")
        if add_new_ex_btn:
            up_step("generate_pack")
            st.experimental_rerun()

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

        temp_list_of_classes = ["-"]
        temp_list_of_classes.extend(all_classes_names)
        search_class = st.selectbox("Class:",temp_list_of_classes)

        search_author = st.text_input("Author:")

    list_all_col1, list_all_col2 = st.columns(2)
    with list_all_col1:
        st.button("Go back",on_click=up_step,args=["logged"])
    with list_all_col2:
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

    to_drop_ids_class = []
    if search_class!="-":
        for key,val in filtered_temp_all_exercises.items():
            if val["Class"] != search_class:
                to_drop_ids_class.append(key)



    to_drop_ids_general = []
    to_drop_ids_general.extend(to_drop_ids_cats)
    to_drop_ids_general.extend(to_drop_ids_idnum)
    to_drop_ids_general.extend(to_drop_ids_author)
    to_drop_ids_general.extend(to_drop_ids_class)

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
elif st.session_state["step"]=="add_exercise":
    add_col1,add_col2,dum_col = st.columns(3)
    with add_col1:
        st.button("Go back",on_click=up_step,args=["logged"],key=uuid.uuid4())
    with add_col2:
        st.subheader("     Add new exercise")

    st.markdown("<br>",unsafe_allow_html=True)

    add_ex_col1,add_ex_col2, add_ex_col3 = st.columns(3)


    with add_ex_col1:
        exercise_title = st.text_input("Exercise name:","Generic name")
    with add_ex_col2:
        exercise_author = st.text_input("Author:",st.session_state["logged"][:2])
    with add_ex_col3:
        exercise_class = search_class = st.selectbox("Class:",all_classes_names)

    exercise_content = st.text_area("Content of exercise goes here")
    exercise_answer = st.text_area("Answer of exercise goes here")
    st.text("Categories")
    categories_list = []

    categories_list=st.columns(len(all_exercise_categories))
    if "add_exercise_checkboxes" not in st.session_state:
        print("Reset stats")
        st.session_state["add_exercise_checkboxes"] = []
        st.session_state["add_exercise_checkboxes_bools"] = []
    for i in range(len(all_exercise_categories)):
        with categories_list[i]:
            #print(len(st.session_state["add_exercise_checkboxes"]))

            def update_checkbox_state(index_bool):
                st.session_state["add_exercise_checkboxes_bools"][index_bool] = not st.session_state["add_exercise_checkboxes_bools"][index_bool]

            fresh_bool_value = False
            if len(st.session_state["add_exercise_checkboxes_bools"]) == len(all_exercise_categories):
                fresh_bool_value=st.session_state["add_exercise_checkboxes_bools"][i]

            checkbtn = st.checkbox(all_exercise_categories[i],key=uuid.uuid4(),on_change=update_checkbox_state,args=[i],
                                   value=fresh_bool_value)




            if len(st.session_state["add_exercise_checkboxes_bools"]) != len(all_exercise_categories):
                st.session_state["add_exercise_checkboxes"].append(checkbtn)
                st.session_state["add_exercise_checkboxes_bools"].append(False)
            # if checkbtn:
            #     print(f"PRE {st.session_state['add_exercise_checkboxes_bools']} ")
            #     #st.session_state["add_exercise_checkboxes_bools"][i]=not st.session_state["add_exercise_checkboxes_bools"][i]
            #     print(f"POST {st.session_state['add_exercise_checkboxes_bools']} ")
            #     print(f"Changed state for {i}")
            #     print(st.session_state["add_exercise_checkboxes_bools"])




    st.warning("Functionality not tested implemented")
    creation_date = datetime.datetime.now().strftime("%d-%m-%Y")
    modification_date = creation_date


    def add_new_exercise():
        temp_id = max(temp_all_exercises.keys())+1
        temp_categories=[all_exercise_categories[x] for x in range(len(all_exercise_categories)) if st.session_state["add_exercise_checkboxes_bools"][x]]
        all_exercise_categories[temp_id]={"ID" : temp_id,
     "Title":exercise_title,
     "Creation_date" : creation_date,
     "Modification_Date" : modification_date,
     "Content":exercise_content,
     "Solution":exercise_answer,
     "Author":exercise_author,
     "Categories":temp_categories,
     "Class": exercise_class
                                          }


        st.session_state["add_exercise_checkboxes"]=[]
        st.session_state["add_exercise_checkboxes_bools"] = []

        def up_content():
            #main.temp_all_exercises[ex["ID"]]["Content"] = mod_content
            #st.session_state["update_exercise"] = (ex["ID"],mod_content)
            with st.spinner('Wait for it...'):
                time.sleep(1)
            st.success('Done!')
            time.sleep(1)
            up_step("logged")
        #todo add information about saving and thats all.
        up_content()
    st.button("Save",on_click=add_new_exercise,args=[], key=uuid.uuid4())

            # with ex_col_3_1:
            #
            #     a = st.button(f"Show{random.randint(0,100)}")
            # with ex_col_3_2:
            #     b = st.button(f"Answer{random.randint(0,100)}")

elif st.session_state["step"] =="generate_pack":
    st.session_state["generate_pack_lock"]=True
    print("gnerate_pack")
    add_col1, add_col2, dum_col = st.columns(3)
    with add_col1:
        st.button("Go back", on_click=up_step, args=["logged"], key=uuid.uuid4())
    with add_col2:
        st.subheader("     Generate exercise pack")

    st.markdown("<br>", unsafe_allow_html=True)

    gen_col1,gen_col2, gen_col3 = st.columns(3)
    with gen_col1:
        pack_name = st.text_input("Name/Title of the pack","ex. GUI_XII")
    with gen_col2:
        amount_of_exercises = st.number_input("Number of exercises",step=1,max_value=8,min_value=1)
    with gen_col3:
        class_of_exercise = st.selectbox("Class:",all_classes_names)
    if "gen_exercise_checkboxes" not in st.session_state:

        st.session_state["gen_exercise_checkboxes"] = []
        st.session_state["gen_exercise_checkboxes_bools"] = []

    categories_list = st.columns(len(all_exercise_categories))
    for i in range(len(all_exercise_categories)):
        with categories_list[i]:
            #print(len(st.session_state["add_exercise_checkboxes"]))

            def update_checkbox_state(index_bool):
                st.session_state["gen_exercise_checkboxes_bools"][index_bool] = not st.session_state["gen_exercise_checkboxes_bools"][index_bool]

            fresh_bool_value = False
            if "gen_exercise_checkboxes_bools" not in st.session_state:
                st.session_state["gen_exercise_checkboxes_bools"]=[]

            if "gen_exercise_checkboxes" not in st.session_state:
                st.session_state["gen_exercise_checkboxes"]=[]

            if len(st.session_state["gen_exercise_checkboxes_bools"]) == len(all_exercise_categories):
                fresh_bool_value=st.session_state["gen_exercise_checkboxes_bools"][i]

            checkbtn = st.checkbox(all_exercise_categories[i],key=uuid.uuid4(),on_change=update_checkbox_state,args=[i],
                                   value=fresh_bool_value)

            if len(st.session_state["gen_exercise_checkboxes_bools"]) != len(all_exercise_categories):
                st.session_state["gen_exercise_checkboxes"].append(checkbtn)
                st.session_state["gen_exercise_checkboxes_bools"].append(False)

    def generate_pack():

        temp_generated_exercises = list(temp_all_exercises.values())
        print(temp_generated_exercises)
        random.shuffle(temp_generated_exercises)
        #print(temp_generated_exercises)
        selected_categories =[]
        #print(st.session_state["add_exer"])

        #Filter by exercise
        if any(st.session_state["gen_exercise_checkboxes_bools"]):
            choosen_gen_cats = []
            for bool,ind in zip(st.session_state["gen_exercise_checkboxes_bools"],list(range(len(all_exercise_categories)))):
                print(bool)
                if bool:
                    choosen_gen_cats.append(all_exercise_categories[ind])
            print(f"Choosen cats: {choosen_gen_cats}")
            #temp_generated_exercises = list(filter(lambda ex: all([sub_x in selected_categories for sub_x in ex["Categories"]]),temp_generated_exercises))
            temp_generated_exercises = [x for x in temp_generated_exercises if all([y in x["Categories"] for y in choosen_gen_cats])]
        else:
            print("No question category filter used")
        print(f"1> {len(temp_generated_exercises)}")
        #filter by class
        temp_generated_exercises = [x for x in temp_generated_exercises if x["Class"]==class_of_exercise]
        print(f"2> {len(temp_generated_exercises)}")
        #filter by amount
        temp_generated_exercises = temp_generated_exercises[:amount_of_exercises]
        print(f"3> {len(temp_generated_exercises)}")
        if len(temp_generated_exercises)==0:
            st.error("Because database is limited, there is no enough exercises for this request")
        else:
            if st.session_state["generate_pack_lock"]:
                st.session_state["generate_pack_lock"] = False
            else:
                st.success("Exercises were generated. But for now there is no PDF - you have to trust me")

            pdf = FPDF('P', 'mm', 'A4')
            pdf.add_page()
            pdf.set_font('Arial', 'B', 25)
            pdf.cell(190, 10, f'{pack_name}', 0, 1, 'C')
            pdf.set_font('Arial', 'B', 15)
            for num in range(len(temp_generated_exercises)):
                this_ex = temp_generated_exercises[num]
                pdf.ln(5)
                pdf.cell(40, 10, f': {this_ex["Title"]}', 0, 1)
                pdf.set_font('Arial', '', 12)
                pdf.cell(70, 10, f'Content: {this_ex["Content"]}', 0, 1)
                #todo add rest of the info
                #todo make sure formatting is correct
                #todo add minor visual enhancements


        #warning if not enough exercises
            return pdf

    #st.button("Generate!",key=uuid.uuid4(),on_click=generate_pack,args=[])
    download_button = st.download_button(f"Download PDF pack",
                                                 data=generate_pack().output(dest="S").encode("latin-1"),
                                                 file_name=f"{pack_name}_exercises.pdf")