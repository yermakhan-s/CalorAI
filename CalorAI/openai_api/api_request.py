import openai
from django.conf import settings
from .utils import calculate_request_cost_kzt
# Set your API key
openai.api_key = settings.OPENAI_API_KEY

# Example usage: Chat with GPT

def get_nutritional_info(food_description):
    # Define system and user prompts
    system_prompt = (
        "You are a nutrition expert. Given a short food description, "
        "calculate its approximate fat, protein, carbs, and calories. "
        "Respond only with the numbers for these values in the order: "
        "fat, protein, carbs, calories, separated by spaces. "
        "For example: '10 30 5 250'. "
        # "If the input is not a valid food description, reply with: 'Error'."
    )
    
    request_cost_kzt = calculate_request_cost_kzt(system_prompt, food_description)
    print(request_cost_kzt)

    # Use OpenAI's GPT model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Cost-effective and high-performing
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": food_description}
        ],
        max_tokens=50,  # Limit the response length
        temperature=0.7  # Balance between creativity and determinism
    )
    
    # Return the response content
    return response['choices'][0]['message']['content']