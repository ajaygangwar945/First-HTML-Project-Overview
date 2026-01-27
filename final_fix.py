import os
import re

excluded_files = ['index.html']

def final_fix_content(content):
    # 1. Broadly remove ALL previous injection blocks to start fresh
    patterns_to_remove = [
        r'/\* Global Responsiveness & Centering \*/.*?(?=\n\s*</style>|\Z)',
        r'/\* --- Mobile Responsive Fix --- \*/.*?(?=\n\s*</style>|\Z)',
        r'/\* --- MOBILE RESPONSIVE RESET --- \*/.*?(?=\n\s*</style>|\Z)',
        r'/\* Legacy Media Query Disabled \*/ @media \(max-width: 0px\) \{.*?\}',
        r'/\* Legacy Query Disabled \*/ @media \(max-width: 0px\) \{.*?\}',
        r'/\* Disabled fixed-scale query \*/ @media screen and \(max-width:1px\)',
        r'/\* Removed problematic query \*/ @media screen and \(max-width:2500px\)'
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # 2. Fix the 'max-max-width' artifacts specifically
    content = content.replace('max-max-width', 'max-width')
    content = re.sub(r'@media screen and \(max-width: \d+%\)', '/* Query Disabled */ @media (max-width: 0px)', content)

    # 3. The Ultimate Clean Responsive Reset
    ultimate_reset = """
    /* --- ULTIMATE RESPONSIVE RESET --- */
    * { box-sizing: border-box !important; }
    html { font-size: 16px !important; }
    body {
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding: 5vw !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        text-align: center !important;
        word-wrap: break-word !important;
        overflow-x: hidden !important;
        background-color: #f4f4f4 !important;
        color: #333 !important;
        float: none !important;
    }
    h1, h2, h3, h4, h5, h6, #h1 { 
        margin: 0.5em 0 !important; 
        padding: 10px !important; 
        background: transparent !important; 
        color: #00264d !important;
        line-height: 1.2 !important;
    }
    h1, #h1 { font-size: 2.2rem !important; }
    h2 { font-size: 1.8rem !important; }
    p, li, label, input, select, textarea, a { 
        font-size: 1rem !important; 
        margin: 10px auto !important;
        width: auto !important;
        max-width: 100% !important;
    }
    img, video, iframe {
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 20px auto !important;
        border-radius: 8px !important;
    }
    table, form, fieldset, details {
        max-width: 100% !important;
        width: 100% !important;
        margin: 20px auto !important;
        border-collapse: collapse !important;
    }
    .overview-btn {
        position: fixed !important;
        font-size: 0.8rem !important;
        padding: 8px 15px !important;
        top: 10px !important;
        right: 10px !important;
        width: auto !important;
        z-index: 10000 !important;
    }
    @media (max-width: 600px) {
        body { padding: 15px !important; }
        h1, #h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
    }
    """

    # 4. Inject into <head> safely
    if '</head>' in content:
        content = content.replace('</head>', f'<style>{ultimate_reset}</style>\n</head>')
    else:
        # Fallback for files without proper head
        content = f'<style>{ultimate_reset}</style>\n' + content

    return content

# Run across all files
fixed_count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root: continue
    for file in files:
        if file in excluded_files: continue
        if not (file.endswith('.html') or file.endswith('.css')): continue
        
        file_path = os.path.join(root, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = final_fix_content(content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed_count += 1

print(f"Cleaned and applied Ultimate Reset to {fixed_count} files.")
