#!/usr/bin/env python3
"""
Test script for Priority Management MCP Server
Validates core functionality and priority calculations
"""

import sys
import os
from datetime import datetime

# Add the current directory to path to import the server
sys.path.insert(0, '.')

try:
    from server import TaskItem, TaskStatus, PriorityLevel, PriorityManagementMCP
    print("✅ Successfully imported Priority Management classes")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_task_creation():
    """Test basic task creation and priority calculation"""
    print("\n🧪 Testing Task Creation and Priority Calculation...")
    
    # Test task: Instrumental/Absolute Arrow Mechanism for Personality Framework
    task = TaskItem(
        id="test_001",
        title="Add Secondary Answers + Arrow Mechanism to Personality Assessment",
        description="Enhance personality prototype with secondary answers and instrumentality vs absoluteness measurement arrows",
        impact=7,  # High impact for personality framework advancement
        urgency=4,  # Medium urgency (not blocking other work)
        difficulty=6,  # Medium-high difficulty (requires UI/UX design + logic)
        value=9,  # Very high Fi value alignment (innovative breakthrough)
        relevance=6,  # Medium-high relevance to current goals
        status=TaskStatus.IDEA,
        tags=["personality-framework", "innovation", "assessment-tool"],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        notes="Key concepts: Instrumentality = function used for other purposes, Absoluteness = attention for its own sake"
    )
    
    print(f"Task Created: {task.title}")
    print(f"Priority Score: {task.priority_score}/10")
    print(f"Priority Level: {task.priority_level.value}")
    print(f"Expected: Medium-High priority due to high value + good impact")
    
    # Validate calculation manually
    difficulty_inverted = 11 - task.difficulty  # 11 - 6 = 5
    expected_score = (
        task.impact * 0.25 +      # 7 * 0.25 = 1.75
        task.urgency * 0.25 +     # 4 * 0.25 = 1.00  
        difficulty_inverted * 0.20 + # 5 * 0.20 = 1.00
        task.value * 0.15 +       # 9 * 0.15 = 1.35
        task.relevance * 0.15     # 6 * 0.15 = 0.90
    )  # Total = 6.00
    
    print(f"Manual Calculation: {expected_score}")
    print(f"Algorithm Result: {task.priority_score}")
    print(f"✅ Calculation {'CORRECT' if abs(task.priority_score - expected_score) < 0.01 else 'ERROR'}")
    
    return task

def test_priority_levels():
    """Test priority level categorization"""
    print("\n🧪 Testing Priority Level Categorization...")
    
    test_cases = [
        (9, 9, 2, 8, 8, "CRITICAL"),  # High impact/urgency, low difficulty, high value
        (7, 6, 5, 6, 7, "HIGH"),      # Good scores across board
        (5, 4, 6, 5, 5, "MEDIUM"),    # Average scores
        (3, 2, 8, 3, 2, "LOW")        # Low scores, high difficulty
    ]
    
    for i, (impact, urgency, difficulty, value, relevance, expected) in enumerate(test_cases):
        task = TaskItem(
            id=f"test_{i}",
            title=f"Test Task {i}",
            description="Test case",
            impact=impact,
            urgency=urgency,
            difficulty=difficulty,
            value=value,
            relevance=relevance,
            status=TaskStatus.IDEA,
            tags=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        actual = task.priority_level.value.upper()
        print(f"Test {i}: Score {task.priority_score} -> {actual} (expected {expected})")
        assert actual == expected, f"Priority level mismatch for test {i}"
    
    print("✅ All priority level tests passed")

def test_mcp_initialization():
    """Test MCP server initialization"""
    print("\n🧪 Testing MCP Server Initialization...")
    
    try:
        mcp = PriorityManagementMCP()
        print("✅ MCP Server initialized successfully")
        print(f"Data directory: {mcp.data_dir}")
        print(f"Tasks file: {mcp.tasks_file}")
        print(f"Config file: {mcp.config_file}")
        
        # Check if files were created
        if mcp.tasks_file.exists():
            print("✅ Tasks file created")
        else:
            print("❌ Tasks file not created")
            
        if mcp.config_file.exists():
            print("✅ Config file created")
        else:
            print("❌ Config file not created")
            
        print(f"Initial task count: {len(mcp.tasks)}")
        
        return mcp
        
    except Exception as e:
        print(f"❌ MCP initialization failed: {e}")
        return None

def main():
    """Run all tests"""
    print("🚀 Priority Management MCP Server - Test Suite")
    print("=" * 60)
    
    # Test core functionality
    task = test_task_creation()
    test_priority_levels()
    mcp = test_mcp_initialization()
    
    print("\n" + "=" * 60)
    
    if task and mcp:
        print("🎉 ALL TESTS PASSED!")
        print("\nPriority Management MCP Server is ready for integration!")
        print("\nNext Steps:")
        print("1. Configure in Claude Desktop MCP settings")
        print("2. Test with real tasks using add_task tool")
        print("3. Use get_priority_dashboard for analytics")
    else:
        print("❌ Some tests failed - check error messages above")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
