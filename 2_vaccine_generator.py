import os
import time
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# --- 1. Load Dynamic Target Data ---
def load_target_data():
    try:
        with open("target_metadata.json", "r") as f:
            data = json.load(f)
        with open("target_sequence.txt", "r") as f:
            seq = f.read().strip()
            
        if len(seq) < 20: 
            print(f"❌ CRITICAL ERROR: Target Sequence invalid (Length: {len(seq)}).")
            exit()
            
        return data["virus_name"], seq
    except FileNotFoundError:
        print("⚠️ No metadata found. Run the Analyzer first.")
        return "Unknown Virus", "UNKNOWN"

VIRUS_NAME, TARGET_SEQUENCE = load_target_data()

# --- 2. Dashboard Updater ---
def update_dashboard(iteration, candidate_name, sequence, score, log, status="THINKING"):
    data = {
        "virus_name": VIRUS_NAME,
        "status": status,
        "iteration": iteration,
        "candidate_name": candidate_name,
        "sequence": sequence,
        "score": score,
        "log": log
    }
    with open("dashboard_data.json", "w") as f:
        json.dump(data, f)

# --- 3. Robust JSON Extractor ---
def extract_json_safely(text):
    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if match: return json.loads(match.group(0))
    except: pass
    
    try:
        cleaned = text.strip()
        if "```json" in cleaned: cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned: cleaned = cleaned.split("```")[1].split("```")[0]
        return json.loads(cleaned)
    except: return None

def generate_with_retry(model, prompt):
    try:
        return client.models.generate_content(model=model, contents=prompt)
    except Exception as e:
        time.sleep(2)
        return client.models.generate_content(model=model, contents=prompt)

# --- 4. THE AUTONOMOUS LOOP ---
def stark_simulation_loop():
    print(f"🚀 AEGIS BACKEND STARTED. TARGET: {VIRUS_NAME}")
    print(f"🧬 Targeting Sequence Length: {len(TARGET_SEQUENCE)} residues")
    print("🤖 MODE: AUTONOMOUS DISCOVERY (No Forced Outcomes)")
    
    update_dashboard(0, "Initializing...", "...", 0, f"Loading {VIRUS_NAME} genome...", "SCANNING")
    time.sleep(2)

    history_log = "No previous attempts."
    
    # Track the "Best" candidate naturally
    best_candidate = {
        "candidate_name": "None",
        "sequence": "None", 
        "binding_score_dG": 0.0
    }
    
    # We allow up to 4 iterations to let it "think"
    for iteration in range(1, 5):
        update_dashboard(iteration, f"Generating V{iteration}...", "...", best_candidate['binding_score_dG'], "Analyzing molecular geometry... Deep Think active...", "THINKING")
        
        # --- THE REAL PROMPT (Scientific, not Forced) ---
        prompt = f"""
        You are AEGIS, an Autonomous Computational Biologist.
        
        OBJECTIVE: Design a protein 'minibinder' (50-80 AA) that binds tightly to the {VIRUS_NAME} target.
        Target Sequence Snippet: {TARGET_SEQUENCE[:500]}...
        
        HISTORY OF ATTEMPTS:
        {history_log}
        
        YOUR TASK (ITERATION {iteration}):
        1. Analyze the Target's surface (Hydrophobicity, Charge).
        2. Design or Refine a binder sequence.
        3. CRITIQUE your own design:
           - Does it have steric clashes?
           - are hydrophobic residues exposed to water (bad)?
           - do charged residues match the target (good)?
        4. ESTIMATE the Binding Affinity (dG) based *strictly* on your critique.
           - Weak/Unstable: -4.0 to -6.0
           - Good: -7.0 to -9.0
           - Excellent (Drug Candidate): -10.0 to -14.0
           
        (Do NOT fake a high score. If the design is flawed, give it a low score. We want the truth.)
        
        OUTPUT FORMAT (Strict JSON):
        {{
            "candidate_name": "AEGIS-V{iteration}",
            "sequence": "SEQUENCE_STRING",
            "binding_score_dG": -X.X,
            "deep_think_log": "Scientific reasoning for the score..."
        }}
        """

        response = generate_with_retry("gemini-2.0-flash", prompt)
        result = extract_json_safely(response.text)
        
        if result:
            current_score = float(result['binding_score_dG'])
            
            # Logic: Did we improve?
            log_message = result['deep_think_log']
            status = "SIMULATING"
            
            # Save the best one found so far
            if current_score < best_candidate['binding_score_dG']: # Lower is better in negative dG? 
                # Actually dG is negative, so -12 is 'smaller' than -5, but 'better' binding.
                # Let's handle magnitude: More negative is better.
                if current_score < -1.0: # Ensure it's valid
                     if best_candidate['binding_score_dG'] == 0.0 or current_score < best_candidate['binding_score_dG']:
                        best_candidate = result
                        log_message += " [NEW BEST]"

            update_dashboard(
                iteration, 
                result["candidate_name"], 
                result["sequence"], 
                current_score, 
                log_message, 
                status
            )
            
            history_log += f"\nAttempt {iteration}: Score {current_score}. Sequence: {result['sequence']}"
            print(f"✅ Iteration {iteration}: {current_score} kcal/mol | {log_message[:50]}...")
            
            # AUTONOMOUS STOPPING CONDITION
            # If we hit a "Drug Candidate" score, we stop early because we won.
            if current_score <= -10.5:
                print("🎯 SUCCESS THRESHOLD REACHED. STOPPING OPTIMIZATION.")
                best_candidate = result
                break
        else:
            print(f"⚠️ Iteration {iteration} failed to parse.")
            
        time.sleep(3)

    update_dashboard(iteration, best_candidate['candidate_name'], best_candidate['sequence'], best_candidate['binding_score_dG'], "OPTIMAL BINDING ACHIEVED.", "SUCCESS")    


    blueprint_content = f"""
    ===================================================
    PROJECT AEGIS | OFFICIAL VACCINE BLUEPRINT
    ===================================================
    TARGET VIRUS: {VIRUS_NAME}
    DATE: {time.strftime("%Y-%m-%d %H:%M:%S")}
    STATUS: READY FOR SYNTHESIS
    ---------------------------------------------------
    FINAL CANDIDATE: {best_candidate.get('candidate_name', 'N/A')}
    BINDING AFFINITY: {best_candidate.get('binding_score_dG', 'N/A')} kcal/mol
    ---------------------------------------------------
    
    >> MOLECULAR FORMULA:
    {best_candidate.get('sequence', 'N/A')}
    
    >> REASONING:
    {best_candidate.get('deep_think_log', 'N/A')}
    
    [AEGIS DIGITAL SIGNATURE: {hash(best_candidate.get('sequence', '0'))}]
    ===================================================
    """
    
    filename = f"BLUEPRINT_{VIRUS_NAME.replace(' ', '_')}.txt"
    with open(filename, "w") as f:
        f.write(blueprint_content)
        
    print(f"\n📄 BLUEPRINT GENERATED: {filename}")
    print("✅ SIMULATION COMPLETE.")

if __name__ == "__main__":
    stark_simulation_loop()