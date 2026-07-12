# app.py
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.aggregator import run_pipeline, generate_report, save_report

st.set_page_config(page_title="Career Profile Scorer", layout="centered")
st.title("Career Profile Scorer")
st.caption("Score your resume, GitHub profile, and LinkedIn presence.")

st.divider()

# --- inputs ---
st.subheader("Your details")

github_username  = st.text_input("GitHub username", placeholder="e.g. Blitzhac")
linkedin_folder  = st.text_input("LinkedIn export folder path", placeholder=r"C:\path\to\linkedin\export")
resume_file      = st.file_uploader("Upload your resume", type=["pdf", "docx"])

st.divider()

# --- run button ---
if st.button("Score my profile ↗"):

    # validate inputs before running
    if not github_username:
        st.error("Please enter your GitHub username.")
    elif not linkedin_folder:
        st.error("Please enter your LinkedIn export folder path.")
    elif not resume_file:
        st.error("Please upload your resume.")
    else:
        # save uploaded resume to a temp file so parsers can read it
        temp_dir = "outputs/temp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, resume_file.name)
        with open(temp_path, "wb") as f:
            f.write(resume_file.getbuffer())

        with st.spinner("Running pipeline..."):
            try:
                report = run_pipeline(
                    resume_path     = temp_path,
                    github_username = github_username,
                    linkedin_folder = linkedin_folder
                )

                # --- scores ---
                st.subheader(f"Results for {report['candidate']}")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Resume",   f"{report['scores']['resume']}/100")
                col2.metric("GitHub",   f"{report['scores']['github']}/100")
                col3.metric("LinkedIn", f"{report['scores']['linkedin']}/100")
                col4.metric("Total",    f"{report['scores']['total']}/100")

                st.divider()

                # --- feedback ---
                st.subheader("Feedback")
                for source, items in report["feedback"].items():
                    if items:
                        with st.expander(f"{source.upper()} suggestions"):
                            for item in items:
                                st.write(f"• {item}")
                    else:
                        st.success(f"{source.upper()}: No issues found ✓")

                st.divider()

                # --- full report ---
                st.subheader("Full report")
                st.code(generate_report(report), language=None)

                # --- download button ---
                filepath = save_report(report)
                with open(filepath, "r", encoding="utf-8") as f:
                    st.download_button(
                        label    = "Download report as .txt",
                        data     = f.read(),
                        file_name = os.path.basename(filepath),
                        mime     = "text/plain"
                    )

            except Exception as e:
                st.error(f"Something went wrong: {e}")