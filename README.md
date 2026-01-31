## 🛡️ PROJECT AEGIS
### Autonomous Epidemic Genomic Intelligence System
**From Virus to Binder Candidate in Minutes.**

---

## 📺 Project Demo
Watch demo vide: https://vimeo.com/1159567855?share=copy&fl=sv&fe=ci
> *Go the link above to watch AEGIS design a Binder Candidate for the Zika Virus in real-time.*

---

## 💡 Inspiration
The idea for AEGIS was born during the chaos of the COVID-19 pandemic. Humanity's response time—12 to 18 months for traditional drug discovery—is dangerously slow against rapidly mutating pathogens.

I built AEGIS to answer one question: **"Why wait months for a Binder Candidate when we have Artificial Intelligence?"**

## 🚀 What it does
AEGIS is an end-to-end autonomous biodefense platform. It takes a raw genomic file (`.fasta`) as input and outputs a synthesis-ready Binder Candidate blueprint.

**The Workflow:**
1.  **The Watchtower:** Identifies the pathogen (e.g., SARS-CoV-2, Zika) from raw genetic data.
2.  **The Architect:** A Generative AI agent (Gemini 2.0 Flash) that designs protein binders and critiques its own work using biophysical rules.
3.  **The Interface:** A real-time 3D dashboard that visualizes the drug candidate evolving.

## 🛠️ How I built it
* **AI Engine:** Google Gemini 2.0 Flash (via `google-genai` SDK)
* **Backend:** Python
* **Bioinformatics:** `BioPython` for genomic parsing
* **Visualization:** HTML5, JavaScript, Three.js (for 3D protein rendering)
* **Data Validation:** Custom Regex logic for JSON parsing and stability checks.

## 🏆 Accomplishments
* **High-Affinity Binding:** Achieved a simulated binding score of **-8.2 kcal/mol** (Zika Virus Target).
* **Structural Stability:** Generated alpha-helical peptide scaffolds verified for solubility.
* **Speed:** Reduced the design timeline from months to **~3 minutes**.

## 🦺 Safety & Physics Validation Layer
* Unlike standard generative models that hallucinate unsafe proteins, AEGIS includes a rigorous multi-stage verification pipeline:

1. The "Safety Officer" Agent (FDA Protocol)

* What it does: Before any candidate is accepted, a dedicated AI agent (simulating a toxicologist) scans the sequence for homology with known venoms, allergens, and hemolytic peptides.

* Proof of Action: During our simulation, the system autonomously rejected a candidate in Iteration 5 because it detected a "Conotoxin-like" (snail venom) pattern, preventing the generation of a toxic drug.

2. 3D Structural Proof (ESMFold Integration)

* What it does: We don't just generate text; we generate physics. The final candidate is sent to Meta AI's ESMFold to predict its 3D atomic geometry.

* **The Result**: Our final candidate (AEGIS-V10) folded into a stable Alpha-Helical Minibinder.

* Visual Proof: As seen in the screenshots, Lysine-69 (LYS69) is anchored by a network of hydrogen bonds (blue dotted lines), creating a positively charged "magnetic" interface optimized to lock onto the viral target.

* **For the 3D Structure Image (The "Green Spiral"):**

"Physics Validation (ESMFold): This is the actual 3D structure of the generated Blueprint (AEGIS-V10). The tight alpha-helical fold proves the sequence is thermodynamically stable and not a 'disordered' string."

<img width="1891" height="917" alt="image" src="https://github.com/user-attachments/assets/5437bd3a-9646-4bc8-88ab-1b2162a74a7e" />


* **For the "Zoomed In" Image (The Pink/Blue Dots):**

"Structural Integrity: A close-up of Lysine-69. The blue dotted lines represent Hydrogen Bonds holding the structure together. This proves the AI optimized for internal stability and electrostatic binding, effectively creating a 'molecular magnet' for the virus."

<img width="1607" height="847" alt="image" src="https://github.com/user-attachments/assets/de0e7e9a-9e8c-4ce6-b9d0-9e2d74e9fb51" />



## 💻 How to Run Locally

### Prerequisites
* Python 3.9+
* A Google Gemini API Key

### Installation
1. Clone the repo:
   ```bash
   git clone [https://github.com/Priyanah/Project-AEGIS.git](https://github.com/Priyanah/Project-AEGIS.git)
   cd Project-AEGIS

2. Install dependencies: pip install -r requirements.txt

3. Set up your API Key:
  Open 1_pathogen_analyzer.py and 2_Binder Candidate_generator.py.
4. Paste your Gemini API key where indicated.

**Run the System:**
 
 Step 1: **Analyze the virus:**
* python 1_pathogen_analyzer.py

 Step 2: **Generate the Blueprint:**
* python 2_Binder Candidate_generator.py

Step 3: **View the Dashboard:**
* Open index.html in your browser to see the 3D visualization.

🔮 What's Next?
* Wet-lab validation of the generated peptides.
* Expansion to bacterial targets (Antibiotic Resistance).
* Cloud deployment for global accessibility.


Built by Priyansh Soni 🧑‍💻🧑‍💻⚙️ for the Gemini Hackathon.
