import streamlit as st
import pandas as pd

from PIL import Image
def load_and_resize(path):
    img = Image.open(path)
    img = img.resize((300, 300))
    return img

from data.questions import questions

st.set_page_config(
    page_title="Which Cat Are You?",
    page_icon="🐱"
)

st.title("🐱 Which Cat Are You?")
st.write("Answer the questions below to discover your cat personality!")

# =========================
# Session State
# =========================

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

current = st.session_state.current_question

# =========================
# QUIZ PAGE
# =========================

if current < len(questions):

    q = questions[current]

    progress = (current + 1) / len(questions)

    st.progress(progress)

    st.subheader(
        f"Question {current + 1} of {len(questions)}"
    )

    answer = st.radio(
        q["question"],
        list(q["options"].keys()),
        index=None,
        key=f"question_{current}"
    )

    if st.button("Next ➡️"):

        if answer is None:
            st.warning(
                "Please select an answer before continuing."
            )

        else:
            st.session_state.answers[current] = answer
            st.session_state.current_question += 1
            st.rerun()

# =========================
# RESULT PAGE
# =========================

else:

    scores = {
        "Chaos Cat": 0,
        "Sleepy Cat": 0,
        "Study Cat": 0,
        "Party Cat": 0,
        "Mystery Cat": 0
    }

    for index, answer in st.session_state.answers.items():

        question = questions[index]

        cat = question["options"][answer]

        scores[cat] += 1

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary_cat = sorted_scores[0][0]
    secondary_cat = sorted_scores[1][0]

    max_score = max(scores.values())

    winners = [
        cat
        for cat, score in scores.items()
        if score == max_score
    ]

    display_cat = primary_cat

    descriptions = {
        "Chaos Cat":
            "🍊 You are full of energy and always looking for adventure. Life is never boring with you!",

        "Sleepy Cat":
            "😴 You enjoy comfort, peace, and relaxation. A perfect day includes plenty of rest.",

        "Study Cat":
            "📚 You are curious, intelligent, and love learning new things.",

        "Party Cat":
            "🎉 You are social, friendly, and enjoy spending time with people.",

        "Mystery Cat":
            "🌙 You are independent, creative, and have your own unique world."
    }

    image_paths = {
        "Chaos Cat": "assets/chaos_cat.jpeg",
        "Sleepy Cat": "assets/sleepy_cat.JPG",
        "Study Cat": "assets/study_cat.JPG",
        "Party Cat": "assets/party_cat.JPG",
        "Mystery Cat": "assets/mystery_cat.JPG"
    }

    fun_facts = {
        "Chaos Cat":
            "🍊 Chaos Cats are responsible for 99% of imaginary broken flower pots.",

        "Sleepy Cat":
            "😴 Sleepy Cats can fall asleep anywhere in under 10 seconds.",

        "Study Cat":
            "📚 Study Cats secretly enjoy learning random facts at 2 AM.",

        "Party Cat":
            "🎉 Party Cats somehow know everyone in the room.",

        "Mystery Cat":
            "🌙 Nobody knows where Mystery Cats disappear to."
    }

    # =========================
    # RESULT HEADER
    # =========================

    if len(winners) == 1:

        st.success(
            f"🐱 You are {primary_cat}!"
        )

    else:

        st.success(
            f"🐱 You're a mix of {' & '.join(winners)}!"
        )

    st.subheader("✨ Personality Analysis")

    st.write(f"**Primary Personality:** {primary_cat}")

    if len(winners) > 1:
        st.write(f"**Secondary Personality:** {secondary_cat}")
        st.info("You have a balanced personality!")

    # =========================
    # IMAGE
    # =========================

    if len(winners) == 1:

        st.image(
          load_and_resize(image_paths[primary_cat])
        )       

    else:

        cols = st.columns(len(winners))

        for i, cat in enumerate(winners):

            with cols[i]:

                st.image(
                    load_and_resize(image_paths[cat])
                )

                st.caption(cat)

    # =========================
    # DESCRIPTION
    # =========================

    if len(winners) == 1:
        st.write(

            descriptions[primary_cat]
        )
    else:
        st.subheader("🐾 Your Cat Personalities")
        for cat in winners:
            st.markdown(f"### {cat}")
            st.write(
                descriptions[cat]
            )

    # =========================
    # FUN FACT
    # =========================

    if len(winners) == 1:

        st.info(
            fun_facts[primary_cat]
        )
    else:
        st.subheader("✨ Fun Facts")
        for cat in winners:
            st.info(
                f"**{cat}**\n\n{fun_facts[cat]}"
            )
        
    # =========================
    # CHART
    # =========================

    st.subheader("📈 Personality Chart")

    df = pd.DataFrame(
        list(scores.items()),
        columns=["Cat", "Score"]
    )

    st.bar_chart(
        df.set_index("Cat")
    )

    # =========================
    # PERCENTAGE
    # =========================

    st.subheader("📊 Personality Breakdown")

    total = sum(scores.values())

    for cat, score in scores.items():

        percentage = (score / total) * 100

        st.write(
            f"{cat}: {percentage:.1f}%"
        )

    st.divider()

    # =========================
    # RETAKE
    # =========================

    if st.button("🔄 Retake Quiz"):

        st.session_state.current_question = 0
        st.session_state.answers = {}

        st.rerun()