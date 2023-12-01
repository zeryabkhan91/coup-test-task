# Coup Game

## Description

This Django project serves as a comprehensive platform for managing and playing the renowned Coup card game. It offers a user-friendly web interface for seamless gameplay and incorporates a feature to read and display game data from a designated file.

## Requirements

To run this project, you will need the following:

- Python 3.x
- Redis Server
- Git (optional, for cloning the repository)

## Setup Instructions

1. Clone the repository
```shell
git clone git@github.com:zeryabkhan91/coup-test-task.git
```

2. Create a virtual environment (recommended but optional):
```shell
python -m venv venv
```

3. Install the required Python packages:
```shell
pip install -r requirements.txt
```

## Usage

To start project run command below:

```shell
python3 manage.py runserver
```

It will show up index page, click stat game and enjoy playing it.

## Project Structure

The project directory structure is as follows:

## File Structure

coup_game/: Django app containing djano app settings, urls and views.
game/: Django app containing the main game logic.
templates/: HTML templates for rendering views.
static/: Static files (CSS, JavaScript, etc.) for the web application.
manage.py: Django management script.
requirements.txt: List of Python dependencies.
