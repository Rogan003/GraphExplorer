python -m venv .venv

if [ -f ".venv/bin/activate" ]; then
    # macOS/Linux
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    # Windows (Git Bash or cmd)
    source .venv/Scripts/activate
elif [ -f ".venv/Scripts/Activate.ps1" ]; then
    # Windows PowerShell
    . .venv/Scripts/Activate.ps1
else
    echo "Could not find venv activation script"
    exit 1
fi

pip install -r requirements.txt

pip install ./api ./platform ./data_source_json ./data_source_xml ./simple_visualizer ./block_visualizer

cd graph_explorer || exit

python manage.py makemigrations && python manage.py migrate && python manage.py runserver