import zipfile
import xml.etree.ElementTree as ET
import os

def get_docx_text(path):
    """
    Extract text from docx file without external dependencies
    """
    try:
        with zipfile.ZipFile(path) as zf:
            xml_content = zf.read('word/document.xml')
        
        root = ET.fromstring(xml_content)
        
        # Namespaces are important in DOCX XML
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        text = []
        for p in root.findall('.//w:p', ns):
            paragraph_text = ""
            for t in p.findall('.//w:t', ns):
                if t.text:
                    paragraph_text += t.text
            if paragraph_text:
                text.append(paragraph_text)
        
        return "\n".join(text)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    path = r"C:\Users\Admin\Downloads\LoginSentinel-Infosec.docx"
    print(get_docx_text(path))
