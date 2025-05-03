# TinkerHub Campus Lead Application Evaluator

This AI model evaluates anonymized TinkerHub campus lead applications based on predefined criteria and guidelines.

## Features

- Automated scoring of applications (1-10 scale)
- Structured feedback generation
- Analysis of both structured and text-based fields
- Alignment with TinkerHub's values and requirements

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from evaluator import evaluate_application

# Example application
application = {
    "role": "Student",
    "experience": "Led coding club activities",
    "current_year": "Year 2",
    "vision_for_campus_community": "Create inclusive tech learning space",
    "challenges_and_solutions": "Addressing accessibility issues",
    "belief_in_tinkerhub": 5,
    "planned_programs": "Monthly hackathons",
    "projects_completed": "Built campus portal",
    "how_they_know_tinkerhub": "WhatsApp",
    "willing_to_travel": "Yes",
    "read_wiki": "Yes",
    "agreement_to_not_lead_elsewhere": "Yes"
}

# Evaluate the application
result = evaluate_application(application)
print(result)
```

## Output Format

The evaluator returns a dictionary with three fields:

1. `Your Score (1-10)`: Numerical score based on the scoring guidelines
2. `Positive Feedback`: Brief feedback highlighting strengths (<50 words)
3. `Areas of Concern`: Constructive feedback on potential areas for improvement (10-50 words)

## Evaluation Criteria

The model considers:
- Academic eligibility (Year 1-3)
- Leadership experience
- Community-first mindset
- Project completion
- Program planning
- Alignment with TinkerHub values
- Travel willingness
- Preparation (wiki reading)
- Commitment (agreement to not lead elsewhere)

## Scoring Guidelines

- 1-3: Does not meet requirements
- 4-6: Meets basic requirements
- 7-8: Strong candidate
- 9-10: Exceptional candidate

## Notes

- All applications are processed anonymously
- The model is designed to be objective and consistent
- Final selection is made through interviews by TinkerHub Foundation 