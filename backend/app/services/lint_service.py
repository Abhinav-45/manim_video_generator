import subprocess
import os
from tempfile import NamedTemporaryFile

def lint_code(code: str) -> dict:
    """Lint Python code using ruff and return results."""
    temp_file = None
    try:
        # Create temporary file
        with NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp:
            temp.write(code)
            temp.flush()
            temp_file = temp.name
        
        # Run ruff linter
        result = subprocess.run(
            ["ruff", "check", temp_file], 
            capture_output=True, 
            text=True,
            timeout=10  # Add timeout to prevent hanging
        )
        
        # Check if linting passed
        if result.returncode == 0:
            return {"success": True, "errors": None}
        else:
            # Combine stdout and stderr for complete error info
            errors = result.stdout + result.stderr
            return {"success": False, "errors": errors.strip()}
            
    except subprocess.TimeoutExpired:
        return {"success": False, "errors": "Linting timeout - code may have infinite loops"}
    except FileNotFoundError:
        return {"success": False, "errors": "Ruff not found. Please install ruff: pip install ruff"}
    except Exception as e:
        return {"success": False, "errors": f"Linting error: {str(e)}"}
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except OSError:
                pass  # Ignore cleanup errors

