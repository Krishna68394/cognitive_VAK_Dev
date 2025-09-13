import pdfplumber
import pypdf
from typing import List, Dict, Any, Optional
import re


class PDFProcessor:
    """Handles PDF processing and text extraction"""
    
    def __init__(self):
        self.pdf_content = ""
        self.pages_content = []
        self.metadata = {}
    
    def extract_text_from_pdf(self, pdf_file) -> Dict[str, Any]:
        """Extract text from PDF file using pdfplumber for better formatting"""
        try:
            self.pages_content = []
            full_text = ""
            
            with pdfplumber.open(pdf_file) as pdf:
                self.metadata = {
                    'num_pages': len(pdf.pages),
                    'title': getattr(pdf.metadata, 'title', 'Unknown'),
                    'author': getattr(pdf.metadata, 'author', 'Unknown'),
                    'creator': getattr(pdf.metadata, 'creator', 'Unknown')
                }
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        cleaned_text = self.clean_extracted_text(page_text)
                        self.pages_content.append({
                            'page_number': page_num + 1,
                            'text': cleaned_text
                        })
                        full_text += f"\n--- Page {page_num + 1} ---\n{cleaned_text}\n"
            
            self.pdf_content = full_text
            
            return {
                'success': True,
                'text': full_text,
                'pages': self.pages_content,
                'metadata': self.metadata
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'pages': [],
                'metadata': {}
            }
    
    def clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove null characters
        text = text.replace('\x00', '')
        
        # Handle (cid:x) encoding issues
        text = re.sub(r'\(cid:\d+\)', '', text)
        
        # Remove excessive newlines but preserve paragraph breaks
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        return text.strip()
    
    def get_pdf_summary(self) -> str:
        """Generate a basic summary of the PDF content"""
        if not self.pdf_content:
            return "No PDF content available"
        
        word_count = len(self.pdf_content.split())
        char_count = len(self.pdf_content)
        
        return f"""
        📄 PDF Summary:
        - Total Pages: {self.metadata.get('num_pages', 0)}
        - Word Count: {word_count:,}
        - Character Count: {char_count:,}
        - Title: {self.metadata.get('title', 'Unknown')}
        - Author: {self.metadata.get('author', 'Unknown')}
        """
    
    def search_in_pdf(self, query: str) -> List[Dict]:
        """Search for specific text in the PDF"""
        results = []
        query_lower = query.lower()
        
        for page in self.pages_content:
            page_text = page['text'].lower()
            if query_lower in page_text:
                # Find the context around the match
                start_idx = page_text.find(query_lower)
                context_start = max(0, start_idx - 100)
                context_end = min(len(page_text), start_idx + len(query) + 100)
                context = page['text'][context_start:context_end]
                
                results.append({
                    'page_number': page['page_number'],
                    'context': context,
                    'match_position': start_idx
                })
        
        return results
    
    def get_expanded_content(self, page_number: int, context: str, mode: str = "general", marks: Optional[int] = None, age: Optional[int] = None) -> str:
        """Get expanded content BELOW the search result with proper length based on study mode"""
        if page_number <= 0 or page_number > len(self.pages_content):
            return context
        
        # Find the page content
        page_content = ""
        for page in self.pages_content:
            if page['page_number'] == page_number:
                page_content = page['text']
                break
        
        if not page_content:
            return context
        
        content_lines = page_content.split('\n')
        
        # Find the line containing the context
        context_line_idx = -1
        for i, line in enumerate(content_lines):
            if context.strip() in line:
                context_line_idx = i
                break
        
        if context_line_idx == -1:
            return context
        
        # Determine how many lines to extract based on mode and marks/age
        if mode == "examination" and marks:
            if marks <= 5:
                lines_needed = 10  # 1-5 marks: 10 lines
            elif marks <= 10:
                lines_needed = 20  # 5-10 marks: 20 lines
            elif marks <= 15:
                lines_needed = 30  # 10-15 marks: 30 lines
            else:
                lines_needed = 30  # 15+ marks: still 30 lines max
        elif mode == "age_appropriate" and age:
            if age <= 5:
                lines_needed = 10  # 1-5 age: 10 lines
            elif age <= 10:
                lines_needed = 20  # 5-10 age: 20 lines
            elif age <= 15:
                lines_needed = 30  # 10-15 age: 30 lines
            else:
                lines_needed = 20  # 15+ age: 20 lines
        elif mode == "general":
            lines_needed = 50  # Updated to 50 lines for general learning
        else:
            lines_needed = 10  # Default fallback
        
        # Extract content BELOW the searched topic (not around it)
        start_idx = context_line_idx + 1  # Start from the line after the search result
        end_idx = min(len(content_lines), start_idx + lines_needed + 10)  # Extra buffer to find complete sentences
        
        expanded_lines = []
        for i in range(start_idx, end_idx):
            line = content_lines[i].strip()
            if line:
                # Stop if we hit a new major heading
                if line.isupper() and len(line) > 10:
                    break
                # Stop if we hit numbered sections or chapters
                if line.startswith(('1.', '2.', '3.', '4.', '5.', 'Chapter', 'CHAPTER')):
                    break
                
                expanded_lines.append(line)
                
                # For exam and age modes, stop when we have enough lines ending with full stop
                if (mode == "examination" or mode == "age_appropriate") and len(expanded_lines) >= lines_needed:
                    if line.endswith('.'):
                        break
                
                # For general mode, stop at complete sentences after minimum lines
                if mode == "general" and line.endswith('.') and len(expanded_lines) >= 50:
                    break
        
        # If we don't have enough content below, include the original context
        if len(expanded_lines) < 3:
            return context + "\n\n" + '\n'.join(expanded_lines)
        
        return '\n'.join(expanded_lines)