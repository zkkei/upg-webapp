UPG Strategic Co-Pilot
An unofficial UPG estimator that transforms passive assessment into active goal-setting for aspiring UP students.
Live Demo ᐊ— Replace this with your live Render URL.
Core Philosophy
Most calculators provide a passive grade. They tell you where you stand, but not where you could go. This tool is built on a different philosophy: that true self-improvement comes from understanding the distance between your current state and your desired potential.
The UPG Strategic Co-Pilot is designed not just to calculate, but to calibrate. It uses a "Harsh Reality" model to provide a realistic, unforgiving estimate that reflects a highly competitive environment. This is not meant to discourage, but to provide a clear, actionable target. It transforms an abstract ambition into a quantifiable objective, serving as a partner in the rigorous journey of self-improvement.
Features
Realistic UPG Estimation: Utilizes the v6.4 "Harsh Reality" model, a non-linear formula that heavily weights top-percentile scores to simulate a competitive admissions landscape.
Weighted Subtests: Inspired by official admissions principles, the model assigns different weights to UPCAT subtests and high school grades.
Strategic Analysis: Provides "Reach," "Target," and "Safety" analysis for your chosen campuses.
Clean, Responsive UI: A web-based interface built with Flask and Tailwind CSS, accessible on any device.
The "Harsh Reality" Model (v6.4)
The core of this calculator is a non-linear conversion function that penalizes scores that are not near-perfect. This is achieved by applying a COMPETITIVENESS_EXPONENT of 2.15 to normalized scores, ensuring that only exceptional performance significantly improves the final UPG.
Disclaimer
This is an educational and strategic tool that provides an ESTIMATE ONLY. The official University Predicted Grade (UPG) formula, its weights, and its constants are confidential and far more complex. Results from this calculator are NOT a guarantee of admission and should be used solely for personal goal-setting and motivation.
Local Development Setup
To run this application on your local machine:
Clone the repository:
git clone https://github.com/your-username/upg-webapp.git
cd upg-webapp


Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install dependencies:
pip install -r requirements.txt


Run the Flask app:
flask run

The application will be available at http://127.0.0.1:5000.
License
This project is licensed under the MIT License. See the LICENSE file for details.
