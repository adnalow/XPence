import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest.mock
from user import User
from colorama import Fore
from ui_mock import UiMock

# Mock Database for testing
class MockDatabase:
    def fetch_one(self, query, params):
        if params[0] == "testuser" and params[1] == "password123":
            return [1]  # Mock user ID
        elif params[0] == "marie" and params[1] == "whUtth3si6m4???":
            return [2]  # Mock user ID
        return None

    def execute_query(self, query, params):
        # For testing registration
        pass

# Custom mock for input function to handle multiple calls
class CustomInputMock:
    def __init__(self, return_values=None):
        self.return_values = return_values or []
        self.call_count = 0
        
    def __call__(self, prompt=""):
        # If we have specified return values, use them in order
        if self.call_count < len(self.return_values):
            value = self.return_values[self.call_count]
            self.call_count += 1
            return value
        # Otherwise return an empty string for any additional calls
        return ""

# Function to test user authentication
def test_user_authentication():
    """Test the user authentication functionality with various scenarios"""
    db = MockDatabase()
    
    # Test login functionality
    test_cases = [
        {"id": "TC001", "description": "Valid credentials", 
         "input": {"username": "testuser", "password": "password123"}, 
         "expected": True},
        
        {"id": "TC002", "description": "Valid credentials (alternative user)", 
         "input": {"username": "marie", "password": "whUtth3si6m4???"}, 
         "expected": True},
        
        {"id": "TC003", "description": "Invalid password", 
         "input": {"username": "testuser", "password": "wrongpassword"}, 
         "expected": False},
        
        {"id": "TC004", "description": "Invalid username", 
         "input": {"username": "nonexistent", "password": "password123"}, 
         "expected": False},
        
        {"id": "TC005", "description": "Empty credentials", 
         "input": {"username": "", "password": ""}, 
         "expected": False},
        
        {"id": "TC006", "description": "Case sensitivity test", 
         "input": {"username": "TestUser", "password": "password123"}, 
         "expected": False}
    ]
    
    # Patch UI to avoid interactive displays
    with unittest.mock.patch('ui.Ui', UiMock):
        # Run all test cases and collect results
        results = []
        for test_case in test_cases:
            # Setup custom input mock for each test case
            input_mock = CustomInputMock([
                test_case["input"]["username"], 
                test_case["input"]["password"],
                ""  # For "Press Enter to continue..." if login fails
            ])
            
            # Apply the input mock for this test case
            with unittest.mock.patch('builtins.input', input_mock):
                user = User(db)
                result = user.login()
                status = "PASS" if result == test_case["expected"] else "FAIL"
                results.append({
                    "id": test_case["id"],
                    "description": test_case["description"],
                    "status": status,
                    "actual": result,
                    "expected": test_case["expected"]
                })
    
    # Display results in a formatted table
    print("\n" + "="*80)
    print("USER AUTHENTICATION TEST RESULTS".center(80))
    print("="*80)
    
    print(f"{'ID':<8} {'Description':<35} {'Status':<8} {'Expected':<12} {'Actual':<12}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['id']:<8} {result['description']:<35} "
              f"{Fore.GREEN if result['status']=='PASS' else Fore.RED}{result['status']:<8}{Fore.RESET} "
              f"{str(result['expected']):<12} {str(result['actual']):<12}")
    
    # Summary
    passed = sum(1 for result in results if result['status'] == "PASS")
    total = len(results)
    print("\n" + "-"*80)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*80)
    return passed, total

# Test registration functionality
def test_user_registration():
    """Test the user registration functionality with various scenarios"""
    db = MockDatabase()
    
    test_cases = [
        {"id": "TC007", "description": "Valid registration", 
         "input": {"username": "newuser", "password": "newpassword"}, 
         "expected": "Registration successful!"},
        
        {"id": "TC008", "description": "Empty username", 
         "input": {"username": "", "password": "password123"}, 
         "expected": "Invalid input"},
        
        {"id": "TC009", "description": "Empty password", 
         "input": {"username": "anotheruser", "password": ""}, 
         "expected": "Invalid input"}
    ]
    
    # Patch UI to avoid interactive displays
    with unittest.mock.patch('ui.Ui', UiMock):
        # Run all test cases and collect results
        results = []
        for test_case in test_cases:
            # Setup custom input mock for each test case
            input_mock = CustomInputMock([
                test_case["input"]["username"], 
                test_case["input"]["password"]
            ])
            
            # Apply the input mock for this test case
            with unittest.mock.patch('builtins.input', input_mock):
                user = User(db)
                try:
                    user.register()
                    if test_case["input"]["username"] and test_case["input"]["password"]:
                        result = "Registration successful!"
                    else:
                        result = "Invalid input"
                except ValueError as e:
                    result = str(e)
                except Exception:
                    result = "Invalid input"
                    
                status = "PASS" if result == test_case["expected"] else "FAIL"
                results.append({
                    "id": test_case["id"],
                    "description": test_case["description"],
                    "status": status,
                    "actual": result,
                    "expected": test_case["expected"]
                })
    
    # Display results in a formatted table
    print("\n" + "="*80)
    print("USER REGISTRATION TEST RESULTS".center(80))
    print("="*80)
    
    print(f"{'ID':<8} {'Description':<35} {'Status':<8} {'Expected':<20} {'Actual':<20}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['id']:<8} {result['description']:<35} "
              f"{Fore.GREEN if result['status']=='PASS' else Fore.RED}{result['status']:<8}{Fore.RESET} "
              f"{result['expected']:<20} {result['actual']:<20}")
    
    # Summary
    passed = sum(1 for result in results if result['status'] == "PASS")
    total = len(results)
    print("\n" + "-"*80)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*80)
    return passed, total

# Running the tests
if __name__ == "__main__":
    print(Fore.CYAN + "\nXPence Functionality Testing - User Authentication Module\n")
    auth_passed, auth_total = test_user_authentication()
    reg_passed, reg_total = test_user_registration()
    
    # Overall summary
    total_passed = auth_passed + reg_passed
    total_tests = auth_total + reg_total
    
    print("\n" + "="*80)
    print("OVERALL TEST SUMMARY".center(80))
    print("="*80)
    print(f"Authentication Tests: {auth_passed}/{auth_total} passed ({auth_passed/auth_total*100:.1f}%)")
    print(f"Registration Tests: {reg_passed}/{reg_total} passed ({reg_passed/reg_total*100:.1f}%)")
    print(f"Overall: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
    print("="*80)