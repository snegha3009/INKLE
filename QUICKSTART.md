# 🚀 QUICK START GUIDE

## Get Running in 5 Minutes!

### Step 1: Install Dependencies (2 minutes)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Get OpenAI API Key (2 minutes)
1. Visit: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy it (starts with sk-...)

### Step 3: Configure Environment (30 seconds)
```bash
# Copy template
cp .env.example .env

# Edit .env and add your key:
# OPENAI_API_KEY=sk-your-key-here
```

### Step 4: Run! (30 seconds)
```bash
# Option A: Command-line testing
python main.py test

# Option B: Web dashboard
python app.py
# Then visit: http://localhost:5000
```

## That's It! 🎉

Your multi-agent tourism system is now running!

## Need Help?
- Read README.md for full documentation
- Check SETUP_GUIDE.md for detailed instructions
- See dashboard-guide.md for web interface help

## Test Queries
Try these in the dashboard or command line:
- "I'm going to Bangalore, let's plan my trip"
- "What's the weather in Paris?"
- "Tell me about Tokyo weather and places to visit"
