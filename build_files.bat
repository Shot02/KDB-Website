@echo off
echo Building project...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Making migrations...
python manage.py makemigrations
python manage.py migrate

echo Collecting static files...
python manage.py collectstatic --noinput

echo Build completed!