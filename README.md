This project is running in combination with PostgreSQL server, version:<br> 
**psql (14.2 (Ubuntu 14.2-1.pgdg20.04+1+b1))**

Python interpreter version: **3.8**

### For terminal lovers:
1. Navigate to the `blue-prism` directory, `cd ~/Git/<git-clone-destination>/`;
2. Create virtual environment named `venv`, `python3 -m venv venv`;
3. Activate the virtual environment, `. venv/bin/activate`;
4. Install the project requirements using `pip` or another preferred alternative,<br>`pip install -r requirements.txt`;
5. Start the FastAPI server, `uvicorn app.main:app --port 5000 --reload`;
6. Issue a [POST] request as follows `http://127.0.0.1:5000/ingest_file?filename=dataset`;
7. Open your `pgAdmin`, or alternative database client, observe the created tables together with their contents;
8. Run test from the project directory, `python -m unittest discover`;