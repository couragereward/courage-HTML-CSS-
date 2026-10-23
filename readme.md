# Rexitoon

Rexitoon is a responsive anime-character carousel built with Flask, HTML, CSS, and
vanilla JavaScript. Browse 20 characters, read a short description of each one,
and view their images without cropping the main character artwork.

## Features

- Twenty character profiles with anime titles, tags, and descriptions.
- Main images fit inside the frame so the full artwork remains visible.
- A blurred image backdrop and accent colors that update with the selected image.
- Character navigation through the arrows, thumbnail strip, keyboard, or touch
  swipe.
- Automatic carousel advancement every six seconds.
- Image download and fullscreen controls.
- Responsive layout for desktop and mobile screens.

## Requirements

- Python 3.10 or newer
- Flask (listed in `requirements.txt`)

## Run locally

From the project directory, create and activate a virtual environment, then
install the dependency:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the Flask development server:

```powershell
.\.venv\Scripts\python.exe index.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser. Stop the server
with `Ctrl+C`.

## Project files

- `index.py` — Flask application, character data, API, image, and download routes.
- `index.html` — page markup.
- `style.css` — responsive styling.
- `script.js` — carousel interactions and image-driven theme.
- `images/` — character images.

The application serves its CSS, JavaScript, and image files through Flask routes;
it does not require a `static/` directory.

## Image filenames

Character images belong in `images/`. The `image_file` value for each character
in `CHARACTERS` in `index.py` must match its filename exactly, including spaces
and extension. Supported extensions for automatic filename lookup are `.jpg`,
`.jpeg`, `.png`, and `.webp`.

If a configured image is missing, the app displays a generated placeholder.

## Controls

- Use **Previous** and **Next**, or the left and right arrow keys, to change
  characters.
- Select a thumbnail to jump directly to that character.
- Swipe left or right on the main image on touch devices.
- Select the download icon to save the selected image.
- Select the fullscreen icon or press `F` to toggle fullscreen.
