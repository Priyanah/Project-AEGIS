import os
import sys
import json
import re
from dotenv import load_dotenv
from Bio import SeqIO
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def analyze_pathogen(fasta_file_path):
    if not os.path.exists(fasta_file_path):
        print(f"❌ ERROR: File {fasta_file_path} not found.")
        return

    print(f"🧬 AEGIS SYSTEM: Loading viral sample from {fasta_file_path}...")
    
    try:
        record = list(SeqIO.parse(fasta_file_path, "fasta"))[0]
        virus_genome = str(record.seq)
        header_info = record.description
    except Exception as e:
        print(f"❌ Error reading FASTA: {e}")
        return

    print(f"🔍 Sample Length: {len(virus_genome)} base pairs.")
    print("🧠 AEGIS BRAIN: Analyzing genome structure...")

    # THE FIX: We explicitly ask for the sequence inside the JSON
    prompt_analysis = f"""
    You are AEGIS. Analyze this viral genome.
    Header: {header_info}
    Genome Sample (First 4000 chars): {virus_genome[:4000]}
    
    TASK:
    1. Identify the Virus Name.
    2. Identify the Target Protein (Spike/Glycoprotein).
    3. EXTRACT or PREDICT the Amino Acid Sequence of that target. 
       (If you can't translate it exactly, generate the standard reference sequence for this virus's target protein).
    
    OUTPUT FORMAT (Strict JSON):
    {{
        "virus_name": "Name Here",
        "target_protein": "Protein Name",
        "analysis_summary": "Brief explanation...",
        "target_sequence": "PASTE_FULL_AMINO_ACID_SEQUENCE_HERE"
    }}
    """
    
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt_analysis)
        
        # EXTRACT JSON SAFELY
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            
            # CHECK FOR FAILURE
            seq = data.get("target_sequence", "")
            if len(seq) < 10 or "placeholder" in seq.lower():
                print("⚠️ AI failed to extract sequence. Retrying with explicit extraction...")
                # Fallback: Force it to generate just the sequence
                fallback_resp = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"For {data['virus_name']}, output the amino acid sequence of the {data['target_protein']}. Output ONLY the sequence string."
                )
                seq = fallback_resp.text.strip()
                data["target_sequence"] = seq

            # Save Metadata
            with open("target_metadata.json", "w") as f:
                json.dump(data, f)
                
            # Save Sequence (The Critical File)
            with open("target_sequence.txt", "w") as f:
                f.write(seq)
                
            print("\n--------- ANALYSIS REPORT ---------")
            print(f"🦠 Virus Detected: {data['virus_name']}")
            print(f"🎯 Target: {data['target_protein']}")
            print(f"🧬 Sequence Extracted: {len(seq)} residues")
            print("-----------------------------------")
            print("✅ Data saved correctly.")
            
        else:
            print("❌ Failed to parse JSON response.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    file_name = "fasta_files/filoviridae.fasta" # Change this to ebola_sample.fasta to test
    analyze_pathogen(file_name)