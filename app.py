from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import openai

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Set your OpenAI API key
openai.api_key = "your-openai-key"  # REPLACE THIS

# Load dataset
df = pd.read_csv("Training Dataset.csv")

# Temporary in-memory chat storage (per user)
chat_histories = {}

# Dataset-based chatbot logic
def dataset_chatbot(query):
    query = query.lower()
    if "average loan" in query:
        return f"Average loan amount is ₹{df['LoanAmount'].mean():.2f}"
    elif "maximum loan" in query or "how much can i get" in query:
        return f"Maximum loan amount is ₹{df['LoanAmount'].max():.2f}"
    elif "minimum loan" in query:
        return f"Minimum loan amount is ₹{df['LoanAmount'].min():.2f}"
    elif "approval rate" in query or "how many approved" in query:
        approved = df['Loan_Status'].value_counts().get('Y', 0)
        total = len(df)
        return f"Loan approval rate is {(approved / total) * 100:.2f}%"
    elif "how many loans" in query:
        return f"Total loans in the dataset: {len(df)}"
    elif "education" in query:
        return str(df['Education'].value_counts())
    elif "married" in query:
        return str(df['Married'].value_counts())
    elif "self employed" in query:
        return str(df['Self_Employed'].value_counts())
    elif "can i apply online" in query:
        return "Yes, many banks offer online application services. Make sure to have your documents ready."
    elif "documents needed" in query or "what documents" in query:
        return "Common documents include ID proof, income proof, address proof, and bank statements."
    elif "what if i don't have a job" in query or "unemployed" in query:
        return "Even if you're unemployed, you may still qualify if you have a co-applicant or other income source."
    elif "how long will it take" in query or "when will i get my loan" in query:
        return "Loan approval time can vary, but typically takes a few days to a week depending on the bank."
    elif "interest rate" in query:
        return "Interest rates vary by bank and credit score, usually between 8% and 15%."
    elif "do i need a co-applicant" in query:
        return "A co-applicant is not mandatory but can help increase your chances if your credit is low."
    elif "what is emi" in query:
        return "EMI stands for Equated Monthly Installment. It's the amount you pay monthly to repay the loan."
    elif "what is credit score" in query:
        return "A credit score is a numerical expression of your creditworthiness. A good score helps get better loans."
    elif "poor credit history" in query:
        return "You may still qualify with a co-applicant or by choosing NBFCs. However, terms may not be ideal."
    elif "can i repay early" in query or "prepayment" in query:
        return "Yes, most loans allow prepayment, though some may charge a penalty. Check with your lender."
    elif "loan duration" in query or "loan term" in query or "how many installments" in query:
        return "Loan terms usually range from 12 to 60 months, which means 12 to 60 monthly installments (EMIs)."
    elif "what is processing fee" in query:
        return "A processing fee is charged by banks to handle your loan application, usually 0.5% to 2% of loan."
    elif "collateral" in query:
        return "For personal loans, collateral is not required. For home or vehicle loans, the asset itself is collateral."
    elif "do i need income proof" in query:
        return "Yes, income proof such as salary slips or bank statements is usually required."
    elif "difference between personal and home loan" in query:
        return "Personal loans are unsecured and for general use. Home loans are secured for property purchase."
    return None


# OpenAI GPT fallback
def gpt_chatbot(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers loan-related questions."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception:
        return "Sorry, something went wrong with the chatbot."

# Unified chatbot logic
def chatbot(query):
    answer = dataset_chatbot(query)
    return answer if answer else gpt_chatbot(query)

# Login route (accept any non-empty credentials)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username and password:
            session["username"] = username
            chat_histories[username] = []  # reset chat history on login
            return redirect(url_for("chatbot_page"))
        else:
            return render_template("login.html", error="Username and password are required.")
    return render_template("login.html")

# Chatbot route
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot_page():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    if username not in chat_histories:
        chat_histories[username] = []

    error = None
    query_value = ""

    if request.method == "POST":
        action = request.form.get("action")
        query = request.form.get("query", "").strip()

        if action == "send":
            if not query:
                error = "Please enter a question."
            else:
                answer = chatbot(query)
                chat_histories[username].append({"user": query, "bot": answer})
            query_value = ""  # Clear input
        elif action == "clear":
            chat_histories[username] = []
            query_value = ""

    return render_template("chatbot.html", chat_history=chat_histories[username], error=error, query=query_value)

# Logout route
@app.route("/logout")
def logout():
    username = session.get("username")
    if username and username in chat_histories:
        del chat_histories[username]
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
