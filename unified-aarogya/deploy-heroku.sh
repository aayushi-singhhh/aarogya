#!/bin/bash

# Aarogya Heroku Deployment Script
echo "🚀 Deploying Aarogya to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "npm install -g heroku"
    exit 1
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Deploy Backend
echo "📦 Deploying Backend..."
cd backend

# Create Procfile if it doesn't exist
if [ ! -f "Procfile" ]; then
    echo "web: gunicorn app:app" > Procfile
    echo "✅ Created Procfile"
fi

# Add gunicorn to requirements if not present
if ! grep -q "gunicorn" requirements.txt; then
    echo "gunicorn==21.2.0" >> requirements.txt
    echo "✅ Added gunicorn to requirements.txt"
fi

# Create Heroku app for backend
APP_NAME_BACKEND="aarogya-backend-$(date +%s)"
heroku create $APP_NAME_BACKEND
heroku buildpacks:set heroku/python -a $APP_NAME_BACKEND

# Set environment variables
heroku config:set FLASK_ENV=production -a $APP_NAME_BACKEND
heroku config:set SECRET_KEY=$(openssl rand -base64 32) -a $APP_NAME_BACKEND

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial backend commit"
fi

# Add Heroku remote and deploy
heroku git:remote -a $APP_NAME_BACKEND
git push heroku main

BACKEND_URL=$(heroku info -a $APP_NAME_BACKEND | grep "Web URL" | awk '{print $3}')
echo "✅ Backend deployed to: $BACKEND_URL"

cd ../frontend

# Deploy Frontend
echo "📦 Deploying Frontend..."

# Update API URL in frontend
if [ -f "src/api/index.js" ]; then
    sed -i.bak "s|http://localhost:5001|$BACKEND_URL|g" src/api/index.js
    echo "✅ Updated API URL to: $BACKEND_URL"
fi

# Create Heroku app for frontend
APP_NAME_FRONTEND="aarogya-frontend-$(date +%s)"
heroku create $APP_NAME_FRONTEND
heroku buildpacks:set heroku/nodejs -a $APP_NAME_FRONTEND

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial frontend commit"
fi

# Add Heroku remote and deploy
heroku git:remote -a $APP_NAME_FRONTEND
git push heroku main

FRONTEND_URL=$(heroku info -a $APP_NAME_FRONTEND | grep "Web URL" | awk '{print $3}')
echo "✅ Frontend deployed to: $FRONTEND_URL"

echo ""
echo "🎉 Deployment Complete!"
echo "📱 Frontend: $FRONTEND_URL"
echo "🔧 Backend: $BACKEND_URL"
echo ""
echo "Next steps:"
echo "1. Update CORS settings in backend to allow frontend domain"
echo "2. Set up custom domains if needed"
echo "3. Configure environment variables for production"
