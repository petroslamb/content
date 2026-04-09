import yaml

# Load the current audit
INPUT_PATH = 'publication_strategy_and_archive/editorial_atlas/rubric_assessments_gemini_3_flash.yaml'
OUTPUT_PATH = 'publication_strategy_and_archive/editorial_atlas/rubric_assessments_gemini_3_flash.yaml'

with open(INPUT_PATH, 'r') as f:
    data = yaml.safe_load(f)

# Anchor Map (Target 10s and 9s for direct scores)
# dimensions: debate, precision, synthesis, utility
anchors = {
    'The Transformer Attractor': {'debate': 10, 'precision': 7, 'synthesis': 7, 'utility': 6},
    'The Hardware Friction Map': {'debate': 7, 'precision': 10, 'synthesis': 8, 'utility': 10},
    'The Binding Gap': {'debate': 6, 'precision': 10, 'synthesis': 8, 'utility': 7},
    'What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)': {'debate': 7, 'precision': 9, 'synthesis': 10, 'utility': 8},
    'Neural Architecture Design as a Reusable Scaffold: A History Review': {'debate': 6, 'precision': 7, 'synthesis': 9, 'utility': 7},
    'The Autonomy Tax': {'debate': 9, 'precision': 8, 'synthesis': 7, 'utility': 9},
    'Operating Agents III: Reasoning Scaffolds and Planning': {'debate': 7, 'precision': 8, 'synthesis': 8, 'utility': 10},
}

def derive_average(subscores):
    values = [v for v in subscores.values() if isinstance(v, (int, float))]
    if not values: return 7
    return int(round(sum(values) / len(values)))

def derive_power(traction, craft):
    return int(round((0.6 * traction) + (0.4 * craft)))

for essay in data['essays']:
    title = essay['title']
    
    # 1. Apply Direct Score Calibration
    if title in anchors:
        essay['direct_scores'].update(anchors[title])
    else:
        # Default de-regulation for everything else (Shift Baseline to 7)
        for k, v in essay['direct_scores'].items():
            if v >= 9: essay['direct_scores'][k] = 8
            elif v == 8: essay['direct_scores'][k] = 7
            
    # 2. Re-calibrate Traction Subscores
    for k, v in essay['traction_subscores'].items():
        if title == 'The Transformer Attractor' and k in ['hook_strength', 'thesis_compression', 'debate_energy']:
            essay['traction_subscores'][k] = 10
        elif title == 'The Hardware Friction Map' and k in ['thesis_compression', 'frame_portability', 'public_packaging']:
            essay['traction_subscores'][k] = 10
        elif title == 'The Binding Gap' and k in ['thesis_compression']:
            essay['traction_subscores'][k] = 10
        else:
            # Shift baseline down
            if v >= 9: essay['traction_subscores'][k] = 8
            elif v == 8: essay['traction_subscores'][k] = 7

    # 3. Re-calibrate Craft Subscores (Reserved 10s only for exceptional rhythm)
    for k, v in essay['craft_subscores'].items():
        if v >= 9: essay['craft_subscores'][k] = 8
        elif v == 8: essay['craft_subscores'][k] = 7
    
    if title in ['The Transformer Attractor', 'The Moltbook Phenomenon']:
        essay['craft_subscores']['sentence_rhythm'] = 9

    # 4. Re-calibrate Section Scores
    for k, v in essay['section_scores'].items():
        if v >= 9: essay['section_scores'][k] = 8
        elif v == 8: essay['section_scores'][k] = 7
        
    if title == 'The Transformer Attractor':
        essay['section_scores']['opening'] = 10
        essay['section_scores']['thesis_lock'] = 10
    if title == 'The Hardware Friction Map':
        essay['section_scores']['thesis_lock'] = 10
        essay['section_scores']['borders'] = 10

    # 5. Handle rationales (ensure they don't sound like "10" if they are "7")
    note = essay['rationale']['whole_essay_note']
    if essay['direct_scores']['precision'] < 10 and 'definitive' in note.lower():
        essay['rationale']['whole_essay_note'] = note.replace('definitive', 'strong').replace('Definitive', 'Strong')

# Write back
with open(OUTPUT_PATH, 'w') as f:
    yaml.dump(data, f, sort_keys=False, width=1000)
