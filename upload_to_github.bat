@echo off
echo ========================================
echo     AspireHR - GitHub Upload Script
echo ========================================
echo.

REM Navigate to the AspireHR directory
cd /d "C:\Users\suresh.kumar.INNOPAYAD\OneDrive - INNOPAY TECHNOLOGIES PRIVATE LIMITED\Documents\GitHub\hrms\aspirehr"

echo Current directory: %CD%
echo.

REM Check if Git is available
echo Checking Git installation...
git --version
if %errorlevel% neq 0 (
    echo ERROR: Git not found. Please install Git first.
    pause
    exit /b 1
)

echo Git is available!
echo.

REM Configure Git (if not already configured)
echo Configuring Git...
git config --global user.name "Suresh Kumar"
git config --global user.email "suresh@innopay.com"
echo Git configured successfully!
echo.

REM Check if repository is already initialized
if exist ".git" (
    echo Repository already initialized.
) else (
    echo Initializing Git repository...
    git init
    echo Repository initialized!
)
echo.

REM Add remote origin (if not already added)
echo Adding remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/innopay-suresh/AspireHR.git
echo Remote origin added!
echo.

REM Create and switch to main branch
echo Creating main branch...
git checkout -b main 2>nul || git checkout main
echo On main branch!
echo.

REM Add all files
echo Adding all files to Git...
git add .
echo Files added to staging area!
echo.

REM Create commit
echo Creating commit...
git commit -m "Initial commit: AspireHR - Modern HR Management System

- Complete app structure with all modules  
- Dynamic leave allocation system with custom date support
- Comprehensive API endpoints for HR operations
- User interface with JavaScript components
- Mock implementations for development environment
- Full documentation and setup guides
- Professional README with featured capabilities
- Contributing guidelines and MIT license"

if %errorlevel% equ 0 (
    echo Commit created successfully!
) else (
    echo Commit failed or no changes to commit.
)
echo.

REM Push to GitHub
echo Pushing to GitHub...
echo NOTE: You may need to authenticate with GitHub
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo     SUCCESS! Upload completed!
    echo ========================================
    echo.
    echo Your AspireHR repository is now available at:
    echo https://github.com/innopay-suresh/AspireHR
    echo.
    echo What's uploaded:
    echo - Professional README.md with documentation
    echo - Complete app structure (35 files)
    echo - Dynamic leave allocation system
    echo - API endpoints and documentation
    echo - Contributing guidelines
    echo - MIT License
    echo - Development setup guides
    echo.
) else (
    echo.
    echo ========================================
    echo     UPLOAD FAILED
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Authentication required - GitHub will prompt for credentials
    echo 2. Repository doesn't exist - create it on GitHub first
    echo 3. Network connectivity issues
    echo.
    echo To retry, run this script again or use:
    echo git push -u origin main
)

echo.
echo Press any key to exit...
pause >nul
