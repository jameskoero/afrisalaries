<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=AfriSalaries%20🌍&fontSize=62&fontColor=fff&animation=fadeIn&fontAlignY=38&desc=ML-Powered%20Salary%20Intelligence%20for%20African%20Tech%20Jobs&descAlignY=60&descAlign=50" width="100%"/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-337AB7?style=for-the-badge)](https://xgboost.readthedocs.io)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-FF6B6B?style=for-the-badge)](https://shap.readthedocs.io)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/jameskoero/afrisalaries/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Countries](https://img.shields.io/badge/Countries-8_African-FF5722?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Active_Development-00C853?style=for-the-badge)]()

<br/>

[📖 API Docs](https://afrisalaries-api.onrender.com/docs) · [🌐 Web App](https://afrisalaries.vercel.app) · [💻 GitHub](https://github.com/jameskoero/afrisalaries) · [🐛 Report Bug](https://github.com/jameskoero/afrisalaries/issues)

<br/>

> **"70%+ of African tech job posts hide salary information.**
> AfriSalaries predicts it — with an explainable breakdown of every factor
> that drove the number. Built for African talent. Trusted by global HR teams."

</div>

---

## ❗ The Problem

African tech is one of the fastest-growing talent markets on the planet — yet it remains one of the most opaque when it comes to compensation.

**Over 70% of tech job posts in Africa include no salary information.**

- A junior engineer in Nairobi accepts KES 80,000/month not knowing the market rate is KES 140,000
- An HR team in Amsterdam sets pay for a Nairobi remote hire with no local data and gets it wrong
- A startup in Lagos loses candidates to a competitor that was simply transparent about pay
- A diaspora professional returning to Accra cannot benchmark what they should ask for

The information asymmetry is structural. Companies have salary bands. Candidates have nothing. AfriSalaries fixes that.

---

## 💡 The Solution

AfriSalaries takes any tech job description as plain text and returns:

1. **A salary range** — low / mid / high in USD or local currency
2. **A confidence score** — how certain the model is per prediction
3. **An explainable breakdown** — which keywords drove the estimate (SHAP values)

No account. No form. Paste the job description. Get the number. Understand why.

```bash
curl -X POST https://afrisalaries-api.onrender.com/predict/ \
  -H "Content-Type: application/json" \
  -d '{"description": "Senior Python Developer 5yrs Django AWS Remote Nairobi Kenya fintech startup", "country": "KE", "currency": "USD"}'
```

**Response:**

```json
{
  "salary_low": 29750,
  "salary_mid": 35000,
  "salary_high": 40250,
  "currency": "USD",
  "confidence": 0.81,
  "top_factors": [
    {"name": "Senior", "value": 0.22},
    {"name": "Python", "value": 0.15},
    {"name": "AWS",    "value": 0.12},
    {"name": "Remote", "value": 0.09}
  ],
  "model_version": "xgboost_v1.0.0"
}
```

---

## 👥 Who This Is For

| Audience | Use Case |
|----------|----------|
| 🌍 African tech workers | Benchmark an offer before replying. Know if the number is fair. |
| 🌐 International HR teams | Set fair pay for African remote hires without guessing |
| 🏢 Hiring managers outside Africa | Understand local market rates before posting a role |
| 📊 Talent acquisition teams | Compare salaries across 8 African countries in one API call |
| 🏦 Investors and researchers | Access anonymized community salary data via the /jobs feed |

---

## ✅ What Is Built

Every item marked ✅ exists in the codebase and is deployable today.

| Component | Status | Detail |
|-----------|--------|--------|
| POST /predict/ | ✅ Built | Job text → salary range + SHAP factors |
| GET /jobs/ public feed | ✅ Built | Recent predictions filterable by country |
| GET /health | ✅ Built | Model load status + API liveness |
| POST /predict/feedback | ✅ Built | User corrections for future retraining |
| XGBoost regression model | ✅ Built | Trains on data/jobs.csv → models/model.pkl |
| TF-IDF text vectorizer | ✅ Built | 5,000 features unigrams + bigrams sublinear TF |
| SHAP TreeExplainer | ✅ Built | Top-5 salary factors per prediction |
| 13 handcrafted features | ✅ Built | Seniority remote skills years country |
| Mock predictor fallback | ✅ Built | API works before model is trained |
| Neon PostgreSQL async | ✅ Built | SQLAlchemy 2.0 async |
| Upstash Redis cache | ✅ Built | 24h TTL via REST API |
| React 18 + Recharts UI | ✅ Built | SHAP bar chart salary card |
| GitHub Actions CI | ✅ Built | pytest on every push to main |
| Render deployment | ✅ Built | render.yaml no Docker needed |
| Vercel frontend | ✅ Built | web/ folder auto-deploys |
| Real scraped data | 🔄 In progress | Target 3,000+ rows BrighterMonday + Fuzu |
| Currency conversion | 📋 Planned | USD KES NGN ZAR GHS live rates |
| Browser extension | 📋 Planned | Auto-predict on LinkedIn job pages |

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| ML Model | XGBoost gradient boosting | Sparse + dense features no GPU trains in minutes |
| Text Features | TF-IDF scikit-learn | Interpretable lightweight proven for job text |
| Explainability | SHAP TreeExplainer | Shows recruiters exactly why the number is what it is |
| API | FastAPI + Pydantic v2 + Uvicorn | Async auto /docs type-safe schemas |
| Database | Neon PostgreSQL + SQLAlchemy 2.0 | Serverless zero idle cost no expiry |
| Cache | Upstash Redis REST API | HTTP Redis no TCP socket works on Render free tier |
| Frontend | React 18 + Vite + Tailwind + Recharts | Builds in Vercel cloud no local build needed |
| CI/CD | GitHub Actions | pytest on push Render and Vercel auto-deploy from main |
| Backend host | Render | Direct Python from GitHub no Docker required |
| Frontend host | Vercel | CDN-backed zero-config for Vite |

**Total infrastructure cost: $0 per month**

---

## 🏗️ System Architecture

```
User (browser or API client)
         │
         ▼
  Vercel CDN → React SPA (web/)
         │
         │  POST /predict/
         ▼
  FastAPI on Render (api/)
         │
         ├─► 1. SHA-256 hash → check Upstash Redis
         │          └── Cache HIT → return instantly under 5ms
         │
         ├─► 2. Cache MISS → Feature Engineering
         │          ├── TF-IDF vectorize → 5,000 sparse features
         │          └── 13 handcrafted features:
         │                seniority_score · years_experience
         │                high_value_skill_count · is_remote
         │                description_length · country one-hot
         │
         ├─► 3. XGBoost.predict() → salary_mid
         │       └── SHAP.TreeExplainer() → top_factors
         │
         ├─► 4. Neon PostgreSQL → persist job + prediction
         │
         └─► 5. Upstash Redis → cache 24 hours

GET /jobs/?country=KE → community salary benchmark feed
```

**Design principles:**
- Stateless API — Render can restart freely with no session loss
- Cache-first — the same job description posted 1,000 times hits the model once
- Graceful degradation — mock predictor means zero 500 errors before training
- Async throughout — handles concurrency on 512MB free-tier RAM

---

## 🔬 How the ML Model Works

Job descriptions are structured text with high-signal keywords. TF-IDF captures which words are distinctive — "Senior", "Machine Learning", "Kubernetes" score high because they identify premium roles. XGBoost learns nonlinear relationships between those term weights and annual salary.

Chosen over neural embeddings: no GPU needed, SHAP-compatible, trains in 10 minutes on Colab CPU.

### Feature Pipeline

```
Raw job description
  → clean: strip HTML · lowercase · normalize punctuation
  → TF-IDF: 5,000 features · ngram(1,2) · sublinear_tf=True
  → 13 handcrafted features:
      seniority_score    junior(-0.15) mid(0.0) senior(+0.25) lead(+0.30)
      years_experience   regex: "5+ years", "3-5 years"
      high_value_skills  count: PyTorch, AWS, Kubernetes, Go...
      is_remote          keyword: remote, hybrid, WFH
      description_length word count
      country_KE...RW    one-hot encoding (8 features)
  → X = hstack([X_tfidf, X_handcrafted])   shape: (n_samples, 5013)
  → XGBRegressor(n_estimators=500, max_depth=6, learning_rate=0.05)
  → SHAP TreeExplainer → top_factors
```

### What Recruiters See

```
Why this salary estimate?

Senior Level   ████████████████████  +$7,700
Python         ████████████████      +$5,250
AWS            ████████████          +$4,200
Remote         ████████              +$3,150
Nairobi        ██████                +$2,450
```

### Model Performance — Honest Status

> ⚠️ Model currently trains on 600-row synthetic bootstrap data.
> Real metrics will be published once BrighterMonday and Fuzu data is collected (target: 3,000+ rows).

| Metric | Target on Real Data |
|--------|---------------------|
| R² | ≥ 0.70 |
| MAE | < $5,500 USD/year |
| MAPE | < 22% |
| Minimum training rows | 3,000+ real posts |

Real data sources being collected: BrighterMonday Kenya · Fuzu East Africa · Jobberman Nigeria · Careers24 South Africa

---

## 📡 API Reference

**Base URL:** `https://afrisalaries-api.onrender.com`

> Render free tier sleeps after 15 min inactivity. First request wakes it in ~30s.
> Add a free [UptimeRobot](https://uptimerobot.com) monitor on `/health` every 5 min to keep it awake.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /predict/ | Predict salary from job description text |
| GET | /jobs/ | Public predictions feed |
| GET | /jobs/{id} | Single prediction detail |
| GET | /health | API and model load status |
| POST | /predict/feedback | Submit salary correction |

**Supported countries:** KE · NG · ZA · GH · ET · TZ · UG · RW

**Supported currencies:** USD · KES · NGN · ZAR

**Interactive Swagger UI:** https://afrisalaries-api.onrender.com/docs

---

## 📁 Project Structure

```
afrisalaries/
├── .github/workflows/ci.yml       # pytest on every push to main
├── api/
│   ├── main.py                    # FastAPI app + lifespan
│   ├── models.py                  # Pydantic v2 schemas
│   ├── core/config.py             # Settings from .env
│   ├── core/database.py           # Async SQLAlchemy + Neon
│   ├── core/cache.py              # Upstash Redis REST client
│   ├── ml/predictor.py            # XGBoost + SHAP + Redis cache
│   ├── ml/features.py             # Text cleaning + 13 features
│   ├── routes/predict.py          # POST /predict/
│   ├── routes/jobs.py             # GET /jobs/
│   ├── routes/health.py           # GET /health
│   └── db/crud.py                 # Async DB queries
├── ml/
│   ├── train.py                   # XGBoost training pipeline
│   └── generate_sample_data.py    # 600-row bootstrap dataset
├── web/
│   ├── src/App.jsx                # Predict form + country selector
│   ├── src/components/SalaryCard.jsx  # SHAP bar chart
│   └── src/lib/api.js             # Axios client to FastAPI
├── tests/test_api.py              # 5 pytest tests
├── render.yaml                    # Render deployment config
├── requirements.txt               # Pinned Python dependencies
└── .env.example                   # Environment variable template
```

---

## ⚡ Quick Start

```bash
git clone https://github.com/jameskoero/afrisalaries.git
cd afrisalaries
pip install -r requirements.txt
cp .env.example .env
uvicorn api.main:app --reload --port 8000
```

API: `http://localhost:8000` · Docs: `http://localhost:8000/docs`

```env
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/afrisalaries?sslmode=require
UPSTASH_REDIS_REST_URL=https://your-db.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here
APP_ENV=production
FRONTEND_URL=https://afrisalaries.vercel.app
MODEL_VERSION=xgboost_v1.0.0
```

---

## 🏋️ Training in Google Colab

Training runs on free Colab CPU — no local compute needed.

```python
!git clone https://github.com/jameskoero/afrisalaries.git
%cd afrisalaries
!pip install -r requirements.txt -q
!python ml/generate_sample_data.py
!python ml/train.py
import json; print(json.load(open("models/metrics.json")))
```

Commit the trained model so Render deploys it:

```bash
git add models/model.pkl models/vectorizer.pkl models/metrics.json
git commit -m "feat: trained XGBoost v1.0.0"
git push origin main
# Render auto-redeploys → /health returns model_loaded: true
```

---

## 🚀 Deployment — $0 Per Month

| Service | Purpose | Sign Up |
|---------|---------|---------|
| Neon | PostgreSQL database | neon.tech |
| Upstash | Redis cache | upstash.com |
| Render | FastAPI backend | render.com |
| Vercel | React frontend | vercel.com |

**Render settings:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- Region: Frankfurt (closest to Kenya)

**Vercel settings:**
- Root Directory: `web` ← critical, build fails without this
- Environment Variable: `VITE_API_URL=https://afrisalaries-api.onrender.com`

Every `git push origin main` auto-redeploys both services.

---

## 🗺️ Roadmap

### v1.0 — Complete ✅
- [x] FastAPI + XGBoost + TF-IDF + SHAP + Redis + PostgreSQL
- [x] React 18 frontend with SHAP salary bar chart
- [x] Mock predictor fallback + feedback endpoint
- [x] GitHub Actions CI + Render + Vercel pipeline
- [x] 8 countries: KE · NG · ZA · GH · ET · TZ · UG · RW

### v1.x — In Progress
- [ ] Real training data: BrighterMonday + Fuzu scraper (3,000+ rows)
- [ ] Publish real model metrics once trained on real data
- [ ] Currency conversion: live USD ↔ KES ↔ NGN ↔ ZAR ↔ GHS

### v2.x — Planned
- [ ] Browser extension: auto-predict on any job board page
- [ ] Weekly model retraining from accumulated feedback data
- [ ] Company-level salary models for top 20 African tech employers

---

## 🤝 Contributing

Best contribution: real anonymized salary data.

```csv
description,salary_usd,country
"Senior Python Dev 5yrs Django AWS remote Nairobi fintech",42000,KE
"Data Analyst SQL Power BI 3yrs Lagos Nigeria banking",24000,NG
"ML Engineer PyTorch computer vision Cape Town South Africa",58000,ZA
```

Fields: `description` (no personal names) · `salary_usd` (annual USD) · `country` (ISO 2-letter)

[Open an issue](https://github.com/jameskoero/afrisalaries/issues) — all records anonymized before training.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 👨‍💻 Author

<div align="center">

**James Onyango Koero**
*Junior ML Engineer · Kisumu, Kenya 🇰🇪*

B.Sc. Physics — Moi University (2012) · Self-taught ML Engineer since 2023

[![LinkedIn](https://img.shields.io/badge/LinkedIn-James_Koero-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/james-koero)
[![GitHub](https://img.shields.io/badge/GitHub-jameskoero-181717?style=for-the-badge&logo=github)](https://github.com/jameskoero)
[![Email](https://img.shields.io/badge/Email-jmskoero%40gmail.com-D14836?style=for-the-badge&logo=gmail)](mailto:jmskoero@gmail.com)
[![CMDMS Live](https://img.shields.io/badge/Live_App-cmdms.onrender.com-46E3B7?style=for-the-badge&logo=render)](https://cmdms.onrender.com)

**What this project demonstrates for technical hiring managers:**

| Skill | Where to See It |
|-------|----------------|
| End-to-end ML system design | Architecture diagram above |
| NLP feature engineering | api/ml/features.py |
| XGBoost regression pipeline | ml/train.py |
| SHAP explainability | api/ml/predictor.py |
| Async FastAPI + Pydantic v2 | api/main.py · api/routes/ |
| Production async PostgreSQL | api/core/database.py |
| Redis caching strategy | api/core/cache.py |
| React data visualization | web/src/components/SalaryCard.jsx |
| CI/CD + cloud deployment | .github/workflows/ci.yml · render.yaml |

> Open to remote ML / data science roles globally.
> This project is my working proof of production ML thinking.

**Repo:** [github.com/jameskoero/afrisalaries](https://github.com/jameskoero/afrisalaries)

</div>

---

<div align="center">

⭐ **Star this repo** if you believe African tech workers deserve pay transparency.

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>
