from click import style
import random
import streamlit as st
import re
import pandas as pd
import plotly.express as px
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import (
    insert_candidate,
    get_candidates,
    delete_candidate
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Screener Pro",
    page_icon="📄",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(
        rgba(255,255,255,0.10),
        rgba(255,255,255,0.10)
    ),
    url("https://images.unsplash.com/photo-1497215842964-222b430dc094");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
            .glass-card{
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
}

/* Main content */
.block-container{
    padding-top: 2rem;
}

/* Cards */
[data-testid="stMetric"]{
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton > button{
    border-radius:10px;
    font-weight:bold;
}

/* Tables */
[data-testid="stDataFrame"]{
    background:white;
    border-radius:12px;
}

/* Expander */
.streamlit-expanderHeader{
    background:white;
    border-radius:10px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#ffffff;
}

</style>
""", unsafe_allow_html=True)
# =========================
# SIDEBAR
# =========================
# =========================
# SIDEBAR
# =========================

st.sidebar.success(
    "🟢 System Status: Active"
)

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title(
    "🚀 AI Resume Screener Pro"
)

st.sidebar.markdown("---")

st.sidebar.info("""
### 📌 Core Features

✅ ATS Score Analysis

✅ Multiple Resume Upload

✅ Candidate Ranking

✅ Skill Detection

✅ Missing Skills Detection

✅ Resume Strength Analysis

✅ Email Extraction

✅ Phone Extraction

✅ CSV Download

✅ Analytics Dashboard

✅ Database Storage
""")

st.sidebar.markdown("---")

st.sidebar.info("""
### 🚀 Why Choose Us?

🎯 Smart ATS Scoring

📊 Candidate Comparison

🤖 AI Recommendations

⚡ Faster Resume Screening

📈 Analytics Dashboard

🔍 Skill Gap Detection
""")

st.sidebar.markdown("---")

st.sidebar.success(
    "🤖 AI Powered Screening"
)

st.sidebar.success(
    "📊 Smart Analytics"
)

st.sidebar.success(
    "🎯 ATS Optimization"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Version 1.0 | Built with Python, Streamlit & SQLite"
)
st.sidebar.markdown("---")

st.sidebar.markdown(
    "[🔗 GitHub Repository](https://github.com/celestial08/ai-resume-screener)"
)

# =========================
# SKILLS LIST
# =========================

skills = [
    "python",
    "java",
    "sql",
    "mysql",
    "html",
    "css",
    "javascript",
    "react",
    "spring boot",
    "git",
    "machine learning",
    "pandas",
    "numpy"
]
Interview_Questions = {

    "python": [
        "What is OOP?",
        "What is a List?",
        "What is a Tuple?",
        "What is a Dictionary?",
        "What are Decorators?",
        "What is Exception Handling?",
        "What is Lambda Function?",
        "What is List Comprehension?",
        "What is Multithreading?",
        "What is Inheritance?",
        "What is Polymorphism?",
        "Difference between List and Tuple?",
        "Difference between Deep Copy and Shallow Copy?",
        "What is __init__()?",
        "What are Generators?",
        "What is Pandas?",
        "What is NumPy?",
        "What is Flask?",
        "What is Django?",
        "What is API?"
    ],

    "sql": [
        "What is Primary Key?",
        "What is Foreign Key?",
        "What is JOIN?",
        "Types of JOINs?",
        "Difference between WHERE and HAVING?",
        "What is GROUP BY?",
        "What is Normalization?",
        "What is Denormalization?",
        "What is Indexing?",
        "What is View?",
        "What is Stored Procedure?",
        "What is Trigger?",
        "What is Subquery?",
        "Difference between DELETE and TRUNCATE?",
        "Difference between UNION and UNION ALL?",
        "What is Aggregate Function?",
        "What is SQL Injection?",
        "What is ACID Property?",
        "What is Composite Key?",
        "What is Candidate Key?"
    ],

    "java": [
        "What is JVM?",
        "What is JDK?",
        "What is JRE?",
        "What is OOP?",
        "What is Inheritance?",
        "What is Polymorphism?",
        "What is Abstraction?",
        "What is Encapsulation?",
        "Difference between Interface and Abstract Class?",
        "What is Exception Handling?"
    ]
}

# ==================.glass-card{=======
# PDF TEXT EXTRACTION
# =========================

def extract_text(pdf_file):

    text = ""

    pdf_reader = PdfReader(pdf_file)

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text
st.markdown("""
<div style="
background:#0f172a;
padding:15px;
border-radius:10px;
color:white;
display:flex;
justify-content:space-between;
">

<h3>🚀 AI Resume Screener Pro</h3>

</div>
""", unsafe_allow_html=True)
if 'df' in locals():

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📄 Resumes",
            len(df)
        )

    with col2:
        st.metric(
            "🥇 Shortlisted",
            len(df[df["Status"]=="Shortlisted"])
        )

    with col3:
        st.metric(
            "⚠️ Review",
            len(df[df["Status"]=="Under Review"])
        )

    with col4:
        st.metric(
            "❌ Rejected",
            len(df[df["Status"]=="Rejected"])
        )

# =========================
# TITLE
# ========================
st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:15px;
box-shadow:0 2px 10px rgba(0,0,0,0.08);
">

<h1 style="color:#1e293b;text-align:center;">
🚀 AI Resume Screener Pro
</h1>

<p style="
text-align:center;
color:#64748b;
font-size:18px;
">
AI Powered Resume Analysis & ATS Tracking System
</p>

</div>
""", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📄 Resumes", "0")

with col2:
    st.metric("🥇 Shortlisted", "0")

with col3:
    st.metric("⚠️ Review", "0")

with col4:
    st.metric("❌ Rejected", "0")
st.info(
    "🤖 AI-Powered Resume Analysis • ATS Scoring • Candidate Ranking • Skill Gap Detection"
)
# =========================
# JOB DESCRIPTION
# =========================

job_description = st.text_area(
    "Enter Job Description",
    height=200
)
st.markdown("""
### 📤 Upload Resume

Upload one or multiple resumes for ATS analysis.
""")

# =========================
# RESUME UPLOAD
# =========================

uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)
st.markdown(
    """
    <h2 style='color:#111827; font-weight:bold;'>
    📋 Previous Candidates
    </h2>
    """,
    unsafe_allow_html=True
)

data = get_candidates()

if data:

    for row in data:

        with st.expander(f"👤 {row[1]}"):

            st.write("📧 Email:", row[2])
            st.write("📱 Phone:", row[3])
            st.write("🎯 ATS Score:", row[4])
            st.write("🛠 Skills:", row[5])
        if st.button(
            f"🗑 Delete Candidate",
            key=f"delete_{row[0]}"
        ):

            delete_candidate(row[0])

            st.success(
                "Candidate Deleted Successfully"
            )

            st.rerun()

else:
   st.markdown(
    """
    <div style="
    background:rgba(255,255,255,0.85);
    padding:12px;
    border-radius:10px;
    color:#111827;
    font-weight:bold;
    ">
    No candidates found.
    </div>
    """,
    unsafe_allow_html=True
)
if uploaded_files:
    st.info(
        f"📄 Total Resumes Uploaded: {len(uploaded_files)}"
    )
# =========================
# MAIN LOGIC
# =========================

if uploaded_files and job_description:

    results = []

    for uploaded_file in uploaded_files:

        resume_text = extract_text(uploaded_file)

        # Candidate Name
        candidate_name = uploaded_file.name.replace(".pdf", "")

        # Email Extraction
        emails = re.findall(
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
            resume_text
        )

        email = emails[0] if emails else "Not Found"

        # Phone Extraction
        phones = re.findall(
            r'(\+91[-\s]?\d{10}|\d{10})',
            resume_text
        )

        phone = phones[0] if phones else "Not Found"

        # ATS Score
        documents = [
            resume_text,
            job_description
        ]

        tfidf = TfidfVectorizer()

        matrix = tfidf.fit_transform(documents)

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        score = round(
            similarity * 100,
            2
        )
        

        # Status
        if score >= 80:
            status = "Shortlisted"

        elif score >= 60:
            status = "Under Review"

        else:
            status = "Rejected"

        # Skills Found
        found_skills = []

        for skill in skills:

            if skill.lower() in resume_text.lower():

                found_skills.append(skill)

        skills_text = ", ".join(found_skills)
        matched_skills = len(found_skills)

        skill_match = round(
        (matched_skills / len(skills)) * 100,
    2
)

        # Missing Skills
        missing_skills = []

        for skill in skills:

            if (
                skill.lower() in job_description.lower()
                and skill.lower()
                not in resume_text.lower()
            ):

                missing_skills.append(skill)

        # Resume Strength
        strength = 0

        if email != "Not Found":
            strength += 2

        if phone != "Not Found":
            strength += 2

        if len(found_skills) >= 5:
            strength += 3

        if "project" in resume_text.lower():
            strength += 3

        # Save Database
        insert_candidate(
            candidate_name,
            email,
            phone,
            score,
            skills_text
        )

        # Results
        results.append({
            "Name": candidate_name,
            "Email": email,
            "Phone": phone,
            "Score": score,
            "Status": status,
            "Strength": f"{strength}/10",
            "Skills": skills_text,
            "Skill Match": f"{skill_match}%",
            "Missing Skills": ", ".join(missing_skills),
            "Resume Text": resume_text
        })
        

        # =========================
    # RANKING SECTION
    # =========================

    results = sorted(
        results,
        key=lambda x: x["Score"],
        reverse=True
    )

    

    # Top 3 Candidates
    df = pd.DataFrame(results)
    top3 = df.head(3)

    st.subheader("🥇 Top 3 Candidates")
    st.table(top3[["Name", "Score", "Status"]])

    # Search Candidate
    search = st.text_input("🔍 Search Candidate")

    if search:
        df = df[
            df["Name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # Filter
    show_shortlisted = st.checkbox(
        "Show Shortlisted Only"
    )

    if show_shortlisted:
        df = df[
            df["Status"] == "Shortlisted"
        ]

    # Candidate Table
                    # Candidate Table
    st.dataframe(df)

    # Candidate Cards
    st.subheader("👥 Candidate Profiles")

    for index, row in df.iterrows():

        with st.container():

            if index == 0:
                st.markdown(
    f"### Rank #{index+1}"
)

                st.success(
                    f"🥇 TOP CANDIDATE - {row['Name']}"
                )

            else:

                st.success(
                    f"👤 {row['Name']}"
                )

            col1, col2 = st.columns(2)

            with col1:
                st.write("📧 Email:", row["Email"])
                st.write("📱 Phone:", row["Phone"])

            with col2:
                
               if row["Score"] >= 80:

                st.success(
                f"🎯 ATS Score: {row['Score']}%"
            )

               elif row["Score"] >= 60:

                st.warning(
                f"🎯 ATS Score: {row['Score']}%"
            )

               else:

                st.error(
                f"🎯 ATS Score: {row['Score']}%"
            )

        st.write("📌 Status:", row["Status"])

        st.write("🛠 Skills:", row["Skills"])
        candidate_skills = row["Skills"].lower()
        with st.expander("🎤 Smart Interview Questions"):

         for skill, questions in Interview_Questions.items():

            if skill in candidate_skills:

             st.write(f"### {skill.upper()}")

            selected_questions = random.sample(
                questions,
                min(20, len(questions))
            )

            for i, q in enumerate(selected_questions, 1):

                st.write(f"{i}. {q}")

            for skill, questions in Interview_Questions.items():

             if skill in candidate_skills:

              st.write(f"### {skill.upper()}")

            for q in questions:

               st.write("•", q)

        st.write(
            "🎯 Skill Match:",
            row["Skill Match"]
        )

        st.error(
            f"Missing Skills: {row['Missing Skills']}"
            if row["Missing Skills"] else ""
        )

        if row["Missing Skills"]:

            st.info(
                f"""
```

🤖 Recommendation

✔ Add {row['Missing Skills']}

✔ Add relevant projects

✔ Add GitHub link

✔ Improve resume keywords
"""
)


        if row["Status"] == "Rejected":

            st.error(
                "❌ Resume does not match job requirements."
            )

            st.info(
                "💡 Add missing skills, projects and relevant keywords."
            )

        elif row["Status"] == "Under Review":

            st.warning(
                "⚠️ Resume partially matches the job description."
            )

            st.info(
                "💡 Add more relevant skills and project experience."
            )

        else:

            st.success(
                "✅ Strong match for this role."
            )

        st.write(
            "💪 Resume Strength:",
            row["Strength"]
        )
        st.progress(
          min(int(row["Score"]),100)
)

        st.write(
           f"🎯 Match Percentage: {row['Score']}%"
)

        with st.expander(
                "📄 View Resume"
            ):

                st.write(
                    row["Resume Text"][:3000]
                )

        strength_value = int(
                row["Strength"].split("/")[0]
            )

        st.progress(
                strength_value * 10
            )

        st.progress(
                min(int(row["Score"]), 100)
            )

        status_text = f"""
Name: {row['Name']}
Email: {row['Email']}
ATS Score: {row['Score']}%
Status: {row['Status']}
Skills: {row['Skills']}
Skill Match: {row['Skill Match']}
"""

        st.download_button(
                "📥 Download Status",
                status_text,
                f"{row['Name']}_status.txt"
            )

        favorite = st.checkbox(
                f"⭐ Favorite {row['Name']}",
                key=f"fav_{index}"
            )

        if favorite:

                st.success(
                    f"{row['Name']} added to Favorites"
                )

        st.divider()
        with st.expander(
    "📊 Score Breakdown"
):

         st.write(
        "📧 Email Found: +20"
    )

         st.write(
        "📱 Phone Found: +20"
    )

         st.write(
        "🛠 Skills Found: +30"
    )

         st.write(
        "📂 Projects Found: +30"
    )
        # Resume Weakness Detector

        weaknesses = []

        if "github" not in row["Resume Text"].lower():
         weaknesses.append("No GitHub Link")

        if "project" not in row["Resume Text"].lower():
         weaknesses.append("No Project Mentioned")

        if "certificate" not in row["Resume Text"].lower():
         weaknesses.append("No Certifications")

        if weaknesses:

         st.warning(
        "🚨 Resume Weaknesses"
    )

        for item in weaknesses:

         st.write(
            f"❌ {item}"
        )
         # Career Role Predictor

        resume_text = row["Resume Text"].lower()

        roles = []

        if "python" in resume_text:
         roles.append("🥇 Python Developer")

        if "sql" in resume_text:
         roles.append("🥈 Data Analyst")

        if (
         "machine learning" in resume_text
           or "ai" in resume_text
):
         roles.append("🥉 AI Engineer")

        if "html" in resume_text or "css" in resume_text:
         roles.append("🌐 Frontend Developer")

        if "java" in resume_text:
         roles.append("☕ Java Developer")

        if roles:

         st.success(
        "🎯 Best Suitable Roles"
    )

    for role in roles:

        st.write(role)
        # Interview Question Generator

        questions = []

        if "python" in resume_text:

         questions.extend([
        "What is OOP in Python?",
        "Difference between List and Tuple?"
    ])

        if "sql" in resume_text:

         questions.extend([
        "What is a Primary Key?",
        "Difference between SQL and MySQL?"
    ])

        if "java" in resume_text:

         questions.extend([
        "What is JVM?",
        "Explain Inheritance in Java."
    ])

        if "machine learning" in resume_text:

         questions.extend([
        "What is Overfitting?",
        "Difference between Supervised and Unsupervised Learning?"
    ])

        if questions:

         with st.expander(
        "🎤 Interview Questions"
    ):

          for q in questions:

            st.write(
                f"• {q}"
            )
            # ATS Score Simulator

        missing = row["Missing Skills"]

    if missing:

     st.subheader(
        "📈 ATS Score Simulator"
    )

    current_score = row["Score"]

    st.write(
        f"Current ATS Score: {current_score}%"
    )

    missing_list = missing.split(",")

    for skill in missing_list:

        skill = skill.strip()

        predicted_score = min(
            current_score + 5,
            100
        )

        st.success(
            f"Add {skill} → Estimated ATS: {predicted_score}%"
        )
        # AI Career Roadmap

        st.subheader(
           "🛣️ Career Roadmap"
)
        # AI Resume Improvement Suggestions

        st.subheader(
         "🤖 AI Suggestions"
)

        if row["Score"] < 80:

         st.warning(
        f"Current ATS Score: {row['Score']}%"
    )

        st.info(
        "To improve your ATS score:"
    )

        if row["Missing Skills"]:

         st.write(
            f"✔ Add Skills: {row['Missing Skills']}"
        )

        if "github" not in row["Resume Text"].lower():

         st.write(
            "✔ Add GitHub Profile"
        )

        if "project" not in row["Resume Text"].lower():

         st.write(
            "✔ Add 2 Projects"
        )

        if "internship" not in row["Resume Text"].lower():

         st.write(
            "✔ Add Internship Experience"
        )

    else:

        st.success(
        "🎉 Resume is already highly optimized."
    )
        missing = row["Missing Skills"]

        if missing:

         missing_list = [
        skill.strip()
        for skill in missing.split(",")
        if skill.strip()
    ]

         week = 1

        for skill in missing_list:

         st.success(
            f"Week {week}: Learn {skill}"
        )

        week += 1

        st.info(
        f"Week {week}: Build a Project using learned skills"
    )

        st.info(
        f"Week {week+1}: Upload project to GitHub"
    )

        st.info(
        f"Week {week+2}: Apply for Internships"
    )

else:

        st.markdown(
    """
    <div style="
    background:rgba(255,255,255,0.85);
    padding:12px;
    border-radius:10px;
    color:#111827;
    font-weight:bold;
    ">
    🎉 Your resume already matches most requirements.
    </div>
    """,
    unsafe_allow_html=True
)
    # Status Summary
if 'df' in locals():
        st.write("### Candidate Status Summary")

        st.success(
        f"✅ Shortlisted: {len(df[df['Status']=='Shortlisted'])}"
    )

        st.warning(
        f"⚠️ Under Review: {len(df[df['Status']=='Under Review'])}"
    )

        st.error(
        f"❌ Rejected: {len(df[df['Status']=='Rejected'])}"
    )

    # Best Candidate
        if len(df) > 0:

         top_candidate = df.iloc[0]
        st.balloons()

        st.success(f"""
🏆 BEST CANDIDATE

Name: {top_candidate['Name']}

Score: {top_candidate['Score']}%

Status: {top_candidate['Status']}
""")

        st.success(
            f"🏆 Best Candidate: {top_candidate['Name']}"
        )

    # CSV Download
        csv = df.to_csv(index=False)

        st.download_button(
        "📥 Download Ranking Report",
        csv,
        "candidate_ranking.csv",
        "text/csv"
    )

    # Analytics Dashboard
        # Analytics Dashboard
        st.subheader("📊 Analytics Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
         st.metric(
            "Candidates",
            len(df)
        )

        with col2:
         st.metric(
            "Shortlisted",
            len(df[df["Status"] == "Shortlisted"])
        )

        with col3:
         st.metric(
            "Rejected",
            len(df[df["Status"] == "Rejected"])
        )

        fig = px.bar(
        df,
        x="Name",
        y="Score",
        color="Status",
        color_discrete_map={
            "Shortlisted": "green",
            "Under Review": "orange",
            "Rejected": "red"
        },
        title="Candidate Ranking"
    )

        st.plotly_chart(
        fig,
        use_container_width=True
    )

        pie = px.pie(
        df,
        names="Status",
        title="Candidate Distribution"
    )

        st.plotly_chart(
        pie,
        use_container_width=True
    )
st.markdown("""
<hr>

<center>

AI Resume Screener Pro © 2026

Built with Python • Streamlit • SQLite

</center>
""", unsafe_allow_html=True)
st.markdown("---")

st.caption(
    "AI Resume Screener Pro | Built using Python, Streamlit, SQLite, Pandas and Plotly"
)
    