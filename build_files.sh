echo "Build Start"
python3.12 -m pip install -r requirements.txt

python3.12 manage.py makemigrations --noinput 
python3.12 manage.py migrate --noinput 

python3.12 manage.py collectstatic --noinput --clear
echo "Build end"