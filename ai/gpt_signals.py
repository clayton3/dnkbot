import openai

# Initialize OpenAI API client
openai.api_key = 'YOUR_OPENAI_API_KEY'

def gpt_generate_signal(context):
    """
    Generate a trading signal using GPT-3 based on the provided context.

    Parameters:
    - context (str): Context information for GPT-3.

    Returns:
    - signal (str): Trading signal ('buy', 'sell', or 'hold').
    """
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=context,
            max_tokens=5,
            n=1,
            stop=None,
            temperature=0.5
        )
        signal = response.choices[0].text.strip().lower()
        return signal
    except openai.error.OpenAIError as e:
        print(f"Error querying GPT: {e}")
        return None