import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from collections import Counter
import re
from typing import List, Dict
import streamlit as st


class PDFVisualizer:
    """Create visual representations of PDF content"""
    
    def __init__(self, pdf_content: str):
        self.pdf_content = pdf_content
        self.words = self._extract_words()
    
    def _extract_words(self) -> List[str]:
        """Extract and clean words from PDF content"""
        if not self.pdf_content:
            return []
        
        # Remove page markers and clean text
        text = re.sub(r'--- Page \d+ ---', '', self.pdf_content)
        
        # Extract words (remove punctuation and numbers)
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'over', 'under', 'again', 'further',
            'then', 'once', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'can', 'may', 'might', 'must', 'shall', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her',
            'its', 'our', 'their'
        }
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        return filtered_words
    
    def create_word_frequency_chart(self, top_n: int = 20) -> go.Figure:
        """Create a word frequency bar chart"""
        if not self.words:
            fig = go.Figure()
            fig.add_annotation(text="No text data available", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        word_counts = Counter(self.words)
        top_words = word_counts.most_common(top_n)
        
        words, counts = zip(*top_words) if top_words else ([], [])
        
        fig = go.Figure(data=go.Bar(
            x=list(counts),
            y=list(words),
            orientation='h',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title=f"Top {top_n} Most Frequent Words in PDF",
            xaxis_title="Frequency",
            yaxis_title="Words",
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def create_word_cloud_data(self, max_words: int = 50) -> Dict[str, int]:
        """Create data for word cloud visualization"""
        if not self.words:
            return {}
        
        word_counts = Counter(self.words)
        return dict(word_counts.most_common(max_words))
    
    def create_text_statistics_chart(self) -> go.Figure:
        """Create text statistics visualization"""
        if not self.pdf_content:
            fig = go.Figure()
            fig.add_annotation(text="No content available", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Calculate statistics
        total_chars = len(self.pdf_content)
        total_words = len(self.words)
        sentences = len(re.findall(r'[.!?]+', self.pdf_content))
        paragraphs = len([p for p in self.pdf_content.split('\n\n') if p.strip()])
        
        # Average calculations
        avg_word_length = sum(len(word) for word in self.words) / len(self.words) if self.words else 0
        avg_sentence_length = total_words / sentences if sentences > 0 else 0
        
        categories = ['Characters', 'Words', 'Sentences', 'Paragraphs', 
                     'Avg Word Length', 'Avg Sentence Length']
        values = [total_chars, total_words, sentences, paragraphs, 
                 round(avg_word_length, 2), round(avg_sentence_length, 2)]
        
        fig = go.Figure(data=go.Bar(
            x=categories,
            y=values,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
        ))
        
        fig.update_layout(
            title="PDF Content Statistics",
            xaxis_title="Metrics",
            yaxis_title="Count",
            height=400
        )
        
        return fig
    
    def create_content_length_distribution(self, pages_content: List[Dict]) -> go.Figure:
        """Create page length distribution chart"""
        if not pages_content:
            fig = go.Figure()
            fig.add_annotation(text="No page data available", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        page_lengths = [len(page['text'].split()) for page in pages_content]
        page_numbers = [page['page_number'] for page in pages_content]
        
        fig = go.Figure(data=go.Scatter(
            x=page_numbers,
            y=page_lengths,
            mode='lines+markers',
            marker_color='blue',
            line_color='lightblue'
        ))
        
        fig.update_layout(
            title="Words per Page Distribution",
            xaxis_title="Page Number",
            yaxis_title="Word Count",
            height=400
        )
        
        return fig
    
    def display_visual_dashboard(self, pages_content: List[Dict] = None):
        """Display complete visual dashboard in Streamlit"""
        st.subheader("📊 PDF Content Visualizations")
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Word Frequency", "📊 Statistics", "📄 Page Analysis", "☁️ Word Cloud"])
        
        with tab1:
            st.subheader("Most Frequent Words")
            top_n = st.slider("Number of top words to show", 10, 50, 20)
            fig_freq = self.create_word_frequency_chart(top_n)
            st.plotly_chart(fig_freq, use_container_width=True)
        
        with tab2:
            st.subheader("Content Statistics")
            fig_stats = self.create_text_statistics_chart()
            st.plotly_chart(fig_stats, use_container_width=True)
        
        with tab3:
            if pages_content:
                st.subheader("Page-wise Analysis")
                fig_pages = self.create_content_length_distribution(pages_content)
                st.plotly_chart(fig_pages, use_container_width=True)
            else:
                st.info("Page data not available for detailed analysis")
        
        with tab4:
            st.subheader("Word Cloud Data")
            word_cloud_data = self.create_word_cloud_data()
            if word_cloud_data:
                # Display as a simple table since we can't install wordcloud
                df = pd.DataFrame(list(word_cloud_data.items()), columns=['Word', 'Frequency'])
                df = df.head(30)  # Show top 30 words
                st.dataframe(df, use_container_width=True)
                
                # Create a simple bar chart as alternative to word cloud
                fig = px.bar(df.head(15), x='Frequency', y='Word', 
                           title="Top 15 Words (Word Cloud Alternative)",
                           orientation='h')
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No word frequency data available")