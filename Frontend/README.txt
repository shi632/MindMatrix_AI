═══════════════════════════════════════════════════════════════
  MIND MATRIX – Mental Health Diagnostics
  Project ID : 2022CSEAI040
  Institute  : ABES Institute of Technology, Ghaziabad
  Guide      : Mrs. Monika Chauhan (Associate Professor, CSE-AI)
  Team       : Shivam Kumar Sharma · Rohit Kumar Kushwaha
               Siddhant Jain · Riyansh Srivastav
═══════════════════════════════════════════════════════════════

FILES IN THIS FOLDER
───────────────────
  index.html   – Main webpage (HTML structure + layout)
  style.css    – All styling (dark theme, animations, responsive)
  app.js       – All logic (Naive Bayes model + Claude AI API)
  README.txt   – This file


HOW TO RUN ON YOUR LAPTOP (no installation needed)
────────────────────────────────────────────────────

  STEP 1 — Open the folder
    Right-click the "mindmatrix" folder → Open in File Explorer

  STEP 2 — Open index.html
    Double-click "index.html"
    It will open in your default browser (Chrome recommended)

  STEP 3 — That's it!
    The app will load. You do NOT need Node.js, Python, or any server.


HOW TO GET THE ANTHROPIC API KEY (FREE)
────────────────────────────────────────
  1. Go to: https://console.anthropic.com
  2. Sign up with your email (free account)
  3. Click "API Keys" in the left sidebar
  4. Click "Create Key" → Copy the key (starts with sk-ant-api03-...)
  5. When the app asks for the API key, paste it there
  6. The key is saved in your browser — you only need to enter it ONCE

  ⚠️  Keep your API key private. Do not share it publicly.
  ⚠️  Free tier gives you $5 of credits — enough for hundreds of tests.


IF THE AI DOCTOR SECTION DOES NOT LOAD
────────────────────────────────────────
  The app has a built-in FALLBACK REPORT. Even without a valid API key,
  the Naive Bayes scores and a pre-written report will still be shown.
  This is useful for offline demos / college presentations.


HOW THE NAIVE BAYES MODEL WORKS (for your viva)
────────────────────────────────────────────────
  1. User selects symptoms → treated as a binary feature vector
     (1 = symptom present, 0 = absent)

  2. Bernoulli Naive Bayes formula:
     P(Class | Features) ∝ P(Class) × ∏ P(Feature_i | Class)

  3. Laplace smoothing applied to avoid zero-probability features:
     P(Feature_i | Class) = (count + 1) / (total_features + 2)

  4. Four output scores computed:
     • Depression Risk  (Emotional symptom features + mood/sleep priors)
     • Anxiety Level    (Anxiety symptoms + stress/energy priors)
     • Stress Score     (Stress features + self-reported slider)
     • Wellbeing Index  (Composite: mood + sleep + energy – risk avg)

  5. Scores passed to Claude AI for natural language diagnosis + advice.


PROJECT STRUCTURE (for your report)
─────────────────────────────────────
  Frontend  : HTML5, CSS3, Vanilla JavaScript (no frameworks)
  ML Model  : Bernoulli Naive Bayes (implemented in app.js Section 4)
  AI Doctor : Claude AI API (claude-sonnet-4-20250514)
  Data      : User-input structured + unstructured (free text)
  Metrics   : Depression%, Anxiety%, Stress%, Wellbeing% (0-100 scale)


DEMO FLOW (for college presentation)
──────────────────────────────────────
  1. Open index.html in Chrome
  2. Enter: Reg No = 2202901520152, Name = Shivam Kumar Sharma
  3. Select mood = "Bad 😔"
  4. Type: "Feeling very stressed about exams, not sleeping well"
  5. Sleep = 3, Energy = 3
  6. Select symptoms: Anxiety/worry, Sleep problems, Difficulty concentrating,
     Academic pressure, Fatigue, Negative thoughts
  7. Stress = 8
  8. Click "Analyze & Get Report"
  9. Shows animated analysis → Full AI Doctor report

═══════════════════════════════════════════════════════════════
