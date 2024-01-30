# WOLT 2024 internship pre-assignment
This is my solution for [WOLT](https://wolt.com/en)'s [2024 internship](https://careers.wolt.com/en/jobs/software-engineer-intern-(2024)/3823ba7) [pre-assignment](https://github.com/woltapp/engineering-internship-2024)


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
