import os
import re

excluded_files = ['index.html']

def fix_css(content, is_html=True):
    # 1. Aggressive cleanup of invalid 'max-max-width' patterns
    # Handles variations like 'max-max-width' or 'max-max-width: 100%' or '@media...max-max-width'
    content = re.sub(r'max-max-width', 'max-width', content)
    
    # 2. Neutralize the problematic 1924px and other fixed-scale queries
    # Change them to a condition that never triggers (e.g., max-width: 0px)
    content = re.sub(r'@media\s+screen\s+and\s+\(max-width\s*:\s*[0-9a-zA-Z%]+\)', 
                     '/* Legacy Query Disabled */ @media (max-width: 0px)', content)
    
    # 3. Responsive Reset Block (Forced with !important)
    responsive_reset = """
    /* --- MOBILE RESPONSIVE RESET --- */
    * { box-sizing: border-box !important; }
    html { font-size: 16px !important; }
    body {
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding: 20px !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        text-align: center !important;
        word-wrap: break-word !important;
        overflow-x: hidden !important;
        float: none !important;
        background-color: #f4f4f4 !important; /* Standardize light background */
        color: #333 !important;
    }
    h1, #h1 { font-size: 2rem !important; margin: 0.5em 0 !important; padding: 10px !important; background: transparent !important; color: #00264d !important; }
    h2 { font-size: 1.5rem !important; margin: 0.5em 0 !important; }
    p, li, label, input, a { font-size: 1rem !important; margin: 10px auto !important; }
    
    img, video, iframe {
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 10px auto !important;
    }
    table, form, fieldset, details {
        max-width: 100% !important;
        width: 100% !important;
        margin: 15px auto !important;
        display: block !important;
    }
    .overview-btn {
        font-size: 0.8rem !important;
        padding: 8px 15px !important;
        top: 10px !important;
        right: 10px !important;
        width: auto !important;
    }
    """

    if is_html:
        # Check if reset already exists
        if '/* --- MOBILE RESPONSIVE RESET --- */' in content:
            return content
            
        # Insert before </head> for broad impact
        if '</head>' in content:
            content = content.replace('</head>', f'<style>{responsive_reset}</style>\n</head>')
        else:
            content = f'<style>{responsive_reset}</style>\n' + content
    else:
        # CSS file cleanup
        if '/* --- MOBILE RESPONSIVE RESET --- */' in content:
            return content
        content = responsive_reset + "\n" + content
        
    return content

# Iterate through files
updated_count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root: continue
    for file in files:
        if file in excluded_files: continue
        file_path = os.path.join(root, file)
        
        if file.endswith('.html') or file.endswith('.css'):
            is_html = file.endswith('.html')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = fix_css(content, is_html=is_html)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

print(f"Aggressively fixed {updated_count} files.")
