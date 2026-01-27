import os
import re

excluded_files = ['index.html']

def fix_css(content, is_html=True):
    # 1. Cleanup invalid 'max-max-width' if it exists from previous failures
    content = content.replace('max-max-width: 100%', 'max-width: 1200px')
    content = content.replace('max-max-width', 'max-width')
    
    # 2. Fix the broken media query markers from previous runs
    content = content.replace('/* Disabled fixed-scale query */ @media screen and (max-width:1px)', '/* Legacy Media Query Disabled */ @media screen and (max-width: 0px)')
    content = content.replace('/* Removed problematic query */ @media screen and (max-width:2500px)', '/* Legacy Media Query Disabled */ @media screen and (max-width: 0px)')
    
    # 3. New Responsive Reset Styles
    # This reset forces reasonable sizes and centering.
    responsive_reset = """
    /* --- Mobile Responsive Fix --- */
    html {
        font-size: 16px; /* Reset base scale */
    }
    body {
        max-width: 100% !important;
        width: auto !important;
        margin: 0 auto !important;
        padding: 5% !important;
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        text-align: center !important;
        word-wrap: break-word;
        overflow-x: hidden;
    }
    h1, #h1 { font-size: 2.5rem !important; padding: 20px 0 !important; margin: 10px 0 !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.75rem !important; }
    p, a, li, label, input { font-size: 1.1rem !important; }
    
    img, video, iframe {
        max-width: 100% !important;
        height: auto !important;
        display: block;
        margin: 20px auto !important;
    }
    table, form, fieldset, details {
        max-width: 100% !important;
        width: 100% !important;
        margin: 20px auto !important;
        box-sizing: border-box;
    }
    .overview-btn {
        font-size: 14px !important;
        padding: 8px 15px !important;
        top: 10px !important;
        right: 10px !important;
    }
    @media (min-width: 768px) {
        body { padding: 40px !important; max-width: 1000px !important; }
        h1, #h1 { font-size: 3.5rem !important; }
    }
    """

    # Inject the reset
    if is_html:
        # Avoid double injection
        if '/* --- Mobile Responsive Fix --- */' in content:
            return content
            
        if '<style>' in content:
            content = content.replace('</style>', f'{responsive_reset}\n</style>', 1)
        else:
            block = f'<style>{responsive_reset}</style>'
            content = content.replace('</head>', f'{block}\n</head>')
    else:
        # CSS file
        if '/* --- Mobile Responsive Fix --- */' in content:
            return content
        content = responsive_reset + "\n" + content
        
    # Also fix some common fixed-width patterns that might still be lurking
    content = re.sub(r'width\s*:\s*\d+px', 'max-width: 100%', content)
    
    return content

# Iterate through files
updated_count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root: continue
    for file in files:
        if file in excluded_files: continue
        file_path = os.path.join(root, file)
        
        if file.endswith('.html'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = fix_css(content, is_html=True)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
                
        elif file.endswith('.css'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = fix_css(content, is_html=False)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

print(f"Fixed {updated_count} files.")
