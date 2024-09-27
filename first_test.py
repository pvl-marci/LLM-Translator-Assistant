from openai import OpenAI

client = OpenAI()


def rewrite_text(text_to_rewrite):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """Act as a grammar corrector. Reply to each message only with a list of triplets: wrong sentence, corrected sentence, and type of error.

Strictly follow these rules:

- Correct spelling, grammar and punctuation

- ALWAYS detect and maintain the original language of the text

- NEVER surround the rewritten text with quotes

- Don't replace urls with markdown links

- Don't change emojis




Text to rewrite:""",
            },
            {"role": "user", "content": text_to_rewrite},
            {
                "role": "assistant",
                "content": "List of triplets:",
            },
        ],
    )
    print(response.choices[0].message.content)


# Main Function
def Main():
    rewrite_text(
        "Yesterday I go to the store and buy some groceries. The cashier was really nice and he give me a discount on my total. I was happy, but I forgot to bought eggs. So, I go back to the store later and they was out of stock. It was a bit disappointing."
    )


# App Starting Point
if __name__ == "__main__":
    Main()
