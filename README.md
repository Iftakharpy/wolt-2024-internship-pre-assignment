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

After installing the dependencies, you can run the project by running the following command in the terminal:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Then open your browser and go to `http://localhost:8000/docs` to see the docs of the api endpoints.

> Note: Of course, you will have to be in the project's base directory(ie. where `Dockerfile` and `README.md` file is located) to for this command to work.🙂

## Run tests

To run the tests, open the terminal in the project base directory, this means the the directory where the `pytest.ini` is located. Then run the following command:

```bash
pytest -v
```

> Note: You should have the project dependencies installed before running the tests.

## To get coverage report

To get the coverage report, open the terminal in the project base directory, this means the the directory where the `pytest.ini` is located. Then run the `coverage.sh` or `coverage.ps1` depending on your operating system.

## Project structure

All the files related to the project are located in the `app` directory. The `app` directory contains the following files and directories:

```bash
.
│   main.py
│   __init__.py
│
├───delivery_fee
│       fee_calculation_steps.py
│       fee_calculator.py
│       fee_transformers.py
│       models.py
│       router.py
│       settings.py
│       utility_meta_classes.py
│       __init__.py
│
└───tests
    │   test_main.py
    │   __init__.py
    │
    └───delivery_fee
        │   test_fee_calculator_initialization.py
        │   __init__.py
        │
        ├───calculation_steps
        │       test_cart_value_fee.py
        │       test_delivery_distance_fee.py
        │       test_number_of_items_fee.py
        │       __init__.py
        │
        ├───calculation_transformers
        │       test_limit_fee_transformer.py
        │       test_reduce_fee_transformer.py
        │       test_rush_hour_fee_transformer.py
        │       __init__.py
        │
        └───model
                test_delivery_fee.py
                test_order_info.py
```

-   `./app/tests/` has all the test cases organized logically under corresponding subfolders. The subfolders is created for each module in the `./app/delivery_fee/` directory on when the number of test cases are too much to store in one file.
-   `main.py` is the entry point of the application.
-   `./app/delivery_fee/` has all the modules related to the delivery fee calculation.
-   `./app/delivery_fee/router.py` has the router for the delivery fee calculation api.
-   `./app/delivery_fee/models.py` has the pydantic models used in the api these are used for data parsing.
-   `./app/delivery_fee/settings.py` has the settings for the delivery fee calculation api.
-   `./app/delivery_fee/utility_meta_classes.py` has the utility meta classes these are used to create the singleton classes.
-   `./app/delivery_fee/fee_calculator.py` has the fee calculator class which is used to calculate the delivery fee.
-   `./app/delivery_fee/fee_calculation_steps.py` has the fee calculation steps which are used to calculate the delivery fee. These does not modify the fee, they calculate fee depending on the order info.
-   `./app/delivery_fee/fee_transformers.py` has the fee transformers which are used to modify the fee. These does not calculate the fee, they modify the fee depending on the order info.
-   `./app/delivery_fee/fee_calculator.py` has the fee calculator class which is used to first follow the delivery calculation steps and then applies the transformers to apply any rules on the calculated fee.

## Class relationships

-   `DeliveryFeeTransformer` and `DeliveryFeeCalculationStep` are interfaces. These are
    implemented by the other classes in the `fee_transformers.py` and `fee_calculation_steps.py` files respectively. Each of these classes has
    their own ConfigOptions sub class which holds the options when calculating or transforming the fee.
-   `DeliveryFeeCalculator` is the main class which is used to calculate the delivery fee. It uses the `DeliveryFeeCalculationStep` and `DeliveryFeeTransformer` classes to calculate and transform the fee.
