# WOLT 2024 internship pre-assignment

This is my solution for [WOLT](https://wolt.com/en)'s [2024 internship](<https://careers.wolt.com/en/jobs/software-engineer-intern-(2024)/3823ba7>) [pre-assignment](https://github.com/woltapp/engineering-internship-2024)

## Run project using docker

To run the project locally, it is recommended to use docker. So for that you will need docker installed on your machine. If you don't have docker installed, you can follow the instructions [here](https://docs.docker.com/get-docker/).

To run project using docker, open the terminal in the project base directory, this means the the directory where the `Dockerfile` is located. Then run the following command:

```bash
docker compose up --build
```

To see the docs of the api endpoints, open your browser and go to `http://localhost:80/docs`.

To stop the project, press `Ctrl + C` in the terminal and then run the following command:

```bash
docker compose down
```

## Run project without docker

To run this project without docker, you will have to have python 3 install. I recommend using `Python version 3.12.0` since this is the version I used during development. You can download python from [here](https://www.python.org/downloads/). When you have python installed, you will need to install the dependencies. To do so run the following command in the terminal:

```bash
pip install -r requirements.txt
```

> Note: You might need to use `pip3` instead of `pip` depending on your python installation.
> And also your current directory should be the project base directory, this means the the directory where the `requirements.txt` is located.

## Run tests

To run the tests, open the terminal in the project base directory, this means the the directory where the `pytest.ini` is located. Then run the following command:

```bash
pytest -v
```

> Note: You should have the project dependencies installed before running the tests.

## To get coverage report

To get the coverage report, open the terminal in the project base directory, this means the the directory where the `pytest.ini` is located. Then run the `coverage.sh` or `coverage.ps1` depending on your operating system.
