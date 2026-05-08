import re
from typing import Dict

class ValidationService:
    @staticmethod
    def validate_email(email: str) -> Dict[str, bool]:
        # Improved regex to handle common email patterns including subdomains and plus-tagging
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.search(regex, email))
        return {"is_valid": is_valid}

    @staticmethod
    def validate_address(address: str) -> Dict[str, bool]:
        # Very basic mock validation
        is_valid = len(address.split(',')) >= 2
        return {"is_valid": is_valid}
