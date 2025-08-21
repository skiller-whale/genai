# Flask HTMX App

This project is a web application built using Flask for the backend and HTMX for the frontend. It allows users to view and add posts with infinite scrolling functionality.

## Project Structure

```
forum
├── src
│   ├── app.py                # Entry point of the application
│   ├── templates             # Contains HTML templates
│   │   ├── index.html       # Displays posts with infinite scroll
│   │   └── form.html        # Form for adding new posts
│   ├── static                # Contains static files
│   │   ├── styles.css        # CSS styles for the frontend
│   │   └── scripts.js        # JavaScript for handling infinite scroll and form submission
│   ├── data                  # Contains data files
│   │   └── posts.json        # Hardcoded posts in JSON format
│   └── routes                # Contains route definitions
│       └── api.py            # API routes for fetching and adding posts
├── requirements.txt          # Lists project dependencies
├── README.md                 # Documentation for the project
└── config.py                 # Configuration settings for the Flask application
```

## Features

- Infinite scroll for viewing posts
- Form to add new posts
- Hardcoded posts for demonstration

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies using:

```
pip install -r requirements.txt
```

## Usage

Run the application using:

```
python src/app.py
```

Visit `http://localhost:5000` in your web browser to access the application.