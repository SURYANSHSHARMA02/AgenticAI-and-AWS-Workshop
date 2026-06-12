from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

# =====================================
# SKILLS DATABASE
# =====================================

skills_db = [
    "python",
    "java",
    "c++",
    "aws",
    "azure",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "sql",
    "mysql",
    "database",
    "github",
    "git",
    "machine learning",
    "deep learning",
    "nlp",
    "langchain",
    "agentic ai",
    "docker",
    "kubernetes",
    "tensorflow",
    "pytorch"
]

# =====================================
# UPLOAD FOLDER
# =====================================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =====================================
# PDF READER
# =====================================

def extract_pdf_text(pdf_path):

    text = ""

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    except Exception as e:
        print("Error:", e)

    return text


# =====================================
# SKILL EXTRACTION
# =====================================

def extract_skills(text):

    found_skills = []

    for skill in skills_db:

        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))


# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================
# ANALYZE RESUMES
# =====================================

@app.route("/analyze", methods=["POST"])
def analyze():

    jd_text = request.form["jd"]

    jd_skills = extract_skills(
        jd_text.lower()
    )

    resumes = request.files.getlist(
        "resumes"
    )

    results = []

    report = []

    report.append("=" * 60)
    report.append("RESUME ANALYSIS REPORT")
    report.append("=" * 60)

    for resume in resumes:

        save_path = os.path.join(
            UPLOAD_FOLDER,
            resume.filename
        )

        resume.save(save_path)

        resume_text = extract_pdf_text(
            save_path
        )

        resume_skills = extract_skills(
            resume_text
        )

        matched = sorted(
            list(
                set(resume_skills)
                &
                set(jd_skills)
            )
        )

        missing = sorted(
            list(
                set(jd_skills)
                -
                set(resume_skills)
            )
        )

        results.append({

            "name": resume.filename,
            "matched": matched,
            "missing": missing

        })

        report.append("\n")
        report.append(
            f"Resume : {resume.filename}"
        )

        report.append(
            "-" * 40
        )

        report.append(
            "\nMatched Skills:"
        )

        if matched:

            for skill in matched:
                report.append(
                    f"✓ {skill}"
                )

        else:

            report.append(
                "No Skills Matched"
            )

        report.append(
            "\nMissing Skills:"
        )

        if missing:

            for skill in missing:
                report.append(
                    f"✗ {skill}"
                )

        else:

            report.append(
                "No Missing Skills"
            )

        report.append(
            "\n" + "-" * 60
        )

    with open(
        "resume_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(report)
        )

    return render_template(
        "index.html",
        results=results
    )


# =====================================
# RUN APP
# =====================================

if __name__ == "__main__":
    app.run(debug=True)