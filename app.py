import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Static system prompt
system_prompt = (
    "The user will provide you with a baking recipe. Your job is to return the same content with precise high-altitude baking adjustments. Show what adjustments were made. "
    "Do not include any additional context, explanations, or clarifications. "
    "Provide only the adjusted recipe in the exact format provided by the user."
)


@app.route("/", methods=["GET", "POST"])
def main():
    altitudeAdjustment = ""
    user_recipe = ""  # Initialize an empty variable for user_recipe
    if request.method == "POST":
        user_recipe = request.form.get("user_recipe", "")  # Safely get the form data

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },  # Use the global system_prompt
                    {"role": "user", "content": user_recipe},
                ],
            )
            altitudeAdjustment = response.choices[0].message.content.strip()
        except Exception as e:
            altitudeAdjustment = f"Error: {e}"

    return render_template(
        "index.html",
        altitudeAdjustment=altitudeAdjustment,
        user_recipe=user_recipe,
    )


if __name__ == "__main__":
    app.run()
