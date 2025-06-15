# Resume-analyzer
# Smart Resume Analyzer & Job Predictor
A Streamlit-powered web application that analyzes resumes (PDF or DOCX), extracts key details, and predicts suitable job roles based on detected skills. It provides a resume quality score, highlights missing information, and suggests roles in automation (GoHighLevel), banking, and teaching fields.
#  Features
 # Extracts Key Information:

Name

Email

Phone number

Skills (from a predefined skill set)

#  Resume Scoring (out of 100)

 Personalized Feedback to improve resume quality
 
 Job Position Suggestions based on identified skills

 Modern UI with gradient background for better user experience

 Supports PDF and DOCX resume uploads

 Manual input options for missing fields
 # Technologies Used
 Python

Streamlit for frontend interface

PyPDF2 and python-docx for file reading

spaCy (NLP) for name/entity extraction

Regex for emails and phone numbers

Custom Job Skill Matching Logic
# Project Structure
├── resume_analyzer.py           # Main Streamlit application
├── README.md                    # Project documentation
# How to Run
Clone this repository:
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
 # Install dependencies:
 pip install streamlit PyPDF2 python-docx spacy
python -m spacy download en_core_web_sm
# Run the Streamlit app:
      streamlit run resume_analyzer.py
Upload a PDF or DOCX resume and interact with the analyzer!
#  Example Output screen shot
<img width="442" alt="image" src="https://github.com/user-attachments/assets/2564df53-7b2d-49d5-80eb-863f14b3d2d9" />

#  Contributing
Contributions and feature requests are welcome! Please fork the repo and submit a pull request.

                                                                                     
