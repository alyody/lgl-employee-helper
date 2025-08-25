"""
Test script for LGL Employee Helper
Run this to test the core functionality before deployment
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main app functions
try:
    from app import process_user_question, HANDBOOK_DATA
    print("✅ Successfully imported app functions")
except ImportError as e:
    print(f"❌ Failed to import app functions: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic question processing"""
    print("\n🧪 Testing Basic Functionality...")
    
    # Test cases
    test_questions = [
        "What are the working hours?",
        "How do I apply for annual leave?",
        "Tell me about sick leave",
        "What benefits do I get?",
        "What is the dress code?",
        "How does the disciplinary process work?",
        "Random question that doesn't match anything"
    ]
    
    for question in test_questions:
        print(f"\n📝 Question: {question}")
        response = process_user_question(question)
        print(f"🤖 Response length: {len(response)} characters")
        print(f"🔍 Contains handbook reference: {'Reference:' in response}")
        print(f"✨ Contains closing message: {'Have a great day' in response}")

def test_data_structure():
    """Test the handbook data structure"""
    print("\n📚 Testing Data Structure...")
    
    required_topics = ['leave', 'sick', 'working hours', 'benefits', 'conduct', 'disciplinary']
    
    for topic in required_topics:
        if topic in HANDBOOK_DATA:
            data = HANDBOOK_DATA[topic]
            print(f"✅ {topic}: Has title and content")
            assert 'title' in data, f"Missing title for {topic}"
            assert 'content' in data, f"Missing content for {topic}"
            assert len(data['content']) > 100, f"Content too short for {topic}"
        else:
            print(f"❌ Missing topic: {topic}")

def main():
    """Run all tests"""
    print("🚀 LGL Employee Helper - Test Suite")
    print("=" * 50)
    
    try:
        test_data_structure()
        test_basic_functionality()
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Ready for deployment.")
        print("\nNext steps:")
        print("1. Push code to GitHub repository")
        print("2. Deploy to Streamlit Cloud")
        print("3. Test the live application")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()