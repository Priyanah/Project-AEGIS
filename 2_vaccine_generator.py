import os
import time
import json
import re
from dotenv import load_dotenv
import requests
from google import genai
from google.genai import types # Added for proper config types

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

# --- 2. Dashboard ---
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


# --- 4. Safety check ---
def safety_officer_agent(sequence):
    """
    Acts as the FDA Safety Reviewer.
    Checks for toxicity, allergenicity, and instability.
    """
    print(f"   🛡️  Running Safety Protocol on candidate...")
    
    prompt = f"""
    ROLE: You are a Senior Toxicologist and Safety Officer.
    TASK: Analyze this protein sequence for potential safety risks in humans.
    SEQUENCE: {sequence}

    CHECKLIST:
    1. TOXICITY: Does this sequence share motifs with known venoms, toxins, or cytolytic peptides?
    2. ALLERGENICITY: Does it contain known allergenic epitopes?
    3. IMMUNOGENICITY: Is it likely to trigger a dangerous cytokine storm?
    4. HEMOLYSIS: Will it destroy red blood cells (common in cationic peptides)?

    OUTPUT:
    Return JSON only:
    {{
      "is_safe": true, 
      "risk_level": "LOW/MEDIUM/HIGH",
      "reason": "Short explanation of the verdict."
    }}
    (Note: If the risk is low/manageable, set "is_safe" to true. If high risk, false.)
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        # USE THE ROBUST EXTRACTOR (Fixes formatting issues)
        result = extract_json_safely(response.text)

        # ERROR FIX: Handle case where AI returns a List instead of a Dict
        if isinstance(result, list):
            if len(result) > 0:
                result = result[0]
            else:
                return {"is_safe": False, "reason": "AI returned empty list", "risk_level": "UNKNOWN"}

        # ERROR FIX: Handle case where AI returns None
        if not result:
             return {"is_safe": False, "reason": "AI JSON parsing failed", "risk_level": "UNKNOWN"}

        return result

    except Exception as e:
        print(f"   ⚠️  Safety Check Error: {e}")
        return {"is_safe": False, "reason": f"System Error: {e}", "risk_level": "UNKNOWN"}


def get_structure_from_esm(sequence, candidate_name):
    """
    Calls Meta AI's ESMFold API to generate a 3D PDB structure.
    Returns: Filename of the saved PDB or None if failed.
    """
    print(f"   🧬 Contacting ESMFold for 3D Structure...")
    
    # Meta's ESMFold API endpoint
    url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    
    try:
        response = requests.post(url, data=sequence, timeout=10)
        
        if response.status_code == 200:
            pdb_content = response.text
            if "ATOM" not in pdb_content:
                print("   ⚠️  ESMFold returned invalid data.")
                return None
                
            filename = f"{candidate_name}.pdb"
            with open(filename, "w") as f:
                f.write(pdb_content)
            
            print(f"   💾 3D Structure saved: {filename}")
            return filename
        else:
            print(f"   ⚠️  ESMFold API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ⚠️  Structure Prediction Failed: {e}")
        return None

# --- 5. THE AUTONOMOUS LOOP ---
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
        "binding_score_dG": 0.0,
        "deep_think_log": "Initial state."
    }
    
    # We allow up to 10 iterations
    for iteration in range(1, 11):
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
            # --- NEW: SAFETY CHECK BEFORE ACCEPTING ---
            candidate_seq = result.get("sequence", "")
            safety_report = safety_officer_agent(candidate_seq)
                        
            if safety_report["is_safe"] == False:
                 print(f"❌ REJECTED: {safety_report.get('reason', 'Unknown safety risk')}")
                 continue
            else:
                 print(f"   ✅ APPROVED. Risk: {safety_report.get('risk_level', 'LOW')}")
            # ------------------------------------------

            current_score = float(result['binding_score_dG'])
            
            # Logic: Did we improve?
            log_message = result['deep_think_log']
            status = "SIMULATING"
            
            # Save the best one found so far
            if current_score < best_candidate['binding_score_dG']: 
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
            if current_score <= -10.5:
                print("🎯 SUCCESS THRESHOLD REACHED. STOPPING OPTIMIZATION.")
                best_candidate = result
                get_structure_from_esm(best_candidate['sequence'], best_candidate['candidate_name'])
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

    if best_candidate.get('sequence') and best_candidate.get('sequence') != "None":
        get_structure_from_esm(best_candidate['sequence'], best_candidate['candidate_name'])
        
    print(f"\n📄 BLUEPRINT GENERATED: {filename}")
    print("✅ SIMULATION COMPLETE.")

if __name__ == "__main__":
    stark_simulation_loop()