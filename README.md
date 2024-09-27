# Coding Assessment Documentation

## Table of Contents

1. [Running the Code](#running-the-code)
2. [Design Choices](#design-choices)
3. [Challenges and Solutions](#challenges-and-solutions)
4. [Future Improvements](#future-improvements)

## Running the Code

#### Steps:

1. **Create a Virtual Environment**: Open your terminal or command prompt and navigate to the project's root directory. Run the following command to create a virtual environment.

   ```bash
   python -m venv .venv
   ```

2. **Activate the Virtual Environment**: Activation will vary depending on your operating system.

   - **On Windows**:

     ```cmd
     .\venv\Scripts\activate
     ```

   - **On macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Required Packages**: Install all dependencies listed in the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

4. **Replace OPENAI API KEY**: Type in your OPEN AI API key in the `.env` file.

   ```bash
   OPENAI_API_KEY = YOUR KEY
   ```

### Running the Application

#### API

To run the API, use the following command:

```bash
uvicorn main:app --reload
```

You can reach the WebUI-Prototype via: (http://127.0.0.1:8000/)

#### Async Test-Script

To test the async Test-Script, use the following command:

```bash
python async_test.py
```

## Design Choices

### General

- I implemented a basic function for the API call, which I can use in every app route that needs it.
- In this case, I have three routes:
  - A route that renders my template
  - A route for testing via WebUI
  - A basic route that returns JSON

### Choice of FastAPI

I chose **FastAPI** for the following reasons:

- **Ease of Use**: API development with easy routing and request handling.
- **Error Handling**: Efficiently manages API errors.
- **Asynchronous Support**: Facilitates non-blocking request handling with asynchronous functions.
- **Automatic Documentation**: Generates interactive API documentation automatically using Swagger UI.

### Testing Strategy

#### Basic Functionality Testing

I implemented a `test_script.py` to test the basic functionality of the OpenAI call.

Additionally, I developed a small WebUI prototype because I prefer testing applications in realistic use case scenarios.

#### Asynchronous Load Testing

An `async_test_script.py` was developed to test how the API handles high volumes of simultaneous requests.

## Challenges and Solutions

- **Format of the Output**: I needed to ensure that the output is in the correct triplet format. Added splitting with semicolon, because it's not used often in texts. I adjusted a prompt template from LangSmith hub. Also added 3 retries in case the format is not as desired.
- **Error handling**: There a multiple errors, that can occur during runtime. I tried to add as many exceptions as possible.
- **Time and perfection**: I didn't want to overcompensate the estimated 2-hour time window. So for basic tasks, I tried to generate the code with ChatGPT or Copilot, especially the web layout. In the end, I needed to quit without perfecting it :D

## Future Improvements

- **Rate Limiting**: Implement strategies to manage OpenAI rate limits, as status code 500 indicates potential issues.
- **Testing**: Conduct more comprehensive tests, including edge cases, to enhance stability.
- **Better Output**: Improve the output format for better readability, structure, and handling in other applications.
- **Clean the code**
