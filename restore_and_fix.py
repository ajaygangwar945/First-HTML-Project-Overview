import os
import re

excluded_files = ['index.html']

def refine_content(content):
    # 1. Remove all previous various injection versions
    patterns_to_remove = [
        r'/\* --- ULTIMATE RESPONSIVE RESET --- \*/.*?(?=</style>|\Z)',
        r'/\* --- Mobile Responsive Fix --- \*/.*?(?=</style>|\Z)',
        r'/\* Global Responsiveness & Centering \*/.*?(?=</style>|\Z)',
        r'/\* Legacy Media Query Disabled \*/ @media \(max-width: 0px\) \{.*?\}',
        r'/\* Legacy Query Disabled \*/ @media \(max-width: 0px\) \{.*?\}',
        r'/\* Disabled fixed-scale query \*/ @media screen and \(max-width:1px\)',
        r'/\* Removed problematic query \*/ @media screen and \(max-width:2500px\)',
        r'<style>\s*</style>' # Clean up empty style tags left behind
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # 2. Restore fixed-scale media queries if they were disabled (but keep them "tamed")
    # Actually, the user wants the ORIGINAL styles. The 1924px query was original.
    # We will restore it but ensure it doesn't break the layout.
    content = content.replace('/* Legacy Media Query Disabled */ @media (max-width: 0px)', '@media screen and (max-width:1924px)')
    content = content.replace('/* Legacy Query Disabled */ @media (max-width: 0px)', '@media screen and (max-width:330px)')
    content = content.replace('/* Disabled fixed-scale query */ @media screen and (max-width:1px)', '@media screen and (max-width:1924px)')

    # 3. Inject the "Light Responsive Fix" (Layout Only)
    # This specifically avoids overriding font-family, color, or background.
    light_fix = """
    /* --- LIGHT RESPONSIVE FIX (Layout Only) --- */
    body {
        max-width: 1200px;
        margin: 0 auto;
        overflow-x: hidden;
        word-wrap: break-word;
    }
    img, video, iframe {
        max-width: 100% !important;
        height: auto !important;
    }
    table, form, fieldset, details {
        max-width: 100% !important;
        width: auto !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    @media (max-width: 768px) {
        /* Scale down the massive fonts relatively without changing style */
        body, h1, h2, h3, h4, h5, h6, p, a, li { 
            font-size: clamp(16px, 8vw, 60px) !important; 
        }
    }
    """

    if '</head>' in content:
        content = content.replace('</head>', f'<style>{light_fix}</style>\n</head>')
    else:
        content = f'<style>{light_fix}</style>\n' + content

    return content

# Process all files
fixed_count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root: continue
    for file in files:
        if file in excluded_files: continue
        if not file.endswith('.html'): continue # Mostly focus on HTML to preserve CSS files purely
        
        file_path = os.path.join(root, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = refine_content(content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed_count += 1

print(f"Restored and light-fixed {fixed_count} HTML files.")
