echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.12 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all deps in the venv
pip3 install -r requirements.txt

# collect static files using the Python interpreter from venv
python3.12 manage.py migrate
python3.12 manage.py collectstatic --noinput

echo "BUILD END"