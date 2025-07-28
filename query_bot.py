import pandas as pd
import os
csv_path = "Training Dataset.csv"
if not os.path.exists(csv_path):
    print(f"File not found: {csv_path}")
else:
    df = pd.read_csv(csv_path)

# Load dataset
#df = pd.read_csv("Training Dataset.csv")
df = pd.read_csv(r"C:\Users\User\Downloads\Training Dataset.csv")

# Clean and preprocess as needed
df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

def answer_query(query: str) -> str:
    query = query.lower()

    if "maximum loan amount" in query:
        return f"The maximum loan amount is ₹{df['LoanAmount'].max()}."

    elif "average loan amount for approved" in query:
        avg = df[df['Loan_Status'] == 1]['LoanAmount'].mean()
        return f"The average loan amount for approved applicants is ₹{avg:.2f}."

    elif "₹25000" in query:
        return "With an income of ₹25,000, your eligibility depends on other factors like coapplicant income, credit history, and employment. On average, applicants with similar income get loans around ₹120-₹150."

    elif "required documents" in query:
        return "Common documents include ID proof, address proof, income proof, bank statements, and employment verification."

    elif "co-applicant income" in query:
        return "Yes, co-applicant income is considered and can improve your loan eligibility."

    elif "how long does it take" in query or "approve a loan" in query:
        return "Loan approval usually takes 5 to 7 working days after document verification."

    elif "loan term duration" in query:
        return f"Most loans are offered with a term of {df['Loan_Amount_Term'].mode()[0]} months."

    elif "credit history is poor" in query:
        return "Poor credit history reduces your chances of loan approval. Try to improve your score or add a coapplicant."

    elif "graduates" in query and "average" in query:
        avg = df[df['Education'] == "Graduate"]['LoanAmount'].mean()
        return f"The average loan amount for graduates is ₹{avg:.2f}."

    elif "urban" in query:
        approved = df[df['Property_Area'] == 'Urban']
        rate = approved['Loan_Status'].mean() * 100
        return f"Yes, around {rate:.2f}% of applicants in urban areas get loans approved."

    elif "married" in query and "percentage" in query:
        married = df[df['Married'] == 'Yes']
        rate = married['Loan_Status'].mean() * 100
        return f"Approximately {rate:.2f}% of married applicants get loan approvals."

    elif "education level" in query:
        grad = df[df['Education'] == "Graduate"]['Loan_Status'].mean() * 100
        not_grad = df[df['Education'] == "Not Graduate"]['Loan_Status'].mean() * 100
        return f"Graduates have an approval rate of {grad:.2f}% while non-graduates have {not_grad:.2f}%."

    elif "self-employed" in query:
        self_emp = df[df['Self_Employed'] == 'Yes']['Loan_Status'].mean() * 100
        return f"Self-employed applicants have a loan approval rate of {self_emp:.2f}%."

    elif "no coapplicant income" in query:
        group = df[df['CoapplicantIncome'] == 0]
        avg = group['LoanAmount'].mean()
        return f"The typical loan amount for people with no coapplicant income is ₹{avg:.2f}."

    elif "dependents" in query and "trend" in query:
        trend = df.groupby('Dependents')['Loan_Status'].mean() * 100
        return "Loan approval rates by number of dependents:\n" + trend.to_string()

    elif "applicant income" in query and "impact" in query:
        return "Higher applicant income generally improves approval chances, but other factors like credit history and dependents matter."

    elif "₹30000" in query and "no dependents" in query:
        return "Yes, with ₹30,000 income and no dependents, you have a strong chance of approval."

    elif "not a graduate" in query:
        not_grad_rate = df[df['Education'] == 'Not Graduate']['Loan_Status'].mean() * 100
        return f"Yes, but the approval rate for non-graduates is around {not_grad_rate:.2f}%."

    elif "credit history" in query and "rate" in query:
        rate = df[df['Credit_History'] == 1]['Loan_Status'].mean() * 100
        return f"Applicants with credit history have an approval rate of {rate:.2f}%."

    elif "without a credit history" in query:
        rate = df[df['Credit_History'] == 0]['Loan_Status'].mean() * 100
        return f"Applicants without credit history have an approval rate of {rate:.2f}%."

    elif "minimum income" in query:
        return "There is no fixed minimum income, but applicants earning ₹15,000+ with a good credit history have higher approval chances."

    elif "unmarried" in query:
        unmarried = df[df['Married'] == 'No']['Loan_Status'].mean() * 100
        return f"Unmarried applicants have an approval rate of {unmarried:.2f}%."

    elif "₹10000" in query and "2 dependents" in query:
        return "With ₹10,000 income and 2 dependents, approval chances are low unless supported by strong credit history or coapplicant."

    elif "self-employed female graduate" in query:
        match = df[
            (df['Self_Employed'] == 'Yes') &
            (df['Gender'] == 'Female') &
            (df['Education'] == 'Graduate')
        ]['Loan_Status'].mean() * 100
        return f"Your group has an approval rate of {match:.2f}%."

    elif "₹40000" in query:
        return "A married couple with ₹40,000 income can generally expect loan amounts around ₹180-₹200 depending on credit history."

    elif "rejected once" in query:
        return "Improved income and credit behavior increase your chances. Past rejection won't necessarily block new approvals."

    elif "coapplicant" in query and "improve" in query:
        return "Yes, adding a coapplicant increases total income and improves loan approval probability."

    else:
        return "Sorry, I don't have a clear answer for that yet."

# List of all queries to test
queries = [
    "What is the maximum loan amount I can get?",
    "What is the average loan amount for approved applicants?",
    "How much loan can I get if my income is ₹25,000?",
    "What are the required documents for loan approval?",
    "Is co-applicant income considered for loan eligibility?",
    "How long does it take to approve a loan?",
    "What is the loan term duration usually offered?",
    "What happens if my credit history is poor?",
    "What’s the average loan amount for graduates?",
    "Is loan approval higher in urban areas?",
    "What percentage of married applicants get their loans approved?",
    "How does education level affect loan approval?",
    "Do self-employed people get their loans approved easily?",
    "What is the typical loan amount for people with no coapplicant income?",
    "Is there any trend in approval based on the number of dependents?",
    "How does applicant income impact loan status?",
    "Am I eligible for a loan if I earn ₹30,000 per month and have no dependents?",
    "Can I get a loan if I am not a graduate?",
    "What’s the loan approval rate for people with credit history?",
    "Can I get a loan without a credit history?",
    "What’s the minimum income required to get a loan approved?",
    "Are loans easier to get if I’m unmarried?",
    "Will my loan be approved if I earn ₹10,000 per month and have 2 dependents?",
    "I am a self-employed female graduate; can I get a loan?",
    "How much loan can a married couple with ₹40,000 income expect?",
    "I was rejected once. What are my chances now with better income?",
    "Can I improve my loan chances by adding a coapplicant?"
]

# Run and print answers
for q in queries:
    print(f"Q: {q}")
    print(f"A: {answer_query(q)}\n")
