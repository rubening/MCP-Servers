# Browser Downloads Configuration Guide
**Target Directory:** G:\INBOX\Downloads_Processing

## CHROME CONFIGURATION

### Method 1: Settings Menu
1. Open Chrome
2. Click three dots (â‹®) â†’ Settings
3. Advanced â†’ Downloads
4. Change "Location" to: G:\INBOX\Downloads_Processing
5. âœ… Turn ON "Ask where to save each file before downloading" (optional - gives you control)

### Method 2: Chrome Shortcut Modification
Right-click Chrome shortcut â†’ Properties â†’ Target field, add:
```
--download-default-directory="G:\INBOX\Downloads_Processing"
```

## BRAVE CONFIGURATION

### Settings Menu
1. Open Brave
2. Click hamburger menu (â˜°) â†’ Settings  
3. Additional Settings â†’ Downloads
4. Change "Location" to: G:\INBOX\Downloads_Processing
5. âœ… Turn ON "Ask where to save each file before downloading" (optional)

## EDGE CONFIGURATION

### Settings Menu
1. Open Edge
2. Click three dots (...) â†’ Settings
3. Downloads (left sidebar)
4. Change "Location" to: G:\INBOX\Downloads_Processing
5. âœ… Turn ON "Ask me what to do with each download" (optional)

## REGISTRY METHOD (Advanced - All Browsers)

### PowerShell Command (Run as Administrator)
```powershell
# Set default download location for new user profiles
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" -Force
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" -Name "{374DE290-123F-4565-9164-39C4925E467B}" -Value "G:\INBOX\Downloads_Processing"
```

## VERIFICATION COMMANDS

### Test Download Location
```powershell
# Check current download folder setting
Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" -Name "{374DE290-123F-4565-9164-39C4925E467B}"
```

## WHY THIS WORKS FOR SI POLR

### Cognitive Load Reduction
- **No decision required** during download moment
- **Batch processing** during weekly maintenance 
- **Consistent location** eliminates "where did I save that?" moments
- **Staging prevents accumulation** across multiple drives

### Processing Workflow
1. **Daily:** Download â†’ G:\INBOX\Downloads_Processing (automatic)
2. **Weekly:** Process staging folder â†’ Move to permanent PARA locations
3. **Monthly:** Review and archive older processed items

### Benefits
- **Eliminates scattered downloads** across D:, E:, F:, I: drives
- **Reduces cognitive burden** of real-time file organization
- **Maintains PARA integrity** through systematic processing
- **Compensates for Si detail retention weakness**
