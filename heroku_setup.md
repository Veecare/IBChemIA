# Deploying to Heroku: Step-by-Step Guide

## Prerequisites
1. Create a [Heroku account](https://signup.heroku.com/) if you don't have one
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Download your project files from Replit

## Deployment Steps

### 1. Set Up Local Repository
```bash
# Create a folder for your project
mkdir ib-chemistry-ia-planner
cd ib-chemistry-ia-planner

# Copy all your files from Replit to this folder
# Include app.py, pages/, utils/, .streamlit/, Procfile, and runtime.txt
```

### 2. Create requirements.txt file
Create a file named `requirements.txt` with the following content:
```
streamlit==1.31.0
matplotlib==3.7.1
numpy==1.24.3
pandas==2.0.1
plotly==5.15.0
scikit-learn==1.2.2
scipy==1.10.1
statsmodels==0.14.0
sympy==1.12.0
fpdf==1.7.2
```

### 3. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

### 4. Create and Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create ib-chemistry-ia-planner

# Push your code to Heroku
git push heroku main

# Open your app
heroku open
```

### 5. Troubleshooting
If you encounter issues:
```bash
# View logs
heroku logs --tail

# Restart the app
heroku restart
```

## Important Notes
- Your app will be available at `https://ib-chemistry-ia-planner.herokuapp.com` (or similar URL assigned by Heroku)
- The free tier of Heroku has limitations:
  - Apps "sleep" after 30 minutes of inactivity
  - Limited to 550-1000 dyno hours per month
- Consider upgrading to a paid plan for more reliable service

## Maintenance
To update your app after making changes:
```bash
git add .
git commit -m "Update description"
git push heroku main
```