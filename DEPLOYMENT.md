# MAG (Monetization Audit Generator) Deployment Guide

## Prerequisites
1. A GitHub account
2. A Streamlit Cloud account (free)
3. NVIDIA API keys (NVIDIA_API_KEY and NVIDIA_API_KEY2)

## Deployment Steps

1. **Push your code to GitHub**
   - Create a new repository on GitHub
   - Push your local code to this repository

2. **Connect to Streamlit Cloud**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account
   - Click "New app" and select your repository

3. **Configure the app**
   - Set the main file to `app.py`
   - Add the following secrets in the Streamlit Cloud settings:
     - `password`: Your chosen password for the app (e.g., "yourpassword")
     - `NVIDIA_API_KEY`: Your NVIDIA API key
     - `NVIDIA_API_KEY2`: Your NVIDIA API key

4. **Deploy**
   - Click "Deploy" to build and deploy your app

## Accessing the app
Once deployed, your app will be accessible at a URL like:
`https://your-app-name.streamlit.app`

Note: The app will prompt for a password when accessed. Use the password you set in the secrets.