import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest.mock
from colorama import Fore, Style, init
from ui_mock import UiMock
from test_user_authentication import CustomInputMock
init(autoreset=True)

# Import all test modules
from test_user_authentication import test_user_authentication, test_user_registration
from test_product_management import test_view_products, test_add_product, test_remove_product
from test_expense_management import test_view_expenses, test_add_expense, test_remove_expense, test_profit_simulation

def print_header(title):
    print("\n" + "="*80)
    print(Fore.CYAN + Style.BRIGHT + title.center(80))
    print("="*80)

def print_section(title):
    print("\n" + "-"*80)
    print(Fore.YELLOW + title)
    print("-"*80)

def run_all_tests():
    """Run all functionality tests and display a comprehensive summary"""
    print_header("XPENCE COMPREHENSIVE FUNCTIONALITY TESTING")
    
    results = {}
    total_passed = 0
    total_tests = 0
    
    # Apply UI mocking for all tests to prevent interactive prompts
    with unittest.mock.patch('ui.Ui', UiMock):
        # User Authentication Tests
        print_section("Running User Authentication Tests")
        results["auth_login"] = test_user_authentication()
        results["auth_register"] = test_user_registration()
        
        # Product Management Tests
        print_section("Running Product Management Tests")
        results["product_view"] = test_view_products()
        results["product_add"] = test_add_product()
        results["product_remove"] = test_remove_product()
        
        # Expense Management Tests
        print_section("Running Expense Management Tests")
        results["expense_view"] = test_view_expenses()
        results["expense_add"] = test_add_expense()
        results["expense_remove"] = test_remove_expense()
        results["expense_profit"] = test_profit_simulation()
    
    # Calculate totals
    for module, (passed, total) in results.items():
        total_passed += passed
        total_tests += total
    
    # Print comprehensive summary
    print_header("XPENCE FUNCTIONALITY TESTING SUMMARY")
    
    # User Auth Summary
    auth_passed = results["auth_login"][0] + results["auth_register"][0]
    auth_total = results["auth_login"][1] + results["auth_register"][1]
    print(f"{Fore.CYAN}User Authentication: {Fore.GREEN}{auth_passed}/{auth_total} tests passed ({auth_passed/auth_total*100:.1f}%)")
    print(f"  {Fore.WHITE}Login Tests: {Fore.GREEN}{results['auth_login'][0]}/{results['auth_login'][1]} passed")
    print(f"  {Fore.WHITE}Registration Tests: {Fore.GREEN}{results['auth_register'][0]}/{results['auth_register'][1]} passed")
    
    # Product Management Summary
    product_passed = results["product_view"][0] + results["product_add"][0] + results["product_remove"][0]
    product_total = results["product_view"][1] + results["product_add"][1] + results["product_remove"][1]
    print(f"\n{Fore.CYAN}Product Management: {Fore.GREEN}{product_passed}/{product_total} tests passed ({product_passed/product_total*100:.1f}%)")
    print(f"  {Fore.WHITE}View Products Tests: {Fore.GREEN}{results['product_view'][0]}/{results['product_view'][1]} passed")
    print(f"  {Fore.WHITE}Add Product Tests: {Fore.GREEN}{results['product_add'][0]}/{results['product_add'][1]} passed")
    print(f"  {Fore.WHITE}Remove Product Tests: {Fore.GREEN}{results['product_remove'][0]}/{results['product_remove'][1]} passed")
    
    # Expense Management Summary
    expense_passed = (results["expense_view"][0] + results["expense_add"][0] + 
                      results["expense_remove"][0] + results["expense_profit"][0])
    expense_total = (results["expense_view"][1] + results["expense_add"][1] + 
                    results["expense_remove"][1] + results["expense_profit"][1])
    print(f"\n{Fore.CYAN}Expense Management: {Fore.GREEN}{expense_passed}/{expense_total} tests passed ({expense_passed/expense_total*100:.1f}%)")
    print(f"  {Fore.WHITE}View Expenses Tests: {Fore.GREEN}{results['expense_view'][0]}/{results['expense_view'][1]} passed")
    print(f"  {Fore.WHITE}Add Expense Tests: {Fore.GREEN}{results['expense_add'][0]}/{results['expense_add'][1]} passed")
    print(f"  {Fore.WHITE}Remove Expense Tests: {Fore.GREEN}{results['expense_remove'][0]}/{results['expense_remove'][1]} passed")
    print(f"  {Fore.WHITE}Profit Simulation Tests: {Fore.GREEN}{results['expense_profit'][0]}/{results['expense_profit'][1]} passed")
    
    # Overall Summary
    print("\n" + "="*80)
    overall_percentage = total_passed / total_tests * 100 if total_tests > 0 else 0
    print(f"{Fore.CYAN}Overall Test Results: {Fore.GREEN}{total_passed}/{total_tests} tests passed ({overall_percentage:.1f}%)")
    print("="*80)
    
    # Return test status (useful for CI/CD integration)
    return total_passed == total_tests

if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print(f"\n{Fore.GREEN}All tests passed successfully!")
        sys.exit(0)
    else:
        print(f"\n{Fore.RED}Some tests failed. Please check the detailed report above.")
        sys.exit(1)