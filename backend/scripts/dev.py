#!/usr/bin/env python3
"""
Development utilities and scripts.
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str = ""):
    """Run a command and handle errors."""
    print(f"🔄 {description or command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    else:
        print(f"✅ Success: {description or command}")
        if result.stdout:
            print(result.stdout)
        return True


def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing dependencies...")
    return run_command("pip install -r requirements.txt", "Installing dependencies")


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    return run_command("pytest", "Running tests")


def run_linting():
    """Run code linting."""
    print("🔍 Running linting...")
    
    commands = [
        ("black --check app tests", "Black formatting check"),
        ("isort --check-only app tests", "Import sorting check"),
        ("flake8 app tests", "Flake8 linting"),
        ("mypy app", "Type checking")
    ]
    
    all_passed = True
    for command, description in commands:
        if not run_command(command, description):
            all_passed = False
    
    return all_passed


def format_code():
    """Format code with black and isort."""
    print("🎨 Formatting code...")
    
    commands = [
        ("black app tests", "Black formatting"),
        ("isort app tests", "Import sorting")
    ]
    
    all_passed = True
    for command, description in commands:
        if not run_command(command, description):
            all_passed = False
    
    return all_passed


def run_server():
    """Run the development server."""
    print("🚀 Starting development server...")
    return run_command("python run.py", "Starting server")


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("""
🛠️  Scaffold Forge Development Tools

Usage: python scripts/dev.py <command>

Commands:
  install     Install dependencies
  test        Run tests
  lint        Run linting checks
  format      Format code
  server      Start development server
  all         Run all checks (install, format, lint, test)
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "install":
        install_dependencies()
    elif command == "test":
        run_tests()
    elif command == "lint":
        run_linting()
    elif command == "format":
        format_code()
    elif command == "server":
        run_server()
    elif command == "all":
        print("🔄 Running all development checks...")
        success = True
        success &= install_dependencies()
        success &= format_code()
        success &= run_linting()
        success &= run_tests()
        
        if success:
            print("🎉 All checks passed!")
        else:
            print("❌ Some checks failed!")
            sys.exit(1)
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
