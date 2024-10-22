#import os
#import requests
#import argparse
import litellm

from datetime import datetime


def get_svg_for_ui_component(description: str) -> str:
    """
    This function prompts GPT-4 to create the UI for a given description,
    delivering it in the form of SVG code only.

    :param description: A string describing the UI or UI component.
    :param api_key: OpenAI API key for authentication.
    :return: SVG code as a string.
    """
    prompt = f"Create an SVG representation of the following UI component: {description}. Return only the SVG code and nothing else."

    # Call the GPT-4 API
    response = litellm.completion(
            model="openai/gpt-4o",
            api_key='sk-2YfBaZ9HM-xfViulI4zJgw',
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


def save_svg_file(svg_code):
    """
    Saves the provided SVG code to a .svg file with a timestamped file name.
    
    :param svg_code: The SVG code as a string.
    """
    # Get the current date and time formatted as YYYY_MM_DD_HH_MM_SS
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_name = f"{timestamp}.svg"
    
    # Write the SVG code to the file
    with open(file_name, "w") as file:
        file.write(svg_code)
    print(f"SVG file saved as {file_name}")

# Example usage

#svg_code = """<svg width="300" height="600" xmlns="http://www.w3.org/2000/svg">
#  <!-- Background Panel -->
#  <rect x="0" y="0" width="300" height="600" fill="#f8f9fa" stroke="#d3d3d3" stroke-width="1"/>

#  <!-- Header Section -->
#  <rect x="0" y="0" width="300" height="60" fill="#ffffff"/>
#  <text x="20" y="35" font-family="Arial" font-size="18" fill="#333">Ticket Title</text>

#  <!-- Metadata Section -->
#  <text x="20" y="90" font-family="Arial" font-size="12" fill="#888">Assignee: John Doe</text>
#  <text x="20" y="110" font-family="Arial" font-size="12" fill="#888">Status: In Progress</text>
#  <text x="20" y="130" font-family="Arial" font-size="12" fill="#888">Priority: High</text>
#  <line x1="0" y1="150" x2="300" y2="150" stroke="#d3d3d3" stroke-width="1"/>

#  <!-- Description Section -->
#  <text x="20" y="180" font-family="Arial" font-size="14" fill="#333">Description:</text>
#  <rect x="20" y="200" width="260" height="100" fill="#ffffff" stroke="#d3d3d3" stroke-width="1"/>
#  <text x="25" y="220" font-family="Arial" font-size="12" fill="#666">
#    This is a brief description of the ticket...
#  </text>

#  <!-- Activity Log Section -->
#  <text x="20" y="330" font-family="Arial" font-size="14" fill="#333">Activity Log:</text>
#  <rect x="20" y="350" width="260" height="200" fill="#ffffff" stroke="#d3d3d3" stroke-width="1"/>
#  <text x="25" y="370" font-family="Arial" font-size="12" fill="#666">
#    - Updated status to 'In Progress'
#  </text>
#  <text x="25" y="390" font-family="Arial" font-size="12" fill="#666">
#    - Commented: "Let's move this forward."
#  </text>
#  <text x="25" y="410" font-family="Arial" font-size="12" fill="#666">
#    - Assigned to John Doe
#  </text>
#</svg>"""


# Example usage
if __name__ == "__main__":
    description = "simple button with rounded corners and a gradient background"
    api_key = "your-openai-api-key"  # Replace with your actual OpenAI API key

    # Retrieve the SVG code
    try:
        svg_code = get_svg_for_ui_component(description, api_key)
        print(svg_code)
        # Call the function with the SVG code
        save_svg_file(svg_code)
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
