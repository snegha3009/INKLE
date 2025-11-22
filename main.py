#!/usr/bin/env python3
"""
Multi-Agent Tourism System - Main Entry Point
Run this file to start the interactive tourism assistant.
"""

import os
import sys
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.tools import TourismTools
from agents.orchestrator import TourismOrchestrator


def run_tests():
    """Run test cases from the assignment"""
    print("="*60)
    print("RUNNING ASSIGNMENT TEST CASES")
    print("="*60)
    
    test_queries = [
        "I'm going to go to Bangalore, let's plan my trip.",
        "I'm going to go to Bangalore, what is the temperature there",
        "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?",
        "I'm going to InvalidCity123"
    ]
    
    # Create tools and orchestrator
    tools_factory = TourismTools()
    tools = tools_factory.create_tools()
    orchestrator = TourismOrchestrator(tools, verbose=False)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}")
        print(f"{'='*60}")
        print(f"User: {query}\n")
        
        result = orchestrator.process_query(query)
        print(f"Assistant: {result['output']}")
        print(f"Status: {'✓ Success' if result['success'] else '✗ Failed'}")


def run_interactive():
    """Run interactive chat mode"""
    # Create tools and orchestrator
    tools_factory = TourismTools()
    tools = tools_factory.create_tools()
    orchestrator = TourismOrchestrator(tools, verbose=True)
    
    # Start chat
    orchestrator.chat()


def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("="*60)
        print("ERROR: OPENAI_API_KEY not found!")
        print("="*60)
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to .env")
        print("3. Run this script again\n")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            run_tests()
            return
        elif sys.argv[1] == "help":
            print("Usage:")
            print("  python main.py         - Run interactive chat mode")
            print("  python main.py test    - Run assignment test cases")
            print("  python main.py help    - Show this help message")
            return
    
    # Default: run interactive mode
    run_interactive()


if __name__ == "__main__":
    main()  