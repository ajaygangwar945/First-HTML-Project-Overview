import os
import re

# Exclude the new index.html (the overview)
excluded_files = ['index.html']

def normalize_css(content, is_html=True):
    # Responsive styles to be injected
    resp_styles = """
    /* Global Responsiveness & Centering */
    body {
        max-width: 1200px;
        margin: 0 auto !important;
        padding: 2.5vw !important;
        line-height: 1.6;
        float: none !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    img, video, iframe {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 20px auto;
        border-radius: 8px;
    }
    table, form, fieldset, details {
        max-width: 100% !important;
        width: auto !important;
        margin: 40px auto !important;
        float: none !important;
        border-collapse: collapse;
    }
    input, select, textarea {
        max-width: 100%;
        box-sizing: border-box;
    }
    """

    if is_html:
        # Check if <style> exists
        if '<style>' in content:
            # Inject before FIRST </style>
            content = content.replace('</style>', f'{resp_styles}\n</style>', 1)
        else:
            # Inject new <style> block before </head>
            style_block = f'<style>{resp_styles}</style>\n'
            content = content.replace('</head>', f'{style_block}</head>')
    else:
        # It's a .css file, append to top or bottom
        content = resp_styles + "\n" + content

    # Clean up the problematic 1924px media query if it exists
    # We'll comment it out to neutralize it completely
    content = content.replace('@media screen and (max-width:1924px)', '/* Disabled fixed-scale query */ @media screen and (max-width:1px)')
    
    # Also handle some common fixed widths in the project
    content = re.sub(r'width\s*:\s*\d+px', 'max-width: 100%', content)
    
    return content

# Iterate through files
updated_files = []
for root, dirs, files in os.walk('.'):
    # Skip .git or other system folders
    if '.git' in root or '.gemini' in root:
        continue
        
    for file in files:
        if file in excluded_files:
            continue
            
        file_path = os.path.join(root, file)
        
        if file.endswith('.html'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = normalize_css(content, is_html=True)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files.append(file_path)
                
        elif file.endswith('.css'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = normalize_css(content, is_html=False)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files.append(file_path)

print(f"Normalized {len(updated_files)} files.")
for f in updated_files:
    print(f" - {f}")
