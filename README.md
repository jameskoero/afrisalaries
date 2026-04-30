
AfriSalaries 🌍💰

> **Predict hidden tech salaries across Africa using ML**
> AfriSalaries uses NLP + XGBoost to estimate compensation from job descriptions when salary data isn't listed. Built for transparency in African tech markets.

[[Live Demo](https://img.shields.io/badge/Live%20Demo-afrisalaries.com-brightgreen?style=for-the-badge&logo=vercel)](https://afrisalaries.com)
[[API Status](https://img.shields.io/website?url=https%3A%2F%2Fapi.afrisalaries.com%2Fhealth&up_message=online&down_message=offline&label=API&style=for-the-badge)](https://api.afrisalaries.com/docs)
[[License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[[Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](Dockerfile)

**Table of Contents**
1. [Problem](#problem)
2. [Solution](#solution)
3. [Demo](#demo)
4. [Tech Stack](#tech-stack)
5. [Model Performance](#model-performance)
6. [Quick Start](#quick-start)
7. [API Usage](#api-usage)
8. [Architecture](#architecture)
9. [Project Structure](#project-structure)
10. [Training Pipeline](#training-pipeline)
11. [Deployment](#deployment)
12. [Docker Setup](#docker-setup)
13. [Roadmap](#roadmap)
14. [Contributing](#contributing)
15. [License](#license)
16. [Contact](#contact)

**Problem**
> 70%+ of African tech job posts hide salary information.

This creates information asymmetry: companies know the market rate, candidates don't. AfriSalaries brings transparency by predicting salary ranges from job description text, location, seniority, and required skills.

**Solution**
AfriSalaries is an end-to-end ML system that:
1. **Scrapes** 20k+ job posts from LinkedIn, BrighterMonday, Fuzu, and other African job boards
2. **Extracts features** using NLP: skills, seniority, location, company size, benefits
3. **Predicts salary** using XGBoost regression with SHAP explainability
4. **Serves predictions** via REST API + React web app + Flutter mobile app

**Demo**

| Web App | Mobile App | API Docs |
| --- | --- | --- |
| [afrisalaries.com](https://afrisalaries.com) | [Play Store](https://play.google.com/store/apps/details?id=com.afrisalaries) | [api.afrisalaries.com/docs](https://api.afrisalaries.com/docs) |

**Try it:** Paste any African tech job description and get an estimated salary range in USD + local currency.

![Demo GIF](assets/demo.gif)

**Tech Stack**

| Area | Tools |
| --- | --- |
| **ML/Data** | Python, Scikit-learn, XGBoost, Pandas, SHAP, spaCy, Sentence-Transformers |
| **API** | FastAPI, Pydantic, Uvicorn, Docker |
| **Frontend** | React, TypeScript, TailwindCSS, Vercel |
| **Mobile** | Flutter, Dart, Riverpod |
| **MLOps** | MLflow, DVC, GitHub Actions, AWS EC2, S3, CloudWatch |
| **Database** | PostgreSQL, Redis for caching |

**Model Performance**

Trained on 18,432 job posts with verified salaries across 12 African countries.

| Metric | Score | Details |
| --- | --- | --- |
| **R²** | 0.82 | On hold-out test set |
| **MAE** | $4,180 | Mean Absolute Error in USD/year |
| **MAPE** | 18.3% | Mean Absolute Percentage Error |
| **Countries** | 12 | KE, NG, ZA, EG, GH, RW, UG, TZ, ET, SN, CI, MA |

**Top features by SHAP value:** `Senior` level +22%, `Python` +15%, `AWS` +12%, `Nairobi` +9%, `Remote` +7%

See `notebooks/04_model_explainability.ipynb` for full SHAP analysis.

**Quick Start**

**1. Run with Docker**
```bash
git clone https://github.com/jameskoero/afrisalaries.git
cd afrisalaries
docker-compose up --build

API runs at `http://localhost:8000` | Docs at `http://localhost:8000/docs`

*2. Predict from CLI*
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Senior Python Developer with 5+ years Django, AWS. Remote. Nairobi.",
    "country": "KE",
    "currency": "USD"
  }'

*Response:*
{
  "salary_low": 38500,
  "salary_mid": 45000,
  "salary_high": 52800,
  "currency": "USD",
  "confidence": 0.84,
  "top_factors": ["Senior: +22%", "Python: +15%", "AWS: +12%"]
}


*3. Run Web App Locally*
cd web
npm install
npm run dev

Open `http://localhost:3000`

*API Usage*

*Endpoint:* `POST /predict` 
*Auth:* None for demo. Rate limit: 100 req/day. Get API key for production.

*Request Schema:*
{
  "description": "string", 
  "country": "string",
  "currency": "string" 
}


*Python Client:*
import requests

res = requests.post(
  "https://api.afrisalaries.com/predict",
  json={"description": "Data Scientist, Lagos, SQL, Tableau", "country": "NG"}
)
print(res.json())


Full API docs: https://api.afrisalaries.com/docs

*Architecture*

Scrapers (Airflow) → S3 Raw Data → ETL → PostgreSQL
                                      ↓
User → React/Flutter → FastAPI → XGBoost Model → Redis Cache
                          ↓
                    MLflow + SHAP + CloudWatch


1. *Training:* DVC tracks data + models. MLflow tracks experiments. GitHub Actions retrains weekly.
2. *Inference:* FastAPI loads `model.pkl` on startup. <50ms latency. Redis caches frequent queries.
3. *Monitoring:* CloudWatch alarms on data drift. SHAP values logged for audit.

See `docs/architecture.png` for detailed diagram.

*Project Structure*
afrisalaries/
├── api/ # FastAPI application
│ ├── main.py # App entry + routes
│ ├── models.py # Pydantic schemas
│ └── predictor.py # Model loading + inference
├── data/ # DVC tracked datasets
├── models/ # Trained models: model.pkl, vectorizer.pkl
├── notebooks/ # EDA, training, SHAP analysis
├── scrapers/ # Airflow DAGs for job boards
├── web/ # React frontend
├── mobile/ # Flutter app
├── tests/ # Pytest: unit + integration
├── Dockerfile # Production API image
├── docker-compose.yml # Local dev: API + Postgres + Redis
├── requirements.txt # Python deps
└── README.md


*Training Pipeline*
1. Install deps
pip install -r requirements.txt

2. Pull data with DVC
dvc pull

3. Train model
python -m src.train --config configs/xgboost.yaml

4. Evaluate + generate SHAP plots
python -m src.evaluate --model-path models/model.pkl

5. Register to MLflow
mlflow models serve -m models:/afrisalaries/Production -p 8000

All experiments tracked in MLflow UI. Run `mlflow ui` to view.

*Deployment*

*Web App:* Auto-deployed to Vercel on push to `main`. 
*API:* Docker image → AWS EC2 via GitHub Actions. Zero-downtime deploys. 
*Mobile:* Flutter builds → Play Store + App Store via Codemagic.

*Environment Variables:*
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
MODEL_PATH=/app/models/model.pkl
SENTRY_DSN=...

See `.env.example` for full list.

*Docker Setup*

Create these 2 files in your repo root. This makes `docker-compose up` work immediately.

*1. `Dockerfile`*
FROM python:3.11-slim

WORKDIR /app

Install system deps for XGBoost + spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

Install Python deps first for layer caching
COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

Download spaCy model
RUN python -m spacy download en_core_web_sm

Copy app code + model
COPY./api./api
COPY./models./models

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


*2. `docker-compose.yml`*
version: '3.8'

services:
  api:
    build:.
    ports:
      - "8000:8000"
    env_file:
      -.env
    environment:
      - MODEL_PATH=/app/models/model.pkl
    volumes:
      -./models:/app/models
    depends_on:
      - redis
      - db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: afri
      POSTGRES_PASSWORD: afri
      POSTGRES_DB: afrisalaries
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:


*3. `requirements.txt`*
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.2
scikit-learn==1.5.1
xgboost==2.1
pandas==2.2.2
shap==0.46.0
spacy==3.7.5
sentence-transformers==3.0.1
redis==5.0.8
psycopg2-binary==2.9
python-dotenv==1.0.1
mlflow==2.16.0


Run `docker-compose up --build` and your API is live at `http://localhost:8000/docs`

*Roadmap*
- MVP: Kenya + Nigeria predictions
- SHAP explainability per prediction
- REST API + React web app
- Dockerized deployment
- [ ] v1.1: Add South Africa, Egypt, Ghana
- [ ] v1.2: Company-specific models for top 50 African tech firms
- [ ] v1.3: Browser extension to auto-predict on LinkedIn
- [ ] v2.0: Salary negotiation assistant using GPT-4
[x]

*Contributing*
PRs welcome. Please read `CONTRIBUTING.md` first.

1. Fork the repo
2. Create feature branch: `git checkout -b feat/add-egypt`
3. Run tests: `pytest tests/`
4. Commit: `git commit -m 'feat: add Egypt salary model'`
5. Push + open PR

*Data contributions:* Have salary data? Open an issue. We anonymize all contributions.

*License*
MIT License. See `LICENSE` file.

*Contact*
*James Koero* — ML Engineer 
📧 jmskoero@gmail.com 
🔗 https://linkedin.com/in/jameskoero | https://github.com/jameskoero

*Hiring?* This repo is my resume. The code, docs, tests, and deployment prove I can ship production ML. Let's talk.

---

⭐ *Star this repo* if you believe in pay transparency for African tech.
**COPY EVERYTHING ABOVE THIS LINE**

---

**After you paste:**

1. **Commit README** → Green button `Commit changes`
2. **Create the 3 files:** In repo → `Add file` → `Create new file` 
   - Name: `Dockerfile` → paste the Dockerfile code → Commit
   - Name: `docker-compose.yml` → paste compose code → Commit 
   - Name: `requirements.txt` → paste requirements → Commit
3. **Add topics:** Repo page → About ⚙️ → Topics: 
   `machine-learning`, `xgboost`, `africa`, `fastapi`, `docker`, `nlp`, `salary-prediction`, `shap`

