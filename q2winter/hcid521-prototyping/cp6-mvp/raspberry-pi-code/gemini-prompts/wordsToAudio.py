import base64
import os
from google import genai
from google.genai import types


def wordsToAudio(input):
    full_response = ""
    client = genai.Client(
        api_key="AIzaSyD1rgVz8vdJRIzpYOtrR6wWQmk3M1OI2iE",
    )

    files = [
        # Make the file available in local system working directory
        client.files.upload(file="file_list.txt"),
    ]
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text=input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_CIVIC_INTEGRITY",
                threshold="BLOCK_NONE",  # Block none
            ),
        ],
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            properties = {
                "response": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        properties = {
                            "word": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "wordtranslated": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "wav-path": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        },
                    ),
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text="""You are helping us create an AI powered soundboard for language learning.  This is the final part of a multi-prompt chain.  You'll receive a message in this format:

\"{ Language } : {list of words or phrases}\"

For each word or phrase, find the most appropriate .wav file in the attached \"file_list.txt\".  Please return the exact path in \"wav-path\".  Then, translate them into the language provided at the beginning of the message."""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        full_response += chunk.text
    return full_response