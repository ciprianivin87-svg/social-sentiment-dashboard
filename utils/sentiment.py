from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text: str) -> dict:
    """Analisi veloce basata su regole con VADER."""
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        category = 'Positivo'
    elif compound <= -0.05:
        category = 'Negativo'
    else:
        category = 'Neutro'
        
    return {
        'compound': compound,
        'category': category
    }

def analyze_sentiment_llm(text: str, provider: str = "gemini", api_key: str = None) -> dict:
    """Analisi avanzata con API LLM (Gemini)."""
    prompt = f"Analizza il sentiment del seguente testo social e rispondi ESATTAMENTE con una sola parola tra [Positivo, Negativo, Neutro]:\n\n\"{text}\""
    
    if provider == "gemini" and api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            res_text = response.text.strip().capitalize()
            category = res_text if res_text in ['Positivo', 'Negativo', 'Neutro'] else 'Neutro'
            return {'compound': 0.0, 'category': category}
        except Exception:
            return analyze_sentiment_vader(text)
            
    return analyze_sentiment_vader(text)