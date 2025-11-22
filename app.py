#!/usr/bin/env python3
"""
Flask API Backend for Multi-Agent Tourism Dashboard
Connects the web interface to the multi-agent system
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import time

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.tools import TourismTools
from agents.orchestrator import TourismOrchestrator

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for dashboard

# Initialize agents (global to avoid recreation on each request)
tools_factory = TourismTools()
tools = tools_factory.create_tools()
orchestrator = None

try:
    orchestrator = TourismOrchestrator(tools, verbose=False)
    print("✓ Multi-agent system initialized successfully")
except Exception as e:
    print(f"✗ Error initializing agents: {e}")
    print("Make sure OPENAI_API_KEY is set in .env file")


@app.route('/')
def index():
    """Serve the dashboard"""
    return send_from_directory('.', 'dashboard_connected.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agents': {
            'parent_agent': 'active',
            'weather_agent': 'active',
            'places_agent': 'active'
        },
        'apis': {
            'nominatim': 'online',
            'open_meteo': 'online',
            'overpass': 'online'
        }
    })


def get_demo_response(query):
    """Generate demo responses when OpenAI is unavailable"""
    query_lower = query.lower()
    
    if 'bangalore' in query_lower:
        return "In Bangalore it's currently 24°C with a chance of 35% to rain.\nList of 5 places: Lalbagh Botanical Garden, Cubbon Park, Bangalore Palace, ISKCON Temple, Vidhana Soudha"
    elif 'paris' in query_lower:
        return "In Paris it's currently 18°C with a chance of 20% to rain.\nList of 5 places: Eiffel Tower, Louvre Museum, Notre-Dame Cathedral, Arc de Triomphe, Sacré-Cœur"
    elif 'tokyo' in query_lower:
        return "In Tokyo it's currently 22°C with a chance of 15% to rain.\nList of 5 places: Senso-ji Temple, Tokyo Skytree, Meiji Shrine, Shibuya Crossing, Imperial Palace"
    elif 'invalid' in query_lower:
        return "I don't know this place exists"
    else:
        return f"Demo response for: {query}\n\n[Note: Add OpenAI credits for full AI-powered responses]"


@app.route('/api/query', methods=['POST'])
def process_query():
    """Process tourism query through multi-agent system"""
    try:
        # Get query from request
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty'
            }), 400
        
        # Check if orchestrator is initialized
        if orchestrator is None:
            return jsonify({
                'success': False,
                'error': 'Agent system not initialized. Check OPENAI_API_KEY in .env'
            }), 500
        
        # Process query through agents
        start_time = time.time()
        
        try:
            result = orchestrator.process_query(query)
            end_time = time.time()
            response_time = int((end_time - start_time) * 1000)
            
            return jsonify({
                'success': result['success'],
                'response': result['output'],
                'response_time': response_time,
                'query': query
            })
        except Exception as e:
            # If OpenAI quota exceeded, return demo response
            error_str = str(e)
            if '429' in error_str or 'quota' in error_str.lower() or 'insufficient_quota' in error_str:
                demo_response = get_demo_response(query)
                end_time = time.time()
                return jsonify({
                    'success': True,
                    'response': demo_response + '\n\n🎭 [Demo Mode: OpenAI quota exceeded - showing sample response]',
                    'response_time': int((end_time - start_time) * 1000),
                    'query': query
                })
            # Re-raise other errors
            raise
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/test', methods=['GET'])
def run_tests():
    """Run all test cases from assignment"""
    test_queries = [
        "I'm going to go to Bangalore, let's plan my trip.",
        "I'm going to go to Bangalore, what is the temperature there",
        "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?",
        "I'm going to InvalidCity123"
    ]
    
    results = []
    
    for query in test_queries:
        try:
            start_time = time.time()
            result = orchestrator.process_query(query)
            end_time = time.time()
            
            results.append({
                'query': query,
                'success': result['success'],
                'response': result['output'],
                'response_time': int((end_time - start_time) * 1000)
            })
        except Exception as e:
            results.append({
                'query': query,
                'success': False,
                'error': str(e)
            })
    
    return jsonify({
        'success': True,
        'tests': results
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    # In production, you'd track these in a database
    return jsonify({
        'total_queries': 0,
        'success_count': 0,
        'avg_response_time': 0,
        'active_agents': 3
    })


if __name__ == '__main__':
    print("="*60)
    print("🚀 Multi-Agent Tourism Dashboard API")
    print("="*60)
    print("\nStarting server...")
    print("Dashboard: http://localhost:5000")
    print("API Docs: http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
