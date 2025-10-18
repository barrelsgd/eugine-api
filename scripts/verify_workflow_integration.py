#!/usr/bin/env python3
"""
Workflow Integration Verification Script

This script verifies that all GitHub Actions workflows are properly integrated
and will work correctly when pushed to the master branch.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Set, Any


def load_workflow(file_path: Path) -> Dict[str, Any]:
    """Load and parse a GitHub Actions workflow file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return {}


def extract_workflow_info(workflow_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
    """Extract key information from a workflow."""
    return {
        'name': workflow_data.get('name', 'Unknown'),
        'filename': filename,
        'triggers': workflow_data.get('on', {}),
        'jobs': list(workflow_data.get('jobs', {}).keys()),
        'permissions': workflow_data.get('permissions', {}),
    }


def check_workflow_names(workflows: List[Dict[str, Any]]) -> List[str]:
    """Check for workflow name consistency issues."""
    issues = []
    workflow_names = {w['name']: w['filename'] for w in workflows}
    
    # Check for duplicate names
    seen_names = set()
    for name, filename in workflow_names.items():
        if name in seen_names:
            issues.append(f"❌ Duplicate workflow name '{name}' in {filename}")
        seen_names.add(name)
    
    return issues


def check_trigger_consistency(workflows: List[Dict[str, Any]]) -> List[str]:
    """Check that workflows have consistent trigger patterns."""
    issues = []
    
    # Expected trigger patterns
    ci_workflows = ['CI', 'Test Docker Compose']
    deployment_workflows = ['Deploy to Staging', 'Deploy to production']
    
    for workflow in workflows:
        name = workflow['name']
        triggers = workflow['triggers']
        
        if name in ci_workflows:
            # CI workflows should trigger on push to master and PRs
            if 'push' not in triggers:
                issues.append(f"❌ {name} should trigger on push events")
            if 'pull_request' not in triggers:
                issues.append(f"❌ {name} should trigger on pull_request events")
        
        elif name in deployment_workflows:
            # Deployment workflows should have specific triggers
            if name == 'Deploy to Staging' and 'push' not in triggers:
                issues.append(f"❌ {name} should trigger on push to master")
            elif name == 'Deploy to production' and 'release' not in triggers:
                issues.append(f"❌ {name} should trigger on release events")
    
    return issues


def check_workflow_dependencies(workflows: List[Dict[str, Any]]) -> List[str]:
    """Check that workflow dependencies are correctly configured."""
    issues = []
    workflow_names = {w['name']: w for w in workflows}
    
    # Check that required workflows exist
    required_workflows = ['CI', 'Test Docker Compose']
    for required in required_workflows:
        if required not in workflow_names:
            issues.append(f"❌ Required workflow '{required}' not found")
    
    # Check Smokeshow workflow references CI correctly
    smokeshow = workflow_names.get('Smokeshow')
    if smokeshow:
        triggers = smokeshow['triggers']
        if 'workflow_run' in triggers:
            workflow_run = triggers['workflow_run']
            if isinstance(workflow_run, dict) and 'workflows' in workflow_run:
                referenced_workflows = workflow_run['workflows']
                if 'CI' not in referenced_workflows:
                    issues.append("❌ Smokeshow workflow should reference 'CI' workflow")
    
    return issues


def check_environment_files() -> List[str]:
    """Check that required environment files exist."""
    issues = []
    required_files = [
        '.env.local.example',
        '.env.staging.example', 
        '.env.production.example'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            issues.append(f"❌ Required environment file '{file_path}' not found")
        else:
            print(f"✅ Found {file_path}")
    
    return issues


def check_docker_compose_files() -> List[str]:
    """Check that required Docker Compose files exist."""
    issues = []
    required_files = [
        'docker-compose.yml',
        'docker-compose.override.yml',
        'docker-compose.staging.yml',
        'docker-compose.prod.yml'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            issues.append(f"❌ Required Docker Compose file '{file_path}' not found")
        else:
            print(f"✅ Found {file_path}")
    
    return issues


def main():
    """Main verification function."""
    print("🔍 GitHub Actions Workflow Integration Verification")
    print("=" * 60)
    
    # Load all workflow files
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return 1
    
    workflows = []
    for workflow_file in workflows_dir.glob('*.yml'):
        workflow_data = load_workflow(workflow_file)
        if workflow_data:
            workflow_info = extract_workflow_info(workflow_data, workflow_file.name)
            workflows.append(workflow_info)
            print(f"✅ Loaded workflow: {workflow_info['name']} ({workflow_file.name})")
    
    print(f"\n📊 Found {len(workflows)} workflows")
    
    # Run all checks
    all_issues = []
    
    print("\n🔍 Checking workflow names...")
    all_issues.extend(check_workflow_names(workflows))
    
    print("\n🔍 Checking trigger consistency...")
    all_issues.extend(check_trigger_consistency(workflows))
    
    print("\n🔍 Checking workflow dependencies...")
    all_issues.extend(check_workflow_dependencies(workflows))
    
    print("\n🔍 Checking environment files...")
    all_issues.extend(check_environment_files())
    
    print("\n🔍 Checking Docker Compose files...")
    all_issues.extend(check_docker_compose_files())
    
    # Report results
    print("\n" + "=" * 60)
    if all_issues:
        print("❌ WORKFLOW INTEGRATION ISSUES FOUND:")
        for issue in all_issues:
            print(f"  {issue}")
        print(f"\n🚨 Total issues: {len(all_issues)}")
        return 1
    else:
        print("✅ ALL WORKFLOW INTEGRATION CHECKS PASSED!")
        print("\n🚀 Your workflows are ready for master branch deployment!")
        return 0


if __name__ == '__main__':
    exit(main())
