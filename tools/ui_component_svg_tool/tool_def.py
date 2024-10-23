from . import main

import inspect


from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry
from .common import COMMON_SECRET_VARIABLES


ui_component_svg_tool = Tool(
    name="create_ui_component_svg",
    type="docker",
    image="python:3.12",
    description="Creates a UI component based on {description} in svg format",
    args=[Arg(name="description", description="description of the UI component you want created", required=True)],
    content="""
curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env

uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1

uv pip install -r /tmp/requirements.txt > /dev/null 2>&1

python /tmp/main.py "{{ .description }}"
""",
    with_files=[
        FileSpec(
            destination="/tmp/main.py",
            source=inspect.getsource(main),
        ),
        FileSpec(
            destination="/tmp/requirements.txt",
            source="""
requests==2.32.3
litellm==1.49.5
""",  # Add any requirements here
        ),
    ],
    secrets=COMMON_SECRET_VARIABLES,
)

tool_registry.register("ui_component_svg", ui_component_svg_tool)
