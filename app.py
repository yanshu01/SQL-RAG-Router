
import streamlit as st
import sqlite3
import chromadb
import pandas as pd

from sentence_transformers import SentenceTransformer
from router import route_query


# -------------------
# Page Config
# -------------------

st.set_page_config(
    page_title="SQL + RAG Router",
    layout="wide"
)

# -------------------
# Load Embedding Model
# -------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -------------------
# SQL Function
# -------------------

def query_sql(question):

    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    question_lower = question.lower()

    # -------------------
    # Department With Highest Average Salary
    # -------------------

    if (
        "highest average salary" in question_lower
        or "highest department salary" in question_lower
        or "which department salary is very high" in question_lower
    ):

        cursor.execute("""
            SELECT department,
                   AVG(salary)
            FROM employees
            GROUP BY department
            ORDER BY AVG(salary) DESC
            LIMIT 1
        """)

        result = cursor.fetchone()

        conn.close()

        return {
            "type": "department_highest",
            "department": result[0],
            "salary": result[1]
        }

    # -------------------
    # Highest Paid Employee
    # -------------------

    if (
        "highest salary" in question_lower
        or "who earns the highest salary" in question_lower
    ):

        cursor.execute("""
            SELECT name,
                   department,
                   salary
            FROM employees
            ORDER BY salary DESC
            LIMIT 1
        """)

        result = cursor.fetchone()

        conn.close()

        return {
            "type": "highest_paid",
            "name": result[0],
            "department": result[1],
            "salary": result[2]
        }

    # -------------------
    # Top 5 Highest Paid Employees
    # -------------------

    if (
        "top 5" in question_lower
        or "highest paid employees" in question_lower
    ):

        cursor.execute("""
            SELECT name,
                   department,
                   salary
            FROM employees
            ORDER BY salary DESC
            LIMIT 5
        """)

        result = cursor.fetchall()

        conn.close()

        return {
            "type": "top5",
            "data": result
        }

    # -------------------
    # Department Employee Count
    # -------------------

    departments = [
        "it",
        "hr",
        "finance",
        "sales",
        "marketing"
    ]

    for dept in departments:

        if dept in question_lower and (
            "how many" in question_lower
            or "count" in question_lower
        ):

            cursor.execute("""
                SELECT COUNT(*)
                FROM employees
                WHERE LOWER(department)=?
            """, (dept,))

            result = cursor.fetchone()

            conn.close()

            return {
                "type": "count",
                "department": dept.upper(),
                "count": result[0]
            }

    # -------------------
    # List Employees By Department
    # -------------------

    for dept in departments:

        if dept in question_lower and (
            "list" in question_lower
            or "show" in question_lower
        ):

            cursor.execute("""
                SELECT name,
                       salary
                FROM employees
                WHERE LOWER(department)=?
            """, (dept,))

            result = cursor.fetchall()

            conn.close()

            return {
                "type": "department_list",
                "department": dept.upper(),
                "data": result
            }

    # -------------------
    # Average Salary By Department
    # -------------------

    if "average salary by department" in question_lower:

        cursor.execute("""
            SELECT department,
                   ROUND(AVG(salary),0)
            FROM employees
            GROUP BY department
            ORDER BY AVG(salary) DESC
        """)

        result = cursor.fetchall()

        conn.close()

        return {
            "type": "avg_department",
            "data": result
        }

    # -------------------
    # Employee Salary Lookup
    # -------------------

    cursor.execute("""
        SELECT name,
               salary
        FROM employees
    """)

    employees = cursor.fetchall()

    for name, salary in employees:

        if name.lower() in question_lower:

            conn.close()

            return {
                "type": "single",
                "name": name,
                "salary": salary
            }

    # -------------------
    # Show All Salaries
    # -------------------

    if "salary" in question_lower:

        conn.close()

        return {
            "type": "table",
            "data": employees
        }

    conn.close()

    return None


# -------------------
# RAG Function
# -------------------

def query_rag(question):

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_collection(
        "company_docs"
    )

    query_embedding = model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    return results["documents"][0][0]


# -------------------
# UI
# -------------------

st.title("SQL + RAG Router")

main_col, sidebar_col = st.columns([3, 1])

with main_col:

    question = st.text_input(
        "Ask a question"
    )

    if st.button("Submit") and question:

        route = route_query(question)

        st.success(
            f"Route Selected: {route.upper()}"
        )

        if route == "sql":

            response = query_sql(question)

            if response:

                if response["type"] == "single":

                    st.subheader(
                        "Employee Salary"
                    )

                    st.success(
                        f"{response['name']} — ₹{response['salary']:,}"
                    )

                elif response["type"] == "department_highest":

                    st.subheader(
                        "Department Analysis"
                    )

                    st.success(
                        f"{response['department']} department has the highest average salary: ₹{response['salary']:,.0f}"
                    )

                elif response["type"] == "highest_paid":

                    st.subheader(
                        "Highest Paid Employee"
                    )

                    st.success(
                        f"{response['name']} ({response['department']}) earns ₹{response['salary']:,}"
                    )

                elif response["type"] == "top5":

                    df = pd.DataFrame(
                        response["data"],
                        columns=[
                            "Employee Name",
                            "Department",
                            "Salary"
                        ]
                    )

                    st.subheader(
                        "Top 5 Highest Paid Employees"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                elif response["type"] == "count":

                    st.subheader(
                        "Department Employee Count"
                    )

                    st.success(
                        f"{response['department']} department has {response['count']} employees."
                    )

                elif response["type"] == "department_list":

                    df = pd.DataFrame(
                        response["data"],
                        columns=[
                            "Employee Name",
                            "Salary"
                        ]
                    )

                    st.subheader(
                        f"{response['department']} Department Employees"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                elif response["type"] == "avg_department":

                    df = pd.DataFrame(
                        response["data"],
                        columns=[
                            "Department",
                            "Average Salary"
                        ]
                    )

                    st.subheader(
                        "Average Salary by Department"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                elif response["type"] == "table":

                    df = pd.DataFrame(
                        response["data"],
                        columns=[
                            "Employee Name",
                            "Salary"
                        ]
                    )

                    st.subheader(
                        "Salary Records"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

            else:

                st.warning(
                    "No matching SQL results found."
                )

        else:

            response = query_rag(question)

            st.subheader(
                "RAG Answer"
            )

            st.write(response)

with sidebar_col:

    st.markdown(
        "### 📂 Available Policies"
    )

    st.markdown(
        "Ask questions about any of these documents:"
    )

    policies = [
        "📄 Employee Handbook",
        "📄 Leave Policy",
        "📄 Benefits Policy",
        "📄 Travel Policy",
        "📄 Code of Conduct",
        "📄 Onboarding Guide",
        "🔒 Security Policy"
    ]

    for policy in policies:
        st.markdown(f"- {policy}")

    st.divider()

    st.markdown(
        "### 💡 Example Questions"
    )

    examples = [
        "What is Sophia Jones's salary?",
        "Who earns the highest salary?",
        "Top 5 highest paid employees",
        "How many employees are in IT?",
        "List all Finance employees",
        "Show average salary by department",
        "Which department has the highest average salary?",
        "What is the leave policy?",
        "What are the travel reimbursement rules?"
    ]

    for example in examples:
        st.code(
            example,
            language=None
        )

