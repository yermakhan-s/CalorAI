# Exchange rate for USD to KZT (update this value as needed)
USD_TO_KZT = 470  # Example: 1 USD = 470 KZT

# OpenAI pricing for GPT-3.5-turbo (in USD)
PRICE_PER_1000_INPUT_TOKENS = 0.0015  # USD
PRICE_PER_1000_OUTPUT_TOKENS = 0.002  # USD

def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Estimate the number of tokens in the input text.
    1 token ≈ 4 characters in English (or use tiktoken for precise calculations).
    """
    return len(text) // 4  # Approximation: 4 characters per token

def calculate_request_cost_kzt(system_prompt, user_input, max_output_tokens=50):
    """
    Calculate the cost of an OpenAI request in KZT.
    """
    # Token counts
    input_tokens = count_tokens(system_prompt) + count_tokens(user_input)
    output_tokens = max_output_tokens  # Set by max_tokens in the API request
    
    # Calculate cost in USD
    input_cost_usd = (input_tokens / 1000) * PRICE_PER_1000_INPUT_TOKENS
    output_cost_usd = (output_tokens / 1000) * PRICE_PER_1000_OUTPUT_TOKENS
    total_cost_usd = input_cost_usd + output_cost_usd

    # Convert USD to KZT
    total_cost_kzt = total_cost_usd * USD_TO_KZT

    return round(total_cost_kzt, 2)