import openai

def gpt_generate_signal(context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": context}]
        )
        signal = response['choices'][0]['message']['content']
        print(f"Usage: {response['usage']}")  # Monitor token usage
        return signal.lower().strip()
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Try again later.")
        return "error"
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return "error"
