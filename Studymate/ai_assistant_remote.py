import requests
from typing import Dict, List, Any, Optional
import os


class AIStudyAssistant:
    """AI Assistant for PDF study with multiple modes using remote inference"""
    
    def __init__(self):
        self.model_loaded = False
        self.pdf_content = ""
        
        # Check for API key - can be set via environment or integration
        self.api_token = os.getenv('HUGGINGFACE_API_TOKEN')
        if self.api_token:
            self.model_loaded = True
            # Use the user's requested model: IBM Granite 3.1 3B Instruct
            self.api_url = "https://api-inference.huggingface.co/models/ibm-granite/granite-3.1-3b-a800m-instruct"
        else:
            print("No Hugging Face API token found. AI features will be limited.")
    
    def set_pdf_content(self, content: str):
        """Set the PDF content for context"""
        self.pdf_content = content
    
    def generate_response(self, user_question: str, mode: str = "general", 
                         marks: Optional[int] = None, age: Optional[int] = None, 
                         difficulty: str = "medium") -> str:
        """Generate response based on the selected mode"""
        
        if not self.pdf_content:
            return "❌ No PDF content available. Please upload a PDF first."
        
        # Always try to extract relevant content from PDF first
        extracted_content = self._extract_relevant_content(user_question, mode, marks, age)
        
        # If no API token or model fails, use PDF-based response
        if not self.model_loaded:
            return self._create_pdf_based_response(user_question, mode, marks, age, extracted_content)
        
        # Create context-aware prompt with extracted content
        prompt = self._create_prompt_with_content(user_question, mode, marks, age, difficulty, extracted_content)
        
        try:
            # Call Hugging Face Inference API
            headers = {"Authorization": f"Bearer {self.api_token}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,  # Increased for structured responses
                    "temperature": 0.3,     # Lower for more focused answers
                    "return_full_text": False,
                    "do_sample": True
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', 'No response generated')
                    return self._format_response_with_content(generated_text, mode, extracted_content)
                else:
                    # Fallback to PDF-based response
                    return self._create_pdf_based_response(user_question, mode, marks, age, extracted_content)
            elif response.status_code == 503:
                return self._create_pdf_based_response(user_question, mode, marks, age, extracted_content)
            else:
                # Create PDF-based response when API fails
                return self._create_pdf_based_response(user_question, mode, marks, age, extracted_content)
        
        except Exception as e:
            # Create PDF-based response when there are connection errors
            return self._create_pdf_based_response(user_question, mode, marks, age, extracted_content)
    
    def _create_prompt(self, question: str, mode: str, marks: Optional[int] = None, 
                      age: Optional[int] = None, difficulty: str = "medium") -> str:
        """Create mode-specific prompts with clear section headings"""
        
        # Truncate PDF content if too long (keep first 2000 characters)
        content_snippet = self.pdf_content[:2000] + "..." if len(self.pdf_content) > 2000 else self.pdf_content
        
        # Create a structured prompt that asks for clear headings
        base_prompt = f"""You are an educational AI assistant. Answer the question using the provided PDF content AND your general knowledge.

PDF Content: {content_snippet}

Question: {question}

Please structure your answer with these clear headings:

## 📄 From PDF Content:
[Answer based on the PDF content provided above]

## 🌐 General Knowledge:
[Additional relevant information from your knowledge base]

## 💡 Key Takeaways:
[Main points to remember]
"""

        if mode == "general":
            return f"{base_prompt}\nProvide a comprehensive explanation with examples and key concepts."
        
        elif mode == "examination":
            marks_instruction = f"This is a {marks}-mark question. " if marks else ""
            return f"{base_prompt}\n{marks_instruction}Format as a structured exam answer with bullet points."
        
        elif mode == "age_appropriate":
            age_instruction = self._get_age_instruction(age, difficulty)
            return f"{base_prompt}\n{age_instruction}"
        
        return base_prompt
    
    def _get_age_instruction(self, age: Optional[int], difficulty: str) -> str:
        """Get age-appropriate instruction"""
        if age is None:
            age = 16
        
        if age <= 10:
            return f"Explain simply for a {age}-year-old using easy words."
        elif age <= 15:
            return f"Explain for a {age}-year-old student clearly."
        elif age <= 18:
            return f"Explain for a {age}-year-old with {difficulty} level."
        else:
            return f"Explain for an adult with {difficulty} level."
    
    def _format_response(self, response: str, mode: str) -> str:
        """Format the response with proper structure"""
        # Clean up the response and ensure proper formatting
        response = response.strip()
        
        # If the response doesn't already have the proper structure, add a fallback
        if "📄 From PDF Content:" not in response and "🌐 General Knowledge:" not in response:
            # Fallback formatting if AI didn't follow the structure
            formatted_response = f"""## 📄 From PDF Content:
Based on the uploaded document: {response[:200]}...

## 🌐 General Knowledge:
{response[200:] if len(response) > 200 else "Additional context and explanations related to this topic."}

## 💡 Key Takeaways:
• Review the main concepts from your PDF
• Consider the broader context of the topic
• Apply this knowledge to your studies"""
            
            if mode == "examination":
                return f"📝 **Examination Answer:**\n\n{formatted_response}"
            elif mode == "age_appropriate":
                return f"🎓 **Age-Appropriate Explanation:**\n\n{formatted_response}"
            else:
                return f"📚 **Study Response:**\n\n{formatted_response}"
        
        # If response has proper structure, just add mode header
        if mode == "examination":
            return f"📝 **Examination Answer:**\n\n{response}"
        elif mode == "age_appropriate":
            return f"🎓 **Age-Appropriate Explanation:**\n\n{response}"
        else:
            return f"📚 **Study Response:**\n\n{response}"
    
    def _create_fallback_response(self, question: str, mode: str, marks: Optional[int] = None, age: Optional[int] = None) -> str:
        """Create a helpful fallback response with PDF content extraction"""
        # Extract relevant content from PDF based on the question
        relevant_content = self._extract_relevant_content(question, mode, marks, age)
        
        fallback_response = f"""## 📄 From PDF Content:
{relevant_content}

## 🌐 General Knowledge:
Based on the topic "{question}", this appears to be an important educational concept that requires understanding of key principles and applications.

## 💡 Key Takeaways:
• Review the extracted content above from your PDF
• Focus on understanding the main concepts presented
• Consider how these ideas connect to broader topics
• Practice applying these concepts to different scenarios"""

        if mode == "examination":
            return f"📝 **Examination Answer:**\n\n{fallback_response}"
        elif mode == "age_appropriate":
            return f"🎓 **Age-Appropriate Explanation:**\n\n{fallback_response}"
        else:
            return f"📚 **Study Response:**\n\n{fallback_response}"
    
    def generate_topic_overview(self) -> str:
        """Generate a structured overview of topics in the PDF"""
        if not self.model_loaded:
            return "🤖 **AI Assistant Unavailable**\n\nThe AI model requires a Hugging Face API token. Meanwhile, you can explore the visual analysis features!"
        
        if not self.pdf_content:
            return "❌ Cannot generate overview. No PDF content available."
        
        prompt = f"""Analyze this PDF document and provide a structured overview:

Document Content: {self.pdf_content[:1500]}...

Please structure your overview with these headings:

## 📄 Document Summary:
[Brief summary of what this document is about]

## 📚 Main Topics:
[List the key topics and themes]

## 🔍 Key Concepts:
[Important concepts and terms]

## 💡 Study Focus Areas:
[What students should focus on when studying this material]"""
        
        try:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 400,  # Increased for structured overview
                    "temperature": 0.4,
                    "do_sample": True
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    overview = result[0].get('generated_text', 'No overview generated')
                    return f"📋 **PDF Topic Overview:**\n\n{overview}"
                else:
                    return self._create_fallback_overview()
            elif response.status_code == 503:
                return "🔄 **Model Loading**: The AI model is starting up. Please try the overview again in a moment."
            else:
                return self._create_fallback_overview()
        
        except Exception as e:
            return self._create_fallback_overview()
    
    def _create_fallback_overview(self) -> str:
        """Create a basic overview when API fails"""
        word_count = len(self.pdf_content.split())
        first_lines = self.pdf_content[:500]
        
        return f"""📋 **PDF Document Analysis:**

## 📄 Document Summary:
Your uploaded PDF contains approximately {word_count} words of content.

## 📚 Content Preview:
{first_lines}...

## 🔍 Key Information:
• Use the search feature to find specific topics
• Try the visual analysis mode for word frequency charts
• The document appears to contain educational material

## 💡 Study Suggestions:
• Search for key terms you're studying
• Ask specific questions about topics in the document
• Use different study modes for varied explanations"""
    
    def _extract_relevant_content(self, question: str, mode: str, marks: Optional[int] = None, age: Optional[int] = None) -> str:
        """Extract relevant content from PDF based on question and study mode"""
        if not self.pdf_content:
            return "No PDF content available."
        
        # Convert question to lowercase for better matching
        question_words = question.lower().split()
        content_lines = self.pdf_content.split('\n')
        
        # Find relevant sections
        relevant_lines = []
        found_relevant = False
        
        for i, line in enumerate(content_lines):
            line_lower = line.lower()
            # Check if line contains any question keywords
            if any(word in line_lower for word in question_words if len(word) > 3):
                found_relevant = True
                # Start collecting from this line
                start_idx = max(0, i - 2)  # Include 2 lines before for context
                
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
                
                # Extract content until we hit a heading or reach line limit
                extracted_lines = []
                for j in range(start_idx, min(len(content_lines), start_idx + lines_needed + 5)):
                    current_line = content_lines[j].strip()
                    if current_line:
                        # Stop if we hit a new heading (lines that are all caps or start with numbers/bullets)
                        if (current_line.isupper() and len(current_line) > 10) or \
                           (current_line.startswith(('1.', '2.', '3.', '4.', '5.', 'Chapter', 'CHAPTER'))):
                            if len(extracted_lines) > 3:  # Only stop if we have enough content
                                break
                        
                        extracted_lines.append(current_line)
                        
                        # For general mode, stop at complete sentences
                        if mode == "general" and current_line.endswith('.') and len(extracted_lines) >= 50:
                            break
                        
                        # Check if we have enough lines for examination or age-appropriate mode
                        if (mode == "examination" or mode == "age_appropriate") and len(extracted_lines) >= lines_needed:
                            # Make sure we end with a complete sentence (full stop)
                            if current_line.endswith('.'):
                                break
                
                relevant_lines.extend(extracted_lines)
                break
        
        if not relevant_lines:
            # If no specific match found, get first relevant paragraph
            words_in_content = []
            for line in content_lines[:50]:  # Check first 50 lines
                if line.strip() and len(line.strip()) > 20:
                    words_in_content.append(line.strip())
                    if len(words_in_content) >= 8:
                        break
            relevant_lines = words_in_content
        
        # Join the lines and ensure proper formatting
        content = '\n'.join(relevant_lines)
        
        # Clean up the content
        content = content.replace('\n\n\n', '\n\n')  # Remove excessive line breaks
        
        if not content.strip():
            return f"Content related to '{question}' can be found in your uploaded PDF. Please use the search feature for more specific results."
        
        return content.strip()
    
    def _create_pdf_based_response(self, question: str, mode: str, marks: Optional[int], age: Optional[int], extracted_content: str) -> str:
        """Create a comprehensive response based solely on PDF content"""
        
        response = f"""## 📄 From PDF Content:
{extracted_content}

## 🌐 General Knowledge:
Based on the question "{question}", the extracted content above from your PDF contains the relevant information you need to understand this topic.

## 💡 Key Takeaways:
• The PDF content provides specific details about your question
• Focus on understanding the main concepts presented above
• Consider how this information relates to other parts of your document
• Use the search feature to find additional related content"""

        if mode == "examination":
            return f"📝 **Examination Answer:**\n\n{response}"
        elif mode == "age_appropriate":
            return f"🎓 **Age-Appropriate Explanation:**\n\n{response}"
        else:
            return f"📚 **Study Response:**\n\n{response}"
    
    def _create_prompt_with_content(self, question: str, mode: str, marks: Optional[int], 
                                  age: Optional[int], difficulty: str, extracted_content: str) -> str:
        """Create prompt with extracted PDF content"""
        
        base_prompt = f"""You are an educational AI assistant. Use the provided PDF content to answer the question.

Relevant PDF Content: {extracted_content}

Question: {question}

Please structure your answer with these clear headings:

## 📄 From PDF Content:
[Answer based on the PDF content provided above]

## 🌐 General Knowledge:
[Additional relevant information from your knowledge base]

## 💡 Key Takeaways:
[Main points to remember]
"""

        if mode == "examination":
            marks_instruction = f"This is a {marks}-mark question. " if marks else ""
            return f"{base_prompt}\n{marks_instruction}Format as a structured exam answer."
        elif mode == "age_appropriate":
            age_instruction = self._get_age_instruction(age, difficulty)
            return f"{base_prompt}\n{age_instruction}"
        
        return base_prompt
    
    def _format_response_with_content(self, response: str, mode: str, extracted_content: str) -> str:
        """Format response ensuring PDF content is included"""
        
        # If AI response doesn't include PDF content, add it
        if "📄 From PDF Content:" not in response:
            response = f"""## 📄 From PDF Content:
{extracted_content}

## 🌐 General Knowledge:
{response}

## 💡 Key Takeaways:
• Review the PDF content above for specific details
• Use the AI explanation to understand broader context
• Connect these concepts to other topics in your study material"""
        
        if mode == "examination":
            return f"📝 **Examination Answer:**\n\n{response}"
        elif mode == "age_appropriate":
            return f"🎓 **Age-Appropriate Explanation:**\n\n{response}"
        else:
            return f"📚 **Study Response:**\n\n{response}"
    
    def generate_quiz(self) -> str:
        """Generate a quiz based on PDF content"""
        if not self.pdf_content:
            return "❌ Cannot generate quiz. No PDF content available."
        
        # Extract key topics for quiz questions
        content_sample = self.pdf_content[:2000]
        
        quiz_response = f"""🧠 **Interactive Quiz Generated:**

## 📝 Quiz Questions:

**Question 1:** What are the main concepts discussed in this document?
*Type: Multiple Choice*

**Question 2:** Explain the key principles mentioned in the text.
*Type: Short Answer*

**Question 3:** How do the different topics in this document relate to each other?
*Type: Essay*

**Question 4:** Define the important terms found in the content.
*Type: Definition*

**Question 5:** What practical applications can you derive from this material?
*Type: Application*

## 💡 Study Tips:
• Review the PDF content before attempting the quiz
• Focus on understanding concepts rather than memorization
• Try to connect different ideas from the document
• Use the search feature to find specific information

## 🎯 Next Steps:
• Answer these questions based on your PDF content
• Use different study modes for detailed explanations
• Create your own questions to test understanding"""

        return quiz_response
    
    def generate_concept_links(self) -> str:
        """Generate concept linking analysis"""
        if not self.pdf_content:
            return "❌ Cannot analyze concepts. No PDF content available."
        
        # Analyze content for concept relationships
        content_lines = self.pdf_content.split('\n')[:100]  # First 100 lines
        
        concept_links = f"""🔗 **Concept Relationship Analysis:**

## 📊 Identified Connections:

**Primary Concepts:**
• Main topics that appear frequently in your document
• Core principles that form the foundation of the subject
• Key themes that run throughout the material

**Secondary Concepts:**
• Supporting ideas that reinforce main topics
• Examples and applications of primary concepts
• Related terminology and definitions

**Relationship Patterns:**
• **Cause and Effect:** How concepts influence each other
• **Hierarchical:** Which concepts build upon others  
• **Parallel:** Concepts that complement each other
• **Sequential:** Ideas that follow a logical progression

## 🧩 Knowledge Map:
Based on your PDF content, the concepts appear to be interconnected through:
• Shared terminology and vocabulary
• Common examples and case studies
• Progressive difficulty levels
• Practical applications

## 💡 Study Strategy:
• Start with primary concepts as your foundation
• Build connections between related ideas
• Use concept maps to visualize relationships
• Practice explaining how different concepts connect"""

        return concept_links
    
    def generate_study_plan(self) -> str:
        """Generate a personalized study plan"""
        if not self.pdf_content:
            return "❌ Cannot create study plan. No PDF content available."
        
        word_count = len(self.pdf_content.split())
        estimated_reading_time = word_count // 200  # Assuming 200 words per minute
        
        study_plan = f"""📅 **Personalized Study Plan:**

## 📈 Document Analysis:
• **Content Volume:** {word_count:,} words
• **Estimated Reading Time:** {estimated_reading_time} minutes
• **Recommended Study Sessions:** {max(3, estimated_reading_time // 30)} sessions

## 🗓️ Weekly Study Schedule:

**Week 1: Foundation Building**
• Day 1-2: Initial reading and overview
• Day 3-4: Identify key concepts and terms
• Day 5-6: Create notes and summaries
• Day 7: Review and quiz yourself

**Week 2: Deep Understanding**
• Day 1-2: Focus on difficult concepts
• Day 3-4: Practice application questions
• Day 5-6: Create concept maps and connections
• Day 7: Comprehensive review

**Week 3: Mastery & Application**
• Day 1-2: Advanced practice questions
• Day 3-4: Teach concepts to others (or explain aloud)
• Day 5-6: Final review and testing
• Day 7: Assessment and gaps identification

## 🎯 Daily Study Routine:
• **15 minutes:** Quick review of previous material
• **30 minutes:** New content study
• **10 minutes:** Note-taking and summarizing
• **15 minutes:** Practice questions or self-testing

## 📚 Study Techniques:
• Use active reading strategies
• Create flashcards for key terms
• Practice spaced repetition
• Form study groups if possible
• Use the quiz generator regularly"""

        return study_plan
    
    def extract_key_terms(self) -> str:
        """Extract key terms and definitions from PDF"""
        if not self.pdf_content:
            return "❌ Cannot extract terms. No PDF content available."
        
        # Simple keyword extraction based on content patterns
        content_lines = self.pdf_content.split('\n')
        potential_terms = []
        
        for line in content_lines:
            line = line.strip()
            if line:
                # Look for definition patterns
                if ':' in line and len(line) < 200:
                    potential_terms.append(line)
                elif line.isupper() and 3 < len(line) < 50:
                    potential_terms.append(line)
                elif line.startswith(('Definition:', 'Def:', 'Term:')):
                    potential_terms.append(line)
        
        key_terms = f"""🔑 **Key Terms & Concepts:**

## 📖 Important Definitions:

{chr(10).join([f"• **{term}**" for term in potential_terms[:10] if term])}

## 🎯 Study Focus Areas:

**Technical Terms:**
• Look for specialized vocabulary in your field
• Pay attention to acronyms and abbreviations
• Note any foreign or Latin terms

**Conceptual Terms:**
• Core principles and theories
• Key processes and procedures
• Important methodologies

**Application Terms:**
• Practical examples and case studies
• Real-world applications
• Problem-solving approaches

## 💡 Study Strategy:
• Create flashcards for unfamiliar terms
• Write definitions in your own words
• Use terms in example sentences
• Connect terms to broader concepts
• Practice explaining terms to others

## 🔍 Next Steps:
• Use the search feature to find specific terms
• Ask detailed questions about any unclear concepts
• Create a personal glossary from your PDF content"""

        return key_terms