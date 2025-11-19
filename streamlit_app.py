import streamlit as st

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(
    page_title="BNSS MCQ Test",
    page_icon="⚖️",
)

TOTAL_WRONG_ALLOWED = 3
MARKS_CORRECT = 1.0
MARKS_WRONG = -0.5

GOLD_THRESHOLD = 80   # >= 80%
SILVER_THRESHOLD = 60 # >= 60%
BRONZE_THRESHOLD = 40 # >= 40%


# ----------------------------
# QUESTION BANK
# ----------------------------
QUESTIONS = [
    {
        "question": "1. BNSS replaces which earlier law?",
        "options": [
            "A. Indian Penal Code",
            "B. Code of Criminal Procedure, 1973",
            "C. Indian Evidence Act, 1872",
            "D. Police Act, 1861",
        ],
        "answer_index": 1,
    },
    {
        "question": "2. Maximum permissible police custody under BNSS (in a case requiring further custody) is—",
        "options": [
            "A. 15 days",
            "B. 30 days",
            "C. 60 days",
            "D. 90 days",
        ],
        "answer_index": 3,
    },
    {
        "question": "3. BNSS mandates that the judgment shall be delivered within how many days after reservation?",
        "options": [
            "A. 7 days",
            "B. 14 days",
            "C. 30 days",
            "D. 45 days",
        ],
        "answer_index": 1,
    },
    {
        "question": "4. Under BNSS, zero-FIR provisions are included under which section?",
        "options": [
            "A. Section 173",
            "B. Section 173(3)",
            "C. Section 173(1)",
            "D. Section 174",
        ],
        "answer_index": 1,
    },
    {
        "question": "5. The provision for trial in absentia of proclaimed offenders is introduced in which section of BNSS?",
        "options": [
            "A. Section 357",
            "B. Section 356",
            "C. Section 258",
            "D. Section 230",
        ],
        "answer_index": 1,
    },
    {
        "question": "6. BNSS allows electronic mode for—",
        "options": [
            "A. FIR filing",
            "B. Search & seizure",
            "C. Summons, warrants & examination of witnesses",
            "D. None of the above",
        ],
        "answer_index": 2,
    },
    {
        "question": "7. The maximum permissible period for completing investigation for offences punishable with 10 years or more under BNSS is—",
        "options": [
            "A. 30 days",
            "B. 60 days",
            "C. 90 days",
            "D. 180 days",
        ],
        "answer_index": 3,
    },
    {
        "question": "8. BNSS introduces mandatory forensic investigation for offences punishable with—",
        "options": [
            "A. More than 3 years",
            "B. More than 5 years",
            "C. More than 7 years",
            "D. More than 10 years",
        ],
        "answer_index": 2,
    },
    {
        "question": "9. \"Plea Bargaining\" provisions under BNSS correspond to which Part of CrPC?",
        "options": [
            "A. Chapter XXIA",
            "B. Chapter XXI",
            "C. Chapter XIX",
            "D. Chapter XXV",
        ],
        "answer_index": 0,
    },
    {
        "question": "10. The right of the accused to meet an advocate during interrogation (not throughout) is guaranteed under BNSS Section—",
        "options": [
            "A. 40",
            "B. 41",
            "C. 42",
            "D. 43",
        ],
        "answer_index": 2,
    },
    {
        "question": "11. Medical examination of a woman shall be conducted by—",
        "options": [
            "A. A government medical officer only",
            "B. A woman medical practitioner",
            "C. Any registered doctor",
            "D. SHO of the police station",
        ],
        "answer_index": 1,
    },
    {
        "question": "12. BNSS mandates audio-video recording of search & seizure under Section—",
        "options": [
            "A. 105",
            "B. 106",
            "C. 107",
            "D. 108",
        ],
        "answer_index": 0,
    },
    {
        "question": "13. The timeline to provide a copy of FIR to the victim in electronic mode is—",
        "options": [
            "A. 24 hours",
            "B. 48 hours",
            "C. 72 hours",
            "D. 7 days",
        ],
        "answer_index": 0,
    },
    {
        "question": "14. Period for filing charge sheet when the accused is in custody for offences punishable up to 10 years is—",
        "options": [
            "A. 60 days",
            "B. 90 days",
            "C. 120 days",
            "D. 180 days",
        ],
        "answer_index": 1,
    },
    {
        "question": "15. Under BNSS, a person can be declared a 'Proclaimed Offender' for—",
        "options": [
            "A. All offences",
            "B. Only economic offences",
            "C. Heinous offences or those punishable with 10+ years",
            "D. Petty offences",
        ],
        "answer_index": 2,
    },
]

TOTAL_QUESTIONS = len(QUESTIONS)


# ----------------------------
# HELPERS
# ----------------------------
def init_state():
    """Initialize all session_state variables."""
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "user_answers" not in st.session_state:
        # store index of selected option (or None)
        st.session_state.user_answers = [None] * TOTAL_QUESTIONS
    if "correct_count" not in st.session_state:
        st.session_state.correct_count = 0
    if "wrong_count" not in st.session_state:
        st.session_state.wrong_count = 0
    if "score" not in st.session_state:
        st.session_state.score = 0.0
    if "test_finished" not in st.session_state:
        st.session_state.test_finished = False


def calculate_percentage(score: float) -> float:
    max_marks = TOTAL_QUESTIONS * MARKS_CORRECT
    # allow negative score but clamp percentage at minimum 0 for display
    percent = (score / max_marks) * 100
    return max(percent, 0.0)


def get_medal(percent: float) -> str:
    if percent >= GOLD_THRESHOLD:
        return "🥇 Gold"
    elif percent >= SILVER_THRESHOLD:
        return "🥈 Silver"
    elif percent >= BRONZE_THRESHOLD:
        return "🥉 Bronze"
    else:
        return "🙂 Keep Practicing"


def reset_test():
    """Reset the whole test."""
    for key in [
        "current_q",
        "user_answers",
        "correct_count",
        "wrong_count",
        "score",
        "test_finished",
    ]:
        if key in st.session_state:
            del st.session_state[key]
    init_state()


# ----------------------------
# MAIN APP
# ----------------------------
def main():
    init_state()

    st.title("⚖️ BNSS MCQ Test")
    st.write(
        """
This is a 15-question BNSS test with **negative marking**:

- ✅ Correct answer: **+1 mark**
- ❌ Wrong answer: **-0.5 mark**
- After **3 wrong answers**, you are **barred from attempting further questions**.
- Medal is awarded based on your final **percentage**.
        """
    )

    # If wrong answers reached the limit, ensure test is marked finished
    if st.session_state.wrong_count >= TOTAL_WRONG_ALLOWED:
        st.session_state.test_finished = True

    # ----------------------------
    # SIDEBAR - PROGRESS
    # ----------------------------
    with st.sidebar:
        st.header("📊 Progress")

        attempted = st.session_state.correct_count + st.session_state.wrong_count
        percent_attempted = attempted / TOTAL_QUESTIONS if TOTAL_QUESTIONS else 0.0

        st.text(f"Question: {st.session_state.current_q + 1} / {TOTAL_QUESTIONS}")
        st.progress(percent_attempted)

        st.write(f"✅ Correct: **{st.session_state.correct_count}**")
        st.write(f"❌ Wrong: **{st.session_state.wrong_count}**")
        st.write(f"🔢 Score: **{st.session_state.score:.2f}**")

        remaining_wrongs = max(TOTAL_WRONG_ALLOWED - st.session_state.wrong_count, 0)
        st.write(f"⚠️ Wrong answers left: **{remaining_wrongs}**")

        if st.button("🔄 Reset Test"):
            reset_test()
            st.rerun()

    # ----------------------------
    # MAIN QUESTION PANEL
    # ----------------------------
    current_index = st.session_state.current_q
    q_data = QUESTIONS[current_index]
    user_answer_index = st.session_state.user_answers[current_index]
    has_answered = user_answer_index is not None

    if st.session_state.test_finished:
        st.warning("You cannot attempt more questions. The test is finished.")
    else:
        st.info(
            "Select your answer and click **Submit Answer**. "
            "Once submitted, the answer for that question is locked."
        )

    st.subheader(q_data["question"])

    # Radio button for options
    # If already answered, we keep the selected option and disable further change.
    if user_answer_index is None:
        default_index = 0  # pre-select first option for convenience
    else:
        default_index = user_answer_index

    selected_option = st.radio(
        "Choose the correct option:",
        q_data["options"],
        index=default_index,
        key=f"q_{current_index}",
        disabled=has_answered or st.session_state.test_finished,
    )

    # Submit button - only active if this question not answered and test not finished
    submit_disabled = has_answered or st.session_state.test_finished

    if st.button("✅ Submit Answer", disabled=submit_disabled):
        # Determine selected index
        try:
            selected_index = q_data["options"].index(selected_option)
        except ValueError:
            selected_index = None

        if selected_index is not None and not has_answered:
            st.session_state.user_answers[current_index] = selected_index

            if selected_index == q_data["answer_index"]:
                st.session_state.correct_count += 1
                st.success("Correct! 🎉 +1 mark")
                st.session_state.score += MARKS_CORRECT
            else:
                st.session_state.wrong_count += 1
                st.error("Wrong answer. -0.5 mark")
                st.session_state.score += MARKS_WRONG

            # Check if limit of wrong answers reached
            if st.session_state.wrong_count >= TOTAL_WRONG_ALLOWED:
                st.session_state.test_finished = True
                st.warning(
                    f"You have reached {TOTAL_WRONG_ALLOWED} wrong answers. "
                    "You are now barred from attempting further questions."
                )

            st.rerun()

    # ----------------------------
    # NAVIGATION BUTTONS
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ Previous") and current_index > 0:
            st.session_state.current_q -= 1
            st.rerun()

    with col2:
        if st.button("Next ➡️") and current_index < TOTAL_QUESTIONS - 1:
            st.session_state.current_q += 1
            st.rerun()

    with col3:
        end_now = st.button("🏁 End Test & View Result")

    # Condition to show result:
    # - user clicked "End Test", OR
    # - test is finished (3 wrong), OR
    # - all questions answered
    all_answered = all(a is not None for a in st.session_state.user_answers)
    show_result = end_now or st.session_state.test_finished or all_answered

    if show_result:
        st.markdown("---")
        st.header("🏆 Final Result")

        score = st.session_state.score
        percent = calculate_percentage(score)
        medal = get_medal(percent)

        attempted = st.session_state.correct_count + st.session_state.wrong_count

        st.write(f"Questions attempted: **{attempted} / {TOTAL_QUESTIONS}**")
        st.write(f"✅ Correct: **{st.session_state.correct_count}**")
        st.write(f"❌ Wrong: **{st.session_state.wrong_count}**")
        st.write(f"🔢 Final Score: **{score:.2f}**")
        st.write(f"📈 Percentage: **{percent:.2f}%**")
        st.subheader(f"Your Medal: {medal}")

        if percent < BRONZE_THRESHOLD:
            st.info("Keep practicing BNSS. Thoda aur revision and you'll get a medal next time! 💪")


if __name__ == "__main__":
    main()
