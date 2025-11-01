# System prompts 
SYSTEM_SUMMARIZER = """
You are a helpful AI assistant that summarizes long text into concise, readable summaries.
Focus on clarity, simplicity, and key takeaways.
"""

USER_SUMMARY_TEMPLATE = """
Summarize the following text in a structured format:

TEXT:
{text}

FORMAT YOUR RESPONSE AS:
## Summary
[3-4 sentence summary of the main points]

## TL;DR
[One concise sentence]

## Quiz Questions
1. [Question about main concept]
2. [Question about key detail]
3. [Question about application/implication]
"""
