a_revision:
	alembic revision --autogenerate -m "$(ARGS)" 

a_upgrade:
	alembic upgrade head 