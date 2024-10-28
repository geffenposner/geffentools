import os
from datetime import datetime
#import requests
#import argparse
import litellm

from pathlib import Path
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError



def get_svg_for_ui_component(description: str) -> str:
    """
    This function prompts GPT-4 to create the UI for a given description,
    delivering it in the form of SVG code only.

    :param description: A string describing the UI or UI component.
    :param api_key: OpenAI API key for authentication.
    :return: SVG code as a string.
    """
    prompt = f"Create an SVG representation of the following UI component: {description}. Return only the SVG code and nothing else."


    openai_api_key = os.environ['OPEN_AI_API_KEY_1']
    if not openai_api_key:
        print("OPEN_AI_API_KEY_1 environment variable is not set.")
        return

    # Call the GPT-4 API
    response = litellm.completion(
            model="openai/gpt-4o",
            api_key=openai_api_key,
            base_url='https://llm-proxy.kubiya.ai',
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

    # Extract and return the SVG code from the response
    svg_code = response['choices'][0]['message']['content'].strip()
    return svg_code


def save_svg_file(svg_code) -> Path:
    """
    Saves the provided SVG code to a .svg file with a timestamped file name.
    
    :param svg_code: The SVG code as a string.
    """
    # Get the current date and time formatted as YYYY_MM_DD_HH_MM_SS
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_name = f"{timestamp}.svg"
    
    file_path = Path(file_name)
    file_path.write_text(svg_code)
    print(f"SVG file saved as {file_name}")
    return file_path


def send_slack_file_to_thread(token, channel_id, thread_ts, file_path, initial_comment):
    client = WebClient(token=token)
    try:
        client.chat_meMessage(
            channel=channel_id,
            text="Here is the SVG code for the UI component"
        )
        response = client.files_upload_v2(
            channel=channel_id,
            file=file_path,
            initial_comment=initial_comment,
            thread_ts=thread_ts,
        )
        print(f"File uploaded to Slack thread: {response}")
        return response
    except SlackApiError as e:
        print(f"Error sending file to Slack thread: {e}")
        raise


# Example usage
if __name__ == "__main__":
    description = "simple button with rounded corners and a gradient background"

    try:
        token = os.environ['SLACK_API_TOKEN']
        channel_id = os.environ['SLACK_CHANNEL_ID']
        thread_ts = os.environ['SLACK_THREAD_TS']
    except Exception as e:
        print(f"Error: {e}")

    # Retrieve the SVG code
    try:
        svg_code = get_svg_for_ui_component(description)
        print(svg_code)

        if not svg_code:
            print("No SVG code returned from GPT-4")
        
        else:
            # Call the function with the SVG code
            file_path = save_svg_file(svg_code)
            comment = "Here is the SVG code for the UI component"
            send_slack_file_to_thread(token, channel_id, thread_ts, file_path.resolve(), comment)
    except Exception as e:
        print(f"Error: {e}")





#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description="Print hello {name}!")
#    parser.add_argument("name", help="Name to say hello to")

#    # Parse command-line arguments
#    args = parser.parse_args()

#    # Get coordinates for the given city
#    name = args.name

#    hello_world(name)
