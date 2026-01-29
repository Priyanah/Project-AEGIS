## 🛡️ PROJECT AEGIS
### Autonomous Epidemic Genomic Intelligence System
**From Virus to Vaccine in Minutes.**

---

## 📺 Project Demo
Watch demo vide: https://vimeo.com/1159567855?share=copy&fl=sv&fe=ci
> *Go the link above to watch AEGIS design a vaccine for the Zika Virus in real-time.*

---

## 💡 Inspiration
The idea for AEGIS was born during the chaos of the COVID-19 pandemic. Humanity's response time—12 to 18 months for traditional drug discovery—is dangerously slow against rapidly mutating pathogens.

I built AEGIS to answer one question: **"Why wait months for a vaccine when we have Artificial Intelligence?"**

## 🚀 What it does
AEGIS is an end-to-end autonomous biodefense platform. It takes a raw genomic file (`.fasta`) as input and outputs a synthesis-ready vaccine blueprint.

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
  Open 1_pathogen_analyzer.py and 2_vaccine_generator.py.
4. Paste your Gemini API key where indicated.

**Run the System:**
 
 Step 1: **Analyze the virus:**
* python 1_pathogen_analyzer.py

 Step 2: **Generate the cure:**
* python 2_vaccine_generator.py

Step 3: **View the Dashboard:**
* Open index.html in your browser to see the 3D visualization.

🔮 What's Next?
* Wet-lab validation of the generated peptides.
* Expansion to bacterial targets (Antibiotic Resistance).
* Cloud deployment for global accessibility.


Built by Priyansh Soni 🧑‍💻🧑‍💻⚙️ for the Gemini Hackathon.
