@echo off
echo.
echo ===============================================
echo   MCP PROJECT KNOWLEDGE OPTIMIZER
echo   AI-Effectiveness Analysis Tool
echo ===============================================
echo.

if "%1"=="" (
    echo Usage: analyze.bat [path_to_project_knowledge.md]
    echo.
    echo Examples:
    echo   analyze.bat project_knowledge.md
    echo   analyze.bat ..\my-project\project_knowledge.md
    echo   analyze.bat sample_project_knowledge.md
    echo.
    echo This tool will analyze your documentation and provide:
    echo   - Quality scores across multiple dimensions
    echo   - Specific recommendations for improvement
    echo   - Detailed metrics and section breakdown
    echo   - Tips for optimizing AI collaboration effectiveness
    echo.
    pause
    exit /b 1
)

echo Analyzing: %1
echo.

C:\Users\ruben\AppData\Local\Programs\Python\Python313\python.exe src\analyzer.py "%1"

echo.
echo Analysis complete!
pause
