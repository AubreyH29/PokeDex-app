import streamlit as st
import json
from openai import OpenAI

#api key here

stats = ["HP", "ATTACK", "DEFENSE", "SPECIAL ATTACK", "SPECIAL DEFENSE", "SPEED" ]
details = ["HEIGHT", "WEIGHT", "GENDER", "CATEGORY"]
system_prompt = """
Generate a pokedex from the Pokemon franchise and save them into a dictionary. The user should be allowed view the existing entries or add a new entry. Return a JSON using the following template:
pages_json
{
    "NAME": a name,
    "NUMBER": a 4 digit entry number. Use official Pokedex number where possible,
    "STATS": a dictionary containing the following{
        "HP": an HP value from 0 to 15 inclusive,
        "ATTACK": an attack value from 0 to 15 inclusive,
        "DEFENSE": a defense value from 0 to 15 inclusive,
        "SPECIAL ATTACK": a special attack value from 0 to 15 inclusive,
        "SPECIAL DEFENSE": a special defense value from 0 to 15 inclusive,       
        "SPEED": a speed value from 0 to 15 inclusive},
    "SPECIAL SKILL": one sentence describing its specialized skill. Use the official Pokedex wherever possible,
    "DETAILS": a dictionary containing the following{
        "HEIGHT": a height (in feet and inches),
        "WEIGHT": a weight (in pounds),
        "GENDER": a gender (male or female),
        "CATEGORY": a category (the type of creature),
        "ABILITY": [list of moves that it can do]"},
    "TYPE":[list of types],
    "WEAK TYPES": [list of weakness types],
    "EVOLUTIONS": for example, "caterpie #0010 --> metapod #0011 --> butterfree #0012"
}
"""

def write_pokedex(pages_json):
    st.write("# " + pages_json["NAME"] + " # " + str(pages_json["NUMBER"]))        
    st.write("## STATS:")
    for i in stats:
        st.write("**" +i + ":** " + str(pages_json["STATS"][i]) +"/15")
    st.write("## SPECIAL_SKILL:")
    st.write(pages_json["SPECIAL SKILL"])
    st.write("## DETAILS:")
    for i in details:
        st.write("**" +i + ":** " + pages_json["DETAILS"][i] +"/15")
    st.write("**ABILITY:**")
    for i in pages_json["DETAILS"]["ABILITY"]:
        st.write(i)
    st.write("## TYPE:")
    for i in pages_json["TYPE"]:
        st.write(i)
    st.write("## WEAK TYPE:")
    for i in pages_json["WEAK TYPES"]:
        st.write(i)
    st.write("## EVOLUTIONS:")
    st.write(pages_json["EVOLUTIONS"])


def get_json_response(system_prompt, user_prompt):
    """
    Sends a prompt to the ChatGPT API where it will return a JSON response.
    ChatGPT will not remember any prior conversations.

    Parameters:
    - system_prompt (str): Directions on how ChatGPT should act. Remember that it must request for a JSON response and include a JSON template.
    - user_prompt (str): A prompt from the user.
    
    Returns:
    - (dict): A dictionary containing ChatGPT's response in the requested JSON format.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return json.loads(response.choices[0].message.content)


if 'pokedex' not in st.session_state:
    st.session_state['pokedex'] = {}
options = ["select"]+ list(st.session_state["pokedex"].keys())

st.write("Welcome to the Pokedex!")
st.write("What would you like to do?")

select_box = st.selectbox("View generated Pokedex entries", options)

with st.form("generate"):
    name = st.text_input("Enter the name of a Pokemon to generate an entry for")
    submit = st.form_submit_button("Submit")
    if submit and name != "":
        st.session_state["pokedex"][name] = get_json_response(system_prompt, name)
        st.rerun()
if select_box != "select":
    write_pokedex(st.session_state["pokedex"][select_box])
