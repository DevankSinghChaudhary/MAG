# **MAG** (Monetisation Audit Generator)

This is monetisation audit generator, works via "NVIDIA_API" (can work with any ai api). Generate audit based on creator's bio, captions.

[![Instagram](https://img.shields.io/badge/Owner-Follow-00000?logo=instagram&logoColor=white)](https://instagram.com/devanksinghchaudhary)

# 🔍 MAG (v1.1)

## Features
- Accept bio and captions as input
- Fully free
- Generates PDF reports in organized output directory
- More features coming...

## Potential Issues
- ### AI API
    - ### Fix
        - > Go to: www.build.nvidia.com/
        - > Make nvidia account
        - > Generate Own API key for free, no limit except 40 requests/min (more than enough for single user)

## Output Directory
All generated PDFs are now saved in the `/output/` directory for better organization.

## Tech Stack
- Python

# **Installation**

## 1. Clone the repo
```bash
git clone https://github.com/devanksinghchaudhary/mag.git
cd mag
```

## 2. Create virtual environment (python/optional)
```bash
python -m venv env
```

## 3. Activate virtual environment
### Windows(PowerShell):
```bash
env\Scripts\activate
```

### Mac/Linux
```bash
source env/bin/activate
```
## 3. Install the dependencies
```bash
pip install -r requirements.txt
```