test:
	pytest -q
demo:
	python3 src/simulation/task1b_pid_balance_controller.py
	python3 scripts/plot_logs.py data/sample_logs.csv out/plot_recovery.png
