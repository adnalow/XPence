"""
Mock UI class to prevent UI interactions during testing
"""

class UiMock:
    """Mock version of UI class that suppresses all UI interactions"""
    @staticmethod
    def display_header(text):
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def display_success(text):
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def display_error(text):
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def display_menu(title, options):
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def get_user_choice(max_option):
        """Mock implementation that returns 0"""
        return 0
        
    @staticmethod
    def clear_screen():
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def display_separator():
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def display_info(text):
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def display_product(index, name, price):
        """Mock implementation that does nothing"""
        pass
        
    @staticmethod
    def display_expense(index, name, amount):
        """Mock implementation that does nothing"""
        pass