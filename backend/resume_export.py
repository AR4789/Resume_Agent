from reportlab.lib.pagesizes import A4
from resume_template import render_resume
import os

def save_optimized_resume(data, output_path, design="modern", density="detailed"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    render_resume(
            type("C", (), {"_filename": output_path}),
            data,
            design=design,
            density=density
        )