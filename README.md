Download the both .pkl file from the google drive link
https://drive.google.com/file/d/18mpEsFwHmUTEv7DF_Pq5UgMZswPzRSSm/view?usp=drive_link
https://drive.google.com/file/d/1lrg5LCuZeurJgjI-dnH1gSiW7f5oxt87/view?usp=drive_link

Then, running the app, I am providing three ways in the render.txt file:
For docker, run this command:
1.	docker build -t sales_forecasting_api .

2.	docker run -p 8000:8000 sales_forecasting_api
For running the app using uvicorn, use this commend:
		python3 app/main.py
For exposing the api into publically use this ngrok commend
		ngrok http 8501

