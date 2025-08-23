# 1) Create a virtual environment
python3 -m venv .venv

# 2) Activate it
source .venv/bin/activate

# 3) Install requirements
pip install -r requirements.txt

# 4) Install local packages
pip install ./api ./platform ./data_source_json ./data_source_xml ./simple_visualizer ./block_visualizer

# 5) Enter the Django project
cd graph_explorer || exit

# 6) Make migrations, migrate, and run the server
python manage.py makemigrations && python manage.py migrate && python manage.py runserver