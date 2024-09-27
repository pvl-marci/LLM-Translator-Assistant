from fastapi import (
    FastAPI,
    Request,
    Form,
)
from openai import AsyncOpenAI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List, Tuple
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Fetch the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client (asynchronous version)
client = AsyncOpenAI()

# Initialize FastAPI instance
app = FastAPI()

# Specify the directory for HTML templates (e.g., forms and results page)
templates = Jinja2Templates(directory="templates")


# API endpoints


# GET endpoint to render the form.html
@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    """
    GET endpoint that renders the form where users can input text for grammar checking.
    It serves the HTML form from the "form.html" template.
    """
    return templates.TemplateResponse("form.html", {"request": request})


# POST endpoint for the grammar checker UI
@app.post("/grammar-check-template")
async def post_endpoint_template(
    request: Request, text_to_rewrite: str = Form(...)
) -> str:
    """
    POST endpoint to process the user's input via the WebUI and get grammar corrections using OpenAI.
    """
    try:
        # Get grammar correction and triplets from OpenAI API
        corrected_text, triplets = await get_grammar_correction_from_openai(
            text_to_rewrite
        )

        # Render the response with the original text, corrected text, and the triplets (errors and corrections)
        return templates.TemplateResponse(
            "form.html",
            {
                "request": request,
                "original_text": text_to_rewrite,
                "corrected_text": corrected_text,
                "triplets": triplets,
            },
        )

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        return templates.TemplateResponse(
            "form.html", {"request": request, "error_message": error_message}
        )


# POST endpoint for the grammar checker API (used for the stress test)
@app.post("/grammar-check-api")
async def post_endpoint_api(
    request: Request, text_to_rewrite: str = Form(...)
) -> JSONResponse:
    """
    POST endpoint to process a input and get grammar corrections using OpenAI.
    It returns the corrected text and error triplets as JSON.
    """
    try:
        # Get grammar correction and triplets from OpenAI API
        corrected_text, triplets = await get_grammar_correction_from_openai(
            text_to_rewrite
        )

        # Return a JSON response with the original text, corrected text, and triplets
        return JSONResponse(
            content={
                "original_text": text_to_rewrite,
                "corrected_text": corrected_text,
                "triplets": triplets,
            }
        )

    except Exception as e:
        # Handle any exceptions and return an error message as JSON
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"}, status_code=500
        )


# Helper function to interact with OpenAI API with a retry mechanism
async def get_grammar_correction_from_openai(
    text: str, max_retries: int = 3
) -> Tuple[str, List[Tuple[str, str, str]]]:
    """
    Function to interact with OpenAI API and return the corrected text and triplets.
    Retries up to `max_retries` times if the format of the response is incorrect. Currently a problem with rate limiting.

    Args:
    - text (str): The text to be grammar-checked.
    - max_retries (int): Maximum number of retries if the response format is incorrect.

    Returns:
    - Tuple[str, List[Tuple[str, str, str]]]: Corrected text and a list of triplets (wrong sentence, corrected sentence, type of error).
    """
    retries = 0

    while retries < max_retries:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Act as a grammar corrector. Reply to each message only with a list of triplets: wrong sentence; corrected sentence; and type of error.
                    Strictly follow these rules:
                    - Correct spelling, grammar and punctuation
                    - Give a detailed type of error for each sentence
                    - ALWAYS detect and maintain the original language of the text
                    - NEVER surround the rewritten text with quotes or brackets
                    - Don't replace URLs with markdown links
                    - Don't change emojis
                    """,
                },
                {"role": "user", "content": text},
            ],
        )

        # Extract the corrected text from the OpenAI API response
        corrected_text = response.choices[0].message.content

        # Extract the triplets (wrong sentence, corrected sentence, type of error) from the response
        triplets = extract_triplets(corrected_text)

        # Check if triplets were successfully extracted
        if triplets:
            return corrected_text, triplets
        else:
            retries += 1
            print(f"Retrying... attempt {retries}/{max_retries}")

    raise ValueError("Failed to get a valid response from OpenAI after 3 attempts.")


# Helper function to extract triplets from the OpenAI response content
def extract_triplets(content: str) -> List[Tuple[str, str, str]]:
    """
    Helper function to extract triplets (wrong sentence, corrected sentence, type of error)
    from the OpenAI response content.
    """
    try:
        triplets = []
        lines = content.split("\n")
        for line in lines:
            parts = line.split(
                ";"
            )  # Split the line into parts using the semicolon because it is not commonly used. Still thinking of a better approach...
            if len(parts) == 3:
                triplets.append(tuple(parts))  # Convert the list of parts into a tuple
        return triplets
    except Exception as e:
        print(f"An error occurred during triplet extraction: {str(e)}")
        return []
