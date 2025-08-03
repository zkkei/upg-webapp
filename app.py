# UPG Strategic Co-Pilot (Web Application)
# Flask Backend
# Developed by Gemini for Goat (@emmzrig)

from flask import Flask, render_template, request

app = Flask(__name__)

# --- Constants & Core Logic ---
# This is the "Harsh Reality" model (v6.4) we perfected.

CAMPUS_CUTOFFS = {
    "UP Diliman": 2.174, "UP Manila": 2.580, "UP Los Baños": 2.600, 
    "UP Baguio": 2.700, "UP Visayas": 2.700, "UP Cebu": 2.800,
    "UP Mindanao": 2.800, "UP Open University": 2.800, "UP Tacloban": 2.800,
}

PALUGIT_BONUS = -0.05

WEIGHTS = {
    'hs': 0.40, 'math': 0.18, 'sci': 0.18, 'lang': 0.12, 'read': 0.12
}

COMPETITIVENESS_EXPONENT = 2.15
TARGET_THRESHOLD = 0.15

def score_to_upg_scale(score):
    """
    Converts a 0-100 score to a 1-5 UPG scale using the non-linear,
    competitive model.
    """
    if score < 0: score = 0
    normalized_score = score / 100
    competitive_score = normalized_score ** COMPETITIVENESS_EXPONENT
    return 1 + (1 - competitive_score) * 4

def compute_upg(scores):
    """Computes the UPG from a dictionary of validated scores."""
    hs_component = score_to_upg_scale(scores['hs']) * WEIGHTS['hs']
    math_component = score_to_upg_scale(scores['math']) * WEIGHTS['math']
    sci_component = score_to_upg_scale(scores['sci']) * WEIGHTS['sci']
    lang_component = score_to_upg_scale(scores['lang']) * WEIGHTS['lang']
    read_component = score_to_upg_scale(scores['read']) * WEIGHTS['read']
    
    base_upg = hs_component + math_component + sci_component + lang_component + read_component
    
    modifiers_applied = []
    if scores['hs_type'] == "Public/Barangay":
        base_upg += PALUGIT_BONUS
        modifiers_applied.append(f"Palugit ({PALUGIT_BONUS:.2f})")
        
    return base_upg, ", ".join(modifiers_applied)

def determine_outcome(upg, c1_choice, c2_choice):
    """Determines the admission outcome and strategic analysis."""
    c1_cutoff = CAMPUS_CUTOFFS.get(c1_choice, 999)
    c2_cutoff = CAMPUS_CUTOFFS.get(c2_choice, 999)

    outcome = ""
    analysis = ""

    if upg <= c1_cutoff:
        outcome = f"✅ Likely to qualify for {c1_choice} (cutoff: {c1_cutoff:.3f})"
        if upg < c1_cutoff - TARGET_THRESHOLD: analysis = f"{c1_choice} is a 'Safety' choice."
        else: analysis = f"{c1_choice} is a 'Target' choice."
    elif upg <= c2_cutoff:
        outcome = f"⚠️ May qualify for {c2_choice} (cutoff: {c2_cutoff:.3f})\n   Did not meet {c1_choice} cutoff ({c1_cutoff:.3f})"
        if upg < c2_cutoff - TARGET_THRESHOLD: analysis = f"{c1_choice} was a 'Reach', but {c2_choice} is a 'Safety' choice."
        else: analysis = f"{c1_choice} was a 'Reach', but {c2_choice} is a 'Target' choice."
    else:
        outcome = f"❌ May not qualify for chosen campuses\n   {c1_choice}: {c1_cutoff:.3f} | {c2_choice}: {c2_cutoff:.3f}"
        analysis = f"Both {c1_choice} and {c2_choice} are 'Reach' choices with this UPG."
        
    return outcome, analysis

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles both the initial page load (GET) and the form submission for
    calculation (POST).
    """
    # Pass campus options to the template for the dropdowns
    campus_options = list(CAMPUS_CUTOFFS.keys())
    results = None
    
    if request.method == 'POST':
        try:
            # Collect and validate scores from the form
            scores = {
                'math': float(request.form['math']),
                'sci': float(request.form['sci']),
                'lang': float(request.form['lang']),
                'read': float(request.form['read']),
                'hs': float(request.form['hs']),
                'hs_type': request.form['hs_type']
            }
            
            # Ensure scores are within a valid range
            for key, value in scores.items():
                if isinstance(value, float) and not (0 <= value <= 100):
                    # Handle error gracefully if needed, for now we assume client-side validation
                    pass

            c1_choice = request.form['campus1']
            c2_choice = request.form['campus2']

            final_upg, modifiers = compute_upg(scores)
            outcome_text, analysis_text = determine_outcome(final_upg, c1_choice, c2_choice)

            results = {
                'upg': f"{final_upg:.4f}",
                'modifiers': modifiers if modifiers else 'None',
                'outcome': outcome_text,
                'analysis': analysis_text
            }

        except (ValueError, KeyError) as e:
            # Handle cases where form data is missing or not a number
            results = {'error': f"Invalid input. Please ensure all fields are filled correctly. Error: {e}"}

    return render_template('index.html', campus_options=campus_options, results=results)

if __name__ == '__main__':
    # This is for local development only.
    # The production server (Gunicorn) will run the app differently.
    app.run(debug=True)
