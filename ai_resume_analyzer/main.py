from flask import Flask, render_template, request
import fitz
from analyse_pdf import analyze_resume_gemini
import os

app = Flask(__name__)

# Function to extract text from PDF
def extract_text_from_the_resume(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":

        # Get uploaded file
        uploaded_file = request.files["resume"]

        # Get job description
        job_description = request.form["job_description"]

        if uploaded_file:

            # Save uploaded file
            file_path = os.path.join("uploads", uploaded_file.filename)

            uploaded_file.save(file_path)

            # Extract resume text
            resume_content = extract_text_from_the_resume(file_path)

            # Reduce token usage
            resume_content = resume_content[:1500]

            # Analyze resume
            result = analyze_resume_gemini(
                resume_content,
                job_description
            )

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":

    # Create uploads folder if not exists
    os.makedirs("uploads", exist_ok=True)

    app.run(debug=True)