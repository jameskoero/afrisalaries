<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=AfriSalaries%20🌍&fontSize=62&fontColor=fff&animation=fadeIn&fontAlignY=38&desc=ML-Powered%20Salary%20Intelligence%20for%20African%20Tech%20Jobs&descAlignY=60&descAlign=50" width="100%"/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.1-337AB7?style=for-the-badge)](https://xgboost.readthedocs.io)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Data](https://img.shields.io/badge/Data-1%2C526_Real_Rows-00C853?style=for-the-badge)]()
[![License](https://img.shields.io/badge/Data_License-CC_BY--SA_4.0-yellow?style=for-the-badge)]()
[![Countries](https://img.shields.io/badge/Countries-8_African-FF5722?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/API-Live_on_Render-46E3B7?style=for-the-badge&logo=render)]()

<br/>

[📖 API Docs](https://afrisalaries.onrender.com/docs) · [🌐 Live App](https://afrisalaries.vercel.app) · [💻 GitHub](https://github.com/jameskoero/afrisalaries) · [🐛 Report Bug](https://github.com/jameskoero/afrisalaries/issues)

<br/>

> **"70%+ of African tech job posts hide salary information.**
> AfriSalaries predicts whether a role is LOW, MEDIUM, or HIGH relative
> to the local market — with a full breakdown of every factor that drove
> the classification. Built in Kisumu, Kenya. Trained on real data."

</div>

---

## ❗ The Problem

African tech is one of the fastest-growing talent markets on the planet — yet it remains one of the most opaque when it comes to compensation. Over 70% of tech job posts across Africa include no salary information whatsoever.

- A junior engineer in Nairobi accepts KES 80,000/month not knowing the market rate is KES 140,000
- An HR team in Amsterdam sets pay for a Lagos remote hire using European benchmarks and gets it wrong
- A startup in Accra loses candidates to a competitor that was simply transparent about pay
- A Kenyan diaspora professional returning home cannot benchmark what they should ask for after years earning in GBP or EUR

The information asymmetry is structural. Companies have salary bands. Candidates have nothing.

---

## 💡 The Solution

AfriSalaries takes any tech job description as plain text and returns a **salary band** — LOW, MEDIUM, or HIGH relative to the local market — with the salary range, country-specific median, and a ranked list of which factors drove the classification.

No account. No form. Paste the description. Get the band. Understand why.

```bash
curl -X POST https://afrisalaries.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Senior Python Developer 8yrs AWS Kubernetes Remote Nairobi Kenya fintech",
    "country": "KE"
  }'
```

**Response:**

```json
{
  "band": "MEDIUM",
  "band_meaning": "At market rate — negotiate on specific skills and experience.",
  "salary_low": 23057,
  "salary_mid": 27692,
  "salary_high": 38898,
  "currency": "USD",
  "confidence": 0.482,
  "country_median": 27692,
  "top_factors": [
    "Seniority: Senior (+85%)",
    "High-value skills: AWS, Kubernetes",
    "Remote work premium",
    "Experience: 8+ years",
    "Country baseline: KE (~$25k median)"
  ],
  "disclaimer": "Statistical estimate only. Based on Stack Overflow Survey 2022–2025 (CC BY-SA 4.0). Excludes equity, bonuses, benefits. Not a legal instrument."
}
```

---

## 🔬 Model — Honest Documentation

### Why Band Classification, Not Exact Salary

AfriSalaries v1 and v2 attempted exact salary regression. Both failed:

| Version | R² | MAPE | Outcome |
|---------|-----|------|---------|
| v1 — XGBoost regressor, TF-IDF 5k | 0.3388 | 92.1% | FAIL |
| v2 — Enhanced features, min_df=1 | 0.3846 | 87.8% | FAIL |
| **v3 — Band classifier + empirical distribution** | **—** | **—** | **✅ Deployed** |

**Root cause analysis of v1/v2 failure (documented, not hidden):**

- Salary range spans $3,000–$200,000 — a 66× range. Within-description variance exceeds between-description variance.
- A Senior Python developer in Kigali earns $18,000. The same role remote earns $120,000. No text model with 1,371 rows bridges a 66× range reliably.
- Predicting the mean ($37k) produced MAPE of 87.8% — the model had learned to guess the average rather than discriminate.

**The pivot:** Band classification reduces the prediction to a tractable question — is this role LOW, MEDIUM, or HIGH relative to local market? Salary bands are also how every HR department in the world thinks. This directly answers the user's negotiation question.

### v3 Architecture

```
Stage 1: XGBoost Band Classifier
  Input:  Job description (text) + country
  Output: LOW / MEDIUM / HIGH salary band
  Method: TF-IDF (3,000 features) + 8 country one-hot
          + 8 numerical features (seniority, years_exp,
            is_remote, hv_skills, country_base,
            desc_len, is_fintech, is_mgmt)

Stage 2: Empirical Salary Distribution
  Input:  Predicted band + country
  Output: P25 / country_median / P75 salary range
  Method: Per-band, per-country medians from
          training data (honest: no per-band regressor
          — negative R² confirmed text cannot
          distinguish within-band salary)
```

### Band Thresholds (Tertile-Based)

| Band | Salary Range (USD/year) | Meaning |
|------|------------------------|---------|
| LOW | < $17,143 | Below market — strong grounds to negotiate upward |
| MEDIUM | $17,143 – $47,872 | At market rate — negotiate on specific factors |
| HIGH | > $47,872 | Above market — evaluate total compensation carefully |

Tertile-based thresholds ensure approximately equal class sizes (506/509/511), preventing class imbalance from biasing the classifier.

### Model Performance

| Metric | Value | Context |
|--------|-------|---------|
| Test Accuracy | 59.5% | vs 33.3% random baseline — 79% relative improvement |
| Test Balanced Accuracy | 59.5% | Balanced across LOW/MEDIUM/HIGH |
| CV Accuracy (5-fold) | 56.2% ± σ | Stratified, honest estimate |
| E2E Band Accuracy | 88.0% | On 150 held-out samples |
| Salary MAPE | 61.7% | Country median within predicted band |
| Salary p50 error | 24.9% | Half of predictions within 25% of true salary |
| Training rows | 1,526 | Real SO Survey data only — zero synthetic rows |

**HIGH band precision = 0.72** — the model is most reliable for premium roles.

**MEDIUM band precision = 0.51** — the hardest band to separate, as expected statistically.

### Feature Engineering

| Feature | Type | Signal |
|---------|------|--------|
| TF-IDF job text | Sparse (3,000) | Role type, technologies, seniority keywords |
| Country one-hot | 8 binary | ZA/NG/KE/GH/ET/TZ/UG/RW |
| Seniority score | Float 0–1 | Intern→Junior→Mid→Senior→Lead |
| Years experience | Float | Regex-extracted from description |
| High-value skill count | Integer | 18 skills: AWS, GCP, PyTorch, Kubernetes... |
| Country baseline | Float | Known USD market anchor per country |
| is_remote | Binary | Remote/hybrid flag |
| is_fintech | Binary | Fintech industry premium signal |
| is_management | Binary | Director/VP/CTO premium |
| Description length | Float | Proxy for role complexity |

**Features excluded by design:** gender (Kenya DPA 2019 / GDPR), age (discrimination laws), company name (too sparse, causes overfitting), exact city (insufficient rows per city).

---

## 📊 Data

### Source

**Stack Overflow Annual Developer Survey 2022–2025**
- Provider: Stack Exchange
- License: **CC BY-SA 4.0** — unrestricted use with attribution
- URL: [survey.stackoverflow.co](https://survey.stackoverflow.co)
- Download: [github.com/StackExchange/Survey](https://github.com/StackExchange/Survey)
- Contains PII: **No** — fully anonymised

### Acquisition

| Year | Global Respondents | African Rows |
|------|-------------------|--------------|
| 2025 | 49,191 | 734 |
| 2024 | 65,437 | 1,062 |
| 2023 | 89,184 | 1,563 |
| 2022 | 73,268 | 1,552 |
| **Total** | **277,080** | **4,911 raw** |

### Cleaning Pipeline: 4,911 → 1,526

| Stage | Rows Remaining | Action |
|-------|---------------|--------|
| Raw | 4,911 | All African respondents |
| Null salary removed | ~2,800 | CompTotal blank = 43% of respondents |
| Currency conversion failures | ~2,400 | Null/unrecognised currency dropped |
| Sanity bounds | ~1,800 | $3,000–$200,000 annual USD |
| Deduplication | 1,675 | Same description + salary = duplicate |
| Country balancing | **1,526** | ZA capped at 3× Nigeria (prevents ZA dominance) |

### Year-Specific Exchange Rates

Nigerian naira devalued ~257% between 2022 and 2025 (NGN 420 → 1,600 per USD). Using a single blended rate would conflate pre- and post-devaluation salaries. Year-specific rates applied for all 4 survey years.

### Country Coverage

| Country | Final Rows | Confidence |
|---------|-----------|------------|
| South Africa (ZA) | 807 | Adequate |
| Nigeria (NG) | 269 | Adequate |
| Kenya (KE) | 225 | Adequate |
| Ghana (GH) | 61 | Elevated uncertainty |
| Ethiopia (ET) | 55 | Elevated uncertainty |
| Uganda (UG) | 48 | Elevated uncertainty |
| Tanzania (TZ) | 33 | Elevated uncertainty |
| Rwanda (RW) | 28 | High uncertainty |

### Salary Distribution (Final Dataset)

| Stat | Value (USD/year) |
|------|-----------------|
| Min | $3,000 |
| 25th percentile | $11,725 |
| Median | $30,378 |
| Mean | $39,131 |
| 75th percentile | $57,487 |
| Max | $200,000 |

---

## ⚠️ Honest Limitations

Intellectual honesty is a prerequisite for credibility.

**L1 — Stack Overflow User Bias**
SO users skew toward experienced, English-speaking, internet-connected developers. Entry-level and peri-urban workers are underrepresented. Model may overestimate for junior roles in less-connected markets.

**L2 — Sparse Country Coverage**
Rwanda (28 rows), Tanzania (33), Uganda (48), Ethiopia (55), Ghana (61) fall below the 100-row threshold for reliable country-specific learning. Confidence scores for these markets carry elevated uncertainty.

**L3 — Self-Reported Salary Bias**
All salary data is self-reported. Well-compensated respondents are more likely to share. Dataset likely carries 5–15% upward bias.

**L4 — Base Salary Only**
Model predicts base salary. A $30,000 role with 5% equity at a Nairobi Series B is economically different from $30,000 at a government parastatal. Equity and bonuses are not captured.

**L5 — Not a Legal Instrument**
AfriSalaries predictions are statistical estimates. They cannot be cited in employment contracts or regulatory filings as authoritative benchmarks.

**L6 — Per-Band Regression Abandoned**
Attempted per-band salary regression produced negative R² values — worse than predicting the band mean. Empirical country-level medians used instead. This is documented as Decision D8 in the project decision log.

---

## 🏗️ System Architecture

```
User (browser or curl)
         │
         ▼
  Vercel CDN → React 18 SPA (web/)
    afrisalaries.vercel.app
         │
         │  POST /predict
         ▼
  FastAPI + Uvicorn on Render (api/)
    afrisalaries.onrender.com
         │
         ├─► Feature Engineering
         │     ├── TF-IDF vectorize (3,000 sparse features)
         │     ├── Country one-hot (8 features)
         │     └── 8 numerical features
         │
         ├─► XGBoost.predict() → band (LOW/MEDIUM/HIGH)
         │
         └─► Empirical lookup → P25/median/P75 salary range
               (country-specific if available, band median fallback)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| ML Model | XGBoost classifier | Sparse + dense features, no GPU, trains in minutes on Colab |
| Text Features | TF-IDF scikit-learn | Lightweight, interpretable, proven for job text |
| API | FastAPI + Pydantic v2 | Async, auto /docs, type-safe schemas |
| Frontend | React 18 + Vite + Tailwind | Zero build cost on Vercel |
| Backend host | Render (free tier) | Docker, auto-redeploy from GitHub |
| Frontend host | Vercel (free tier) | CDN-backed, zero-config for Vite |
| Training | Google Colab (CPU) | Free, no GPU required |

**Total infrastructure cost: $0/month**

---

## 📁 Project Structure

```
afrisalaries/
├── api/
│   ├── main.py           # FastAPI app, lifespan, /predict, /health
│   └── models.py         # Pydantic v2 schemas
├── models/
│   ├── band_classifier.pkl   # XGBoost band classifier
│   ├── vectorizer.pkl        # TF-IDF (3,000 features)
│   ├── band_thresholds.pkl   # Q33/Q67 + salary stats per band
│   ├── country_columns.pkl   # Country one-hot columns
│   ├── numerical_features.pkl
│   └── metrics.json          # Full training metrics
├── data/
│   ├── jobs_so.csv           # 1,526 cleaned SO rows
│   ├── jobs.csv              # description/salary_usd/country
│   └── dataset_stats.json    # Provenance and data statistics
├── web/
│   ├── src/App.jsx           # Predict form + result card
│   ├── src/main.jsx
│   └── index.html
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

```bash
git clone https://github.com/jameskoero/afrisalaries.git
cd afrisalaries
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

API: `http://localhost:8000` · Docs: `http://localhost:8000/docs`

---

## 🚀 Deployment — $0/month

| Service | Purpose | URL |
|---------|---------|-----|
| Render | FastAPI + Docker backend | afrisalaries.onrender.com |
| Vercel | React frontend | afrisalaries.vercel.app |

**Render:** Docker deployment. Auto-redeploys on `git push main`.
**Vercel:** Root Directory = `web`. Framework = Vite. Auto-deploys on push.

> Render free tier sleeps after 15 min idle. First request wakes in ~30s.

---

## 🗺️ Roadmap

### v3.0 — Complete ✅
- [x] Real data pipeline: SO Survey 2022–2025, 1,526 rows, CC BY-SA 4.0
- [x] Year-specific exchange rates (NGN devaluation corrected)
- [x] Band classifier: XGBoost + TF-IDF + 8 numerical features
- [x] Empirical salary distribution per band per country
- [x] FastAPI + Docker + Render deployment
- [x] React 18 + Vite + Tailwind frontend on Vercel
- [x] Full decision log — all architectural pivots documented

### v3.x — Next
- [ ] Real job board data: BrighterMonday + Fuzu scraper (target 5,000+ rows)
- [ ] Return to salary regression once data > 3,000 rows per country
- [ ] Neon PostgreSQL: prediction history + feedback loop
- [ ] SHAP explainability restored once regression is viable

### v4.x — Planned
- [ ] Browser extension: auto-predict on any African job board
- [ ] Weekly retraining from accumulated feedback
- [ ] Expand to 16 African countries
- [ ] Peer-reviewed publication on African tech salary transparency

---

## 👨‍💻 Author

<div align="center">

**James Onyango Koero**
*ML Engineer · Kisumu, Kenya 🇰🇪*

B.Sc. Physics & Mathematics — Moi University (2012)
Self-taught ML Engineer since 2023

[![LinkedIn](https://img.shields.io/badge/LinkedIn-James_Koero-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/james-koero)
[![GitHub](https://img.shields.io/badge/GitHub-jameskoero-181717?style=for-the-badge&logo=github)](https://github.com/jameskoero)
[![Email](https://img.shields.io/badge/Email-jmskoero%40gmail.com-D14836?style=for-the-badge&logo=gmail)](mailto:jmskoero@gmail.com)

**What this project demonstrates:**

| Skill | Evidence |
|-------|---------|
| End-to-end ML pipeline | Stages 1–10: acquisition → cleaning → training → deployment |
| Scientific honesty | Two failed models documented and diagnosed before pivot |
| Real data engineering | 4,911 raw rows → 1,526 clean, year-specific FX rates |
| Production deployment | Docker + Render + Vercel, $0/month |
| Research methodology | Decision log, limitation disclosures, no inflated metrics |
| Mobile-first engineering | Built entirely on Android (Termux + Colab) |

> Open to remote ML / data science roles globally.
> This project is my working proof of end-to-end ML thinking —
> including the failures that led to the right architecture.

</div>

---

## 📄 Data License

Training data sourced from Stack Overflow Annual Developer Survey 2022–2025,
licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
© Stack Exchange Inc. Attribution maintained throughout.

---

<div align="center">

⭐ **Star this repo** if you believe African tech workers deserve pay transparency.

*Built with intellectual honesty in Kisumu, Kenya.*
*For the millions of African tech workers who deserve to know what their skills are worth.*

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>
