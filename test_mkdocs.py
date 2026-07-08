#!/usr/bin/env python3
"""
Simple test script to verify MkDocs setup for SPlusthon documentation.
"""

import os
import sys
import subprocess

def check_mkdocs_installed():
    """Check if MkDocs is installed."""
    try:
        result = subprocess.run([sys.executable, '-m', 'mkdocs', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ MkDocs installed: {result.stdout.strip()}")
            return True
        else:
            print("✗ MkDocs not installed")
            return False
    except Exception as e:
        print(f"✗ Error checking MkDocs: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    required = {
        'mkdocs': 'mkdocs',
        'mkdocs-material': 'material'
    }
    missing = []
    
    for package, import_name in required.items():
        try:
            __import__(import_name)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} not installed")
            missing.append(package)
    
    return missing

def check_docs_structure():
    """Check if docs directory structure is correct."""
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    
    required_files = [
        'index.md',
        'installation.md',
        'quick-start.md',
        'api-reference.md',
        'faq.md',
        'concepts/index.md',
        'concepts/entities.md',
        'concepts/sessions.md',
        'concepts/events.md',
        'concepts/string-sessions.md',
        'concepts/errors.md',
        'concepts/full-api.md',
        'concepts/botapi-vs-mtproto.md',
        'concepts/asyncio.md',
        'examples/index.md',
        'examples/users.md',
        'examples/chats-and-channels.md',
        'examples/working-with-messages.md',
        'examples/word-of-warning.md',
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(docs_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file}")
        else:
            print(f"✗ {file}")
            missing_files.append(file)
    
    return missing_files

def check_mkdocs_config():
    """Check if mkdocs.yml is valid."""
    config_file = os.path.join(os.path.dirname(__file__), 'mkdocs.yml')
    
    if not os.path.exists(config_file):
        print("✗ mkdocs.yml not found")
        return False
    
    print("✓ mkdocs.yml found")
    
    # Try to parse YAML
    try:
        import yaml
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['site_name', 'theme', 'nav', 'plugins']
        for key in required_keys:
            if key in config:
                print(f"✓ {key} configured")
            else:
                print(f"✗ {key} missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error parsing mkdocs.yml: {e}")
        return False

def test_build():
    """Test building the documentation."""
    print("\nTesting documentation build...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'mkdocs', 'build', '--clean'], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✓ Documentation build successful")
            return True
        else:
            print(f"✗ Documentation build failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error building documentation: {e}")
        return False

def main():
    """Main test function."""
    print("SPlusthon Documentation MkDocs Test")
    print("=" * 50)
    
    # Check MkDocs installation
    print("\n1. Checking MkDocs installation...")
    mkdocs_installed = check_mkdocs_installed()
    
    # Check dependencies
    print("\n2. Checking dependencies...")
    missing_deps = check_dependencies()
    
    # Check docs structure
    print("\n3. Checking documentation structure...")
    missing_files = check_docs_structure()
    
    # Check mkdocs config
    print("\n4. Checking MkDocs configuration...")
    config_valid = check_mkdocs_config()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    all_ok = True
    
    if not mkdocs_installed:
        print("✗ MkDocs is not installed")
        all_ok = False
    
    if missing_deps:
        print(f"✗ Missing dependencies: {', '.join(missing_deps)}")
        all_ok = False
    
    if missing_files:
        print(f"✗ Missing documentation files: {len(missing_files)}")
        all_ok = False
    
    if not config_valid:
        print("✗ MkDocs configuration is invalid")
        all_ok = False
    
    if all_ok:
        print("✓ All checks passed!")
        print("\nTo build documentation:")
        print("  mkdocs build")
        print("\nTo serve documentation locally:")
        print("  mkdocs serve")
        print("\nTo deploy to GitHub Pages:")
        print("  mkdocs gh-deploy")
        
        # Test build
        print("\n" + "=" * 50)
        print("Testing documentation build...")
        if test_build():
            print("\n✓ Documentation is ready!")
        else:
            print("\n✗ Documentation build failed")
            all_ok = False
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
