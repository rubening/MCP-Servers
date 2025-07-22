# PowerShell Update Instructions
**Generated:** June 12, 2025

## MANUAL POWERSHELL UPDATE

### Method 1: Microsoft Store (Easiest)
1. Open Microsoft Store
2. Search for "PowerShell"
3. Click "Get" or "Update" if available
4. Restart your terminal after installation

### Method 2: Direct Download
1. Go to: https://github.com/PowerShell/PowerShell/releases/latest
2. Download: PowerShell-7.x.x-win-x64.msi
3. Run the installer
4. Choose "Add PowerShell to PATH"
5. Restart your terminal

### Method 3: Command Line (if you have winget)
```cmd
winget install --id Microsoft.Powershell --source winget
```

### Verification
After installation, open a new PowerShell window and run:
```powershell
$PSVersionTable.PSVersion
```

You should see version 7.x.x instead of 5.x.x

## BENEFITS OF UPDATED POWERSHELL
- Better performance
- More features for file operations
- Enhanced security
- Better compatibility with modern tools
- Improved scripting capabilities

## CURRENT VERSION CHECK
Your current version appears to be Windows PowerShell 5.x (older)
Updated version will be PowerShell 7.x (newer)
