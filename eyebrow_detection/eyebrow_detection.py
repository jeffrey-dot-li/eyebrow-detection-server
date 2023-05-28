"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
from eyebrow_detection.api import create_upload_file
import pynecone as pc
from typing import List, Tuple

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"




class State(pc.State):
    """The app state."""

    # The images to show.
    csv_rows: list[list[str]] = []

    async def handle_upload(self, files: List[pc.UploadFile]):
        self.csv_rows = (await create_upload_file(files))


color = "blue"


def index():
    """The main view."""
    return pc.vstack(
        pc.upload(
            pc.vstack(
                pc.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                pc.text("Drag and drop files here or click to select files"),
            ),
            multiple=True,
            accept={
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/webp": [".webp"],
            },
            max_files=5,
            disabled=False,
            on_keyboard=True,
            border=f"1px dotted {color}",
            padding="5em",
        ),
        pc.button(
            "Upload",
            on_click=lambda: State.handle_upload(pc.upload_files()),
        ),
        pc.foreach(
            State.csv_rows, lambda txt: pc.text(txt)          
        ),
        padding="5em",
    )

async def api_test():
    return {"my_result": "hi"}




# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.api.add_api_route("/upload_file", create_upload_file, methods=["POST"])
app.api.add_api_route("/test", api_test)
app.compile()
