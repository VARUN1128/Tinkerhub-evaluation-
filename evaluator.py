import re
from typing import Dict, Tuple

class TinkerHubEvaluator:
    def __init__(self):
        pass

    def evaluate_application(self, application: Dict) -> Tuple[int, str, str]:
        application = self._validate_and_fill_defaults(application)
        score, positives, concerns = 0, [], []

        # Academic eligibility
        year = application['current_year']
        if year not in ['Year 1', 'Year 2', 'Year 3']:
            concerns.append("Not eligible: must be in Year 1-3.")
            return 1, "Not eligible.", "Final year students are not eligible."
        else:
            score += 1

        # Travel readiness
        travel_ready = self._is_yes(application['willing_to_travel'])
        if travel_ready:
            score += 1
            positives.append("willingness to travel")
        else:
            concerns.append("Not willing to travel; may miss key events.")

        # Read Wiki
        read_wiki = self._is_yes(application['read_wiki'])
        if read_wiki:
            score += 1
            positives.append("thorough preparation (read wiki)")
        else:
            concerns.append("Has not read the wiki; may lack context.")

        # Agreement to not lead elsewhere
        agreement = self._is_yes(application['agreement_to_not_lead_elsewhere'])
        if agreement:
            score += 1
        else:
            concerns.append("Did not agree to not lead elsewhere.")

        # Belief in TinkerHub
        belief = int(application['belief_in_tinkerhub'])
        if belief >= 4:
            score += 1
            positives.append("strong belief in TinkerHub's mission")
        elif belief >= 2:
            score += 0.5
            concerns.append("Could show stronger belief in TinkerHub.")
        else:
            concerns.append("Low belief in TinkerHub's mission.")

        # Leadership/ownership evidence
        leadership_keywords = ["lead", "organize", "initiated", "founded", "coordinated", "ownership", "managed", "responsible", "core team", "president", "secretary", "captain", "head"]
        leadership_score = 0
        for field in ['experience', 'projects_completed', 'planned_programs', 'challenges_and_solutions']:
            text = application[field].lower()
            if any(word in text for word in leadership_keywords):
                leadership_score += 1
        if leadership_score >= 2:
            score += 2
            positives.append("clear leadership and ownership of initiatives")
        elif leadership_score == 1:
            score += 1
            concerns.append("Some leadership, but could be clearer.")
        else:
            concerns.append("No clear evidence of leadership or ownership.")

        # Community-first mindset
        community_keywords = ["community", "team", "we", "together", "help others", "peer", "collaborate", "shared", "impact", "inclusive", "support"]
        community_score = 0
        for field in ['vision_for_campus_community', 'planned_programs', 'challenges_and_solutions', 'experience']:
            text = application[field].lower()
            if any(word in text for word in community_keywords):
                community_score += 1
        if community_score >= 2:
            score += 1
            positives.append("community-first mindset")
        elif community_score == 1:
            score += 0.5
            concerns.append("Could show more community focus.")
        else:
            concerns.append("No clear community-first focus.")

        # TinkerHub/initiative participation
        tinkerhub_keywords = ["tinkerhub", "foundation", "chapter", "public initiative", "hackathon", "event", "program", "bootcamp", "workshop", "challenge"]
        participation_score = 0
        for field in ['experience', 'projects_completed', 'planned_programs']:
            text = application[field].lower()
            if any(word in text for word in tinkerhub_keywords):
                participation_score += 1
        if participation_score >= 2:
            score += 1
            positives.append("active in TinkerHub or similar initiatives")
        elif participation_score == 1:
            score += 0.5
            concerns.append("Limited initiative participation.")
        else:
            concerns.append("No clear initiative participation.")

        # Vision and program ideas
        vision_len = len(application['vision_for_campus_community'].strip())
        program_len = len(application['planned_programs'].strip())
        if vision_len > 100 and program_len > 100:
            score += 1
            positives.append("clear vision and strong program ideas")
        elif vision_len > 50 or program_len > 50:
            score += 0.5
            concerns.append("Vision or program ideas could be more detailed.")
        else:
            concerns.append("Vision and program ideas are too brief.")

        # One-year involvement (look for 'year', 'months', 'since', 'long', 'ongoing')
        involvement_keywords = ["year", "months", "since", "long", "ongoing"]
        involvement_score = 0
        for field in ['experience', 'projects_completed']:
            text = application[field].lower()
            if any(word in text for word in involvement_keywords):
                involvement_score += 1
        if involvement_score >= 1:
            score += 1
            positives.append("shows ongoing involvement")
        else:
            concerns.append("No clear evidence of ongoing involvement.")

        # --- HARD CAPS for critical requirements ---
        if not read_wiki:
            score = min(score, 7)
        if not agreement:
            score = min(score, 6)
        if not travel_ready:
            score = min(score, 6)
        if belief < 4:
            score = min(score, 7)

        # Clamp score and assign band
        score = int(min(10, max(1, round(score))))

        # Only give a 10 if all critical requirements are met and there are no concerns
        if score == 10:
            if not (read_wiki and agreement and travel_ready and belief >= 4):
                score = 9
            elif len([c for c in concerns if c.strip()]) > 0:
                score = 9

        if score <= 3:
            band = "Does not meet requirements"
        elif score <= 6:
            band = "Meets basic requirements"
        elif score <= 8:
            band = "Strong candidate"
        else:
            band = "Exceptional candidate"

        # Feedback
        if positives:
            positive_feedback = (
                "Positive aspects: " + "; ".join([p[0].upper() + p[1:] for p in positives])
            )
        else:
            positive_feedback = "Meets basic requirements."

        if concerns:
            area_of_concern = (
                "Areas of concern: " + "; ".join([c[0].upper() + c[1:] for c in concerns])
            )
        else:
            area_of_concern = "No major concerns identified."

        return score, positive_feedback, area_of_concern

    def _is_yes(self, val):
        return str(val).strip().lower() in ['yes', 'true', 'on', '1']

    def _validate_and_fill_defaults(self, application: Dict) -> Dict:
        defaults = {
            'role': 'Student',
            'current_year': 'Year 1',
            'experience': '',
            'vision_for_campus_community': '',
            'challenges_and_solutions': '',
            'belief_in_tinkerhub': 1,
            'planned_programs': '',
            'projects_completed': '',
            'how_they_know_tinkerhub': '',
            'willing_to_travel': 'No',
            'read_wiki': 'No',
            'agreement_to_not_lead_elsewhere': 'No'
        }
        for key, default in defaults.items():
            value = application.get(key, default)
            if key == 'belief_in_tinkerhub':
                try:
                    value = int(value)
                    if value < 1 or value > 5:
                        value = 1
                except (ValueError, TypeError):
                    value = 1
            if value is None:
                value = default
            application[key] = value
        return application

def evaluate_application(application: Dict) -> Dict:
    evaluator = TinkerHubEvaluator()
    score, positive_feedback, areas_of_concern = evaluator.evaluate_application(application)
    return {
        "Your Score (1-10)": score,
        "Positive Feedback": positive_feedback,
        "Areas of Concern": areas_of_concern
    } 