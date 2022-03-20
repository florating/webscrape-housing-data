# Background

- https://pypi.org/project/selenium/
- https://towardsdatascience.com/17-terminal-commands-every-programmer-should-know-4fc4f4a5e20e
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Instructions

`/Users/flora/.gitconfig`

- `env source/bin/activate`
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
- `python3 main.py`

## Troubleshooting

https://stackoverflow.com/questions/58906183/vs-code-python-interpreter-cant-find-my-venv

- Activate your virtualenv. Go to the parent folder where your Virtual Environment is located and run venv\scripts\activate. Keep in mind that the first name "venv" can vary: `source venv/bin/activate`
- `pip freeze > requirements.txt`
- `deactivate` to exit the venv
- `rm venv` to delete the venv
- `py -m venv venv` to create a new one
- `pip install -r requirements.txt` to install the requirements.
