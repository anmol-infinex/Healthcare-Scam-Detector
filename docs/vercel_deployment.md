# Vercel Deployment

This repository is configured for one-click Vercel deployment.

## Runtime Architecture

- `public/`: source frontend files.
- `scripts/build.mjs`: copies `public/` to `dist/`.
- `dist/`: Vercel static output directory generated during build.
- `api/index.py`: Flask-based Python Vercel Function.
- `models/healthcare_scam_detector.joblib`: trained scikit-learn model loaded by the API.

## Vercel Settings

Vercel can import the GitHub repository with these settings from `vercel.json`:

- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`
- API Route: `/api/predict`

No manual dashboard changes are required.
