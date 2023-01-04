docker-compose up db -d --build --force-recreate --wait

sleep 1

alembic upgrade head

sleep 1

python3 app.py
