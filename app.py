import streamlit as st
import sqlite3
import chromadb
import pandas as pd

from sentence_transformers import SentenceTransformer
from router import route_query

st.set_page_config(layout="wide")

model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------
# SQL Function
# -------------------

def query_sql(question):
    # ... (keep your existing query_sql code unchanged)
    pass


# -------------------
# RAG Function
# -------------------

def query_rag(question):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("company_docs")
    query_embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )
    return results["documents"][0][0]


# -------------------
# Streamlit UI
# -------------------

st.title("SQL + RAG Router")

main_col, sidebar_col = st.columns([3, 1])

with main_col:
    question = st.text_input("Ask a question")

    if st.button("Submit") and question:
        route = route_query(question)
        st.success(f"Route Selected: {route.upper()}")

        if route == "sql":
            response = query_sql(question)
            if response:
                if response["type"] == "single":
                    st.subheader("Employee Salary")
                    st.success(f"{response['name']} — ₹{response['salary']:,}")

                elif response["type"] == "department_highest":
                    st.subheader("Department Analysis")
                    st.success(
                        f"{response['department']} department has the highest average salary: ₹{response['salary']:,.0f}"
                    )

                elif response["type"] == "highest_paid":
                    st.subheader("Highest Paid Employee")
                    st.success(
                        f"{response['name']} ({response['department']}) earns ₹{response['salary']:,}"
                    )

                elif response["type"] == "top5":
                    df = pd.DataFrame(
                        response["data"],
                        columns=["Employee Name", "Department", "Salary"]
                    )
                    st.subheader("Top 5 Highest Paid Employees")
                    st.dataframe(df, use_container_width=True)

                elif response["type"] == "count":
                    st.subheader("Department Employee Count")
                    st.success(
                        f"{response['department']} department has {response['count']} employees."
                    )

                elif response["type"] == "department_list":
                    df = pd.DataFrame(
                        response["data"],
                        columns=["Employee Name", "Salary"]
                    )
                    st.subheader(f"{response['department']} Department Employees")
                    st.dataframe(df, use_container_width=True)

                elif response["type"] == "avg_department":
                    df = pd.DataFrame(
                        response["data"],
                        columns=["Department", "Average Salary"]
                    )
                    st.subheader("Average Salary by Department")
                    st.dataframe(df, use_container_width=True)

                elif response["type"] == "table":
                    df = pd.DataFrame(
                        response["data"],
                        columns=["Employee Name", "Salary"]
                    )
                    st.subheader("Salary Records")
                    st.dataframe(df, use_container_width=True)

            else:
                st.warning("No matching SQL results found.")

        else:
            response = query_rag(question)
            st.subheader("RAG Answer")
            st.write(response)


with sidebar_col:

    # -------------------
    # Policy Files Panel
    # -------------------

    st.markdown("### 📂 Available Policies")
    st.markdown("Ask questions about any of these documents:")

    policies = [
        "📄 Employee Handbook",
        "📄 Leave Policy",
        "📄 Benefits Policy",
        "📄 Travel Policy",
        "📄 Code of Conduct",
        "📄 Onboarding Guide",
        "🔒 Security Policy",
    ]

    for policy in policies:
        st.markdown(f"- {policy}")

    st.divider()

    # -------------------
    # Example Queries Panel
    # -------------------

    st.markdown("### 💡 Try asking")

    examples = [
        "Who earns the highest salary?",
        "Top 5 highest paid employees",
        "How many employees are in IT?",
        "List all Finance employees",
        "Show average salary by department",
        "What is Sophia Jones's salary?",
        "What is the leave policy?",
        "What are the travel reimbursement rules?",
    ]

    for example in examples:
        st.code(example, language=None)