# Web Version - THE ARCHITECTURE OF SHADOWS

## Overview

This is a basic web-based interactive version of the book. It provides navigation between volumes and editions.

## Files

- `index.html` - Main HTML structure
- `styles.css` - Styling for the web interface
- `script.js` - JavaScript for navigation and edition switching

## Usage

1. Open `index.html` in a web browser
2. Select either "Master Edition" or "Student Edition"
3. Navigate through volumes

## Current Implementation

This is a basic implementation that provides:
- Edition selection (Master/Student)
- Volume navigation
- Basic styling with dark theme

## Future Enhancements

For a full-featured web version, consider:

1. **Static Site Generator**: Use Hugo, Jekyll, or similar to convert markdown to HTML
2. **Backend Server**: Use Node.js/Express or similar to serve markdown content
3. **Chapter Loading**: Implement actual chapter content loading from markdown files
4. **Search Functionality**: Add search across all content
5. **Responsive Design**: Enhance mobile experience
6. **Progress Tracking**: Track reading progress
7. **Annotations**: Allow user annotations
8. **Dark/Light Mode**: Toggle between themes

## Static Site Generation

To generate a full static site from the markdown files:

```bash
# Using Hugo
hugo new site web-version
# Copy markdown content to content directory
# Configure theme
hugo

# Using Jekyll
jekyll new web-version
# Copy markdown content to _posts directory
jekyll build
```

## Local Server

To view the web version with proper file loading:

```bash
# Using Python
python -m http.server 8000

# Using Node.js (http-server)
npx http-server
```

Then navigate to http://localhost:8000
