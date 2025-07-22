# Claude Project Settings & Documentation Protocol

## Mandatory Documentation Protocol
**ALWAYS follow this protocol when working with Ruben:**

### 1. Knowledge Base Updates Required
Whenever we:
- **Solve a technical problem** â†’ Update PROJECT_KNOWLEDGE.md with the fix
- **Discover system-specific quirks** â†’ Document in the "Windows-Specific Instructions" section  
- **Find working vs non-working commands** â†’ Add to "Directory Navigation Commands" or create new section
- **Complete a project milestone** â†’ Update "What's Been Accomplished"
- **Learn something about Ruben's environment** â†’ Add to "Operating Environment" section

### 2. Auto-Documentation Triggers
**Immediately update documentation when:**
- Commands work differently than expected (like `py` vs `python`)
- Configuration files need specific formatting
- Error messages reveal system-specific issues
- File paths or directory structures are discovered
- New tools or capabilities are successfully implemented

### 3. Documentation Format
**Always include:**
- **What the problem was**
- **What the solution is** 
- **Why it works**
- **Exact commands/code used**
- **Any Windows-specific considerations**

### 4. Session Workflow
**At the end of each session:**
1. Check if PROJECT_KNOWLEDGE.md needs updates
2. Add any new discoveries to appropriate sections
3. Update "Current Project Status" if things changed
4. Note any unresolved issues for next time

### 5. Critical Areas to Document
- **Python/command line quirks** (like the `py` vs `python` issue)
- **File path differences** between what Claude expects vs Windows reality
- **Configuration file formats** that work vs don't work
- **Error patterns** and their solutions
- **Successful tool implementations** and how they work

## Communication Reminders
- Ruben is a complete beginner - always explain technical terms
- Use available MCP tools actively instead of asking manual tasks
- Give complete file paths and step-by-step instructions
- Celebrate wins and keep motivation high
- Always verify environment before giving OS-specific instructions

## Current Project Priority
Focus on building useful, working tools that solve real problems while teaching Ruben through hands-on experience.
