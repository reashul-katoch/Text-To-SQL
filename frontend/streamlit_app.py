import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Text-to-SQL",
    page_icon="🤖",
    layout="wide"
)


# -------------------------
# Session State
# -------------------------

defaults = {
    "token": None,
    "role": None,
    "username": None,

    # Clarification state
    "pending_question": None,
    "clarification_prompt": None,

    # Write confirmation state
    "pending_write_question": None,
    "pending_write_sql": None,
    "pending_write_operation": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------------
# Login
# -------------------------

if not st.session_state.token:

    st.title("🤖 AI-Powered Text-to-SQL")
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]
            st.session_state.username = username

            st.rerun()

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Login failed"
                )
            )

    st.stop()


# -------------------------
# Sidebar
# -------------------------

st.title("🤖 AI-Powered Text-to-SQL")

st.sidebar.success(
    f"User: {st.session_state.username}"
)

st.sidebar.info(
    f"Role: {st.session_state.role.upper()}"
)

if st.sidebar.button("Logout"):

    for key in defaults:
        st.session_state[key] = defaults[key]

    st.rerun()


# -------------------------
# API Headers
# -------------------------

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}


# =========================================================
# WRITE CONFIRMATION
# =========================================================

if st.session_state.pending_write_question:

    st.subheader("⚠️ Write Operation Confirmation")

    st.warning(
        "This query will modify data in the database."
    )

    st.write(
        f"Operation: **{st.session_state.pending_write_operation}**"
    )

    st.write("Generated SQL:")

    st.code(
        st.session_state.pending_write_sql,
        language="sql"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✅ Confirm Write"):

            response = requests.post(
                f"{API_URL}/query",
                json={
                    "question": st.session_state.pending_write_question,
                    "confirm_write": True
                },
                headers=headers
            )

            data = response.json()

            if response.status_code == 200:

                if data.get("status") == "success":

                    st.success(
                        "Write operation executed successfully."
                    )

                    st.write(
                        f"Rows affected: "
                        f"{data.get('rows_affected', 0)}"
                    )

                    # Clear pending write state
                    st.session_state.pending_write_question = None
                    st.session_state.pending_write_sql = None
                    st.session_state.pending_write_operation = None

                else:

                    st.error(
                        data.get(
                            "detail",
                            data
                        )
                    )

            else:

                st.error(
                    data.get(
                        "detail",
                        data
                    )
                )

    with col2:

        if st.button("❌ Cancel"):

            st.session_state.pending_write_question = None
            st.session_state.pending_write_sql = None
            st.session_state.pending_write_operation = None

            st.rerun()

    st.stop()


# =========================================================
# CLARIFICATION
# =========================================================

if st.session_state.pending_question:

    st.subheader("❓ Clarification Required")

    st.info(
        st.session_state.clarification_prompt
    )

    clarification = st.text_input(
        "Your answer",
        key="clarification_input"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Continue"):

            if not clarification.strip():

                st.warning(
                    "Please provide a clarification."
                )

            else:

                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": st.session_state.pending_question,
                        "clarification": clarification
                    },
                    headers=headers
                )

                data = response.json()

                if response.status_code == 200:

                    if data.get("status") == "success":

                        st.session_state.pending_question = None
                        st.session_state.clarification_prompt = None

                        st.success(
                            "Query executed successfully!"
                        )

                        st.code(
                            data["sql"],
                            language="sql"
                        )

                        st.dataframe(
                            data["data"],
                            use_container_width=True
                        )

                    elif data.get("status") == "confirmation_required":

                        # Move to write confirmation
                        st.session_state.pending_question = None
                        st.session_state.clarification_prompt = None

                        st.session_state.pending_write_question = (
                            st.session_state.pending_question
                        )

                        st.session_state.pending_write_sql = data["sql"]
                        st.session_state.pending_write_operation = (
                            data["operation"]
                        )

                        st.rerun()

                    else:

                        st.error(
                            data.get(
                                "detail",
                                data
                            )
                        )

                else:

                    st.error(
                        data.get(
                            "detail",
                            data
                        )
                    )

    with col2:

        if st.button("Cancel"):

            st.session_state.pending_question = None
            st.session_state.clarification_prompt = None

            st.rerun()

    st.stop()


# =========================================================
# NORMAL QUERY INTERFACE
# =========================================================

st.header("Ask Your Database")

question = st.text_area(
    "Enter your question",
    placeholder=(
        "Example: Show me all customers from Chandigarh"
    ),
    height=100
)


if st.button("Run Query"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            response = requests.post(
                f"{API_URL}/query",
                json={
                    "question": question
                },
                headers=headers
            )

            
            try:
                data = response.json()
            except ValueError:
                st.error(
                    f"API returned a non-JSON response "
                    f"(HTTP {response.status_code})"
                )
                st.code(response.text)
                st.stop()

            # -------------------------
            # Clarification
            # -------------------------

            if data.get("status") == "clarification_required":

                st.session_state.pending_question = question

                st.session_state.clarification_prompt = (
                    data["question"]
                )

                st.rerun()


            # -------------------------
            # Write Confirmation
            # -------------------------

            elif data.get("status") == "confirmation_required":

                st.session_state.pending_write_question = question

                st.session_state.pending_write_sql = (
                    data["sql"]
                )

                st.session_state.pending_write_operation = (
                    data["operation"]
                )

                st.rerun()


            # -------------------------
            # SELECT Success
            # -------------------------

            elif data.get("status") == "success":

                st.success(
                    "Query executed successfully!"
                )

                st.subheader("Generated SQL")

                st.code(
                    data["sql"],
                    language="sql"
                )

                if "data" in data:

                    st.subheader("Results")

                    st.dataframe(
                        data["data"],
                        use_container_width=True
                    )

                    st.caption(
                        f"Rows returned: {data['count']}"
                    )

                else:

                    st.write(
                        f"Rows affected: "
                        f"{data.get('rows_affected', 0)}"
                    )


            # -------------------------
            # Error
            # -------------------------

            else:

                st.error(
                    data.get(
                        "detail",
                        data
                    )
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Make sure the backend is running."
            )