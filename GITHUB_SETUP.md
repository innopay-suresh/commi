# GitHub Setup Guide for AspireHR

## Step 1: Install Git on Windows

### Option A: Download Git for Windows
1. Go to https://git-scm.com/download/win
2. Download the latest version
3. Run the installer with default settings
4. Restart your terminal/PowerShell

### Option B: Using Winget (Windows Package Manager)
```powershell
winget install --id Git.Git -e --source winget
```

### Option C: Using Chocolatey (if installed)
```powershell
choco install git
```

## Step 2: Configure Git (After Installation)

Open PowerShell and run:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Initialize Git Repository

Navigate to your AspireHR directory and run:
```powershell
cd "C:\Users\suresh.kumar.INNOPAYAD\OneDrive - INNOPAY TECHNOLOGIES PRIVATE LIMITED\Documents\GitHub\hrms\aspirehr"
git init
```

## Step 4: Add Remote Repository

Add your GitHub repository as the remote origin:
```powershell
git remote add origin https://github.com/innopay-suresh/AspireHR.git
```

## Step 5: Create and Switch to Main Branch

```powershell
git checkout -b main
```

## Step 6: Add Files to Git

Add all your files to the repository:
```powershell
git add .
```

## Step 7: Commit Your Changes

Create your first commit:
```powershell
git commit -m "Initial commit: AspireHR - Modern HR Management System

- Complete app structure with all modules
- Dynamic leave allocation system
- Comprehensive API endpoints
- User interface with JavaScript components
- Mock implementations for development
- Full documentation and setup guides"
```

## Step 8: Push to GitHub

Push your code to GitHub:
```powershell
git push -u origin main
```

## Step 9: Verify on GitHub

1. Go to https://github.com/innopay-suresh/AspireHR
2. You should see all your files uploaded
3. The README.md will display automatically

## Alternative: Using GitHub Desktop

If you prefer a GUI approach:

1. Download GitHub Desktop from https://desktop.github.com
2. Install and sign in to your GitHub account
3. Click "Add an Existing Repository from your Hard Drive"
4. Select your AspireHR folder
5. Click "Publish repository"
6. Choose "innopay-suresh/AspireHR" as the repository name

## Step 10: Repository Settings (Optional)

Once your repository is uploaded, you can:

### Enable GitHub Pages
1. Go to Settings → Pages
2. Choose source branch (main)
3. Your documentation will be available at a public URL

### Set Up Branch Protection
1. Go to Settings → Branches
2. Add branch protection rules for main branch
3. Require pull request reviews

### Configure Repository Settings
1. Add repository description: "AspireHR - Modern HR and Payroll Management System built on Frappe Framework"
2. Add topics: `frappe` `hr` `payroll` `python` `javascript` `erp` `hrms`
3. Add website URL if you have one

## Common Issues and Solutions

### Issue: Git not recognized
**Solution**: Restart your terminal after installing Git, or add Git to PATH manually

### Issue: Permission denied (publickey)
**Solution**: Set up SSH keys or use HTTPS with personal access token

### Issue: Repository already exists
**Solution**: If the repository already exists on GitHub, clone it first:
```powershell
git clone https://github.com/innopay-suresh/AspireHR.git
```
Then copy your files into the cloned directory.

## Next Steps After Upload

1. **Create Issues**: Add any known bugs or feature requests as GitHub Issues
2. **Set Up CI/CD**: Configure GitHub Actions for automated testing
3. **Create Wiki**: Add detailed documentation to the repository wiki
4. **Invite Collaborators**: Add team members to the repository
5. **Create Releases**: Tag versions and create releases for deployment

## Backup Your Work

Before making any changes, always:
```powershell
git status          # Check current status
git add .           # Add all changes
git commit -m "Your commit message"
git push           # Push to GitHub
```

## Repository Structure After Upload

```
AspireHR/
├── README.md                 # Main repository documentation
├── LICENSE                   # MIT License
├── DEVELOPMENT_SETUP.md     # Development setup guide
├── GITHUB_SETUP.md          # This file
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── hooks.py                 # Frappe hooks
├── modules.txt              # Module list
├── patches.txt              # Database patches
├── __init__.py              # Package initialization
├── api/                     # API endpoints
├── human_resources/         # HR module
├── payroll/                 # Payroll module
├── notifications/           # Notification module
├── setup/                   # Setup module
├── startup/                 # Startup module
├── public/                  # Frontend assets
└── docs/                    # Documentation
```

## Support

If you encounter any issues:
1. Check the [GitHub Issues](https://github.com/innopay-suresh/AspireHR/issues)
2. Create a new issue with details
3. Contact support at suresh@innopay.com

---

**Happy Coding!** 🚀
