from openai import OpenAI
from prompts import SYSTEM_SUMMARIZER, USER_SUMMARY_TEMPLATE

def generate_summary(text,user_api_key = None):
  """Takes input text, call openai api, generate summary + quiz"""

  # --- Mock Mode for users without an API key ---
  if not user_api_key:
      return (
          "### Summary:\n"
          "This is a **demo summary** generated in Mock Mode.\n\n"
          "### Quiz Questions:\n"
          "1. What was the main topic of the text?\n"
          "2. What are the key takeaways?\n\n"
          "### TL;DR:\n"
          "Mock summary preview. Add your API key to generate real summaries!"
      ), 0

  try:
    client = OpenAI(api_key = user_api_key)
    user_prompt = USER_SUMMARY_TEMPLATE.format(text = text)

    response = client.chat.completions.create(
      model = "gpt-4o-mini",
      messages=[{'role':'system', 'content':SYSTEM_SUMMARIZER},
                {'role':'user','content':user_prompt}],
      temperature=0.7,
      max_completion_tokens=700
    )

    summary = response.choices[0].message.content.strip()

    usage = response.usage

    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens

    input_cost = (input_tokens/1000)*.00015
    output_cost = (output_tokens/1000)*.0006

    total_cost = input_cost + output_cost

    return summary, total_cost
  
  except Exception as e:
    error_msg = f"❌ Error: {str(e)}\n\nPlease check:\n- Your API key is valid\n- You have credits in your account"
    return error_msg, 0
     
