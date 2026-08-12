# 🗳️ ElectionPulse AI

### AI-Powered Election Prediction & Forecasting Platform

ElectionPulse AI is an end-to-end machine learning web application designed to analyze historical Indian election data and generate constituency-level election predictions.

The platform combines Machine Learning, Time Series Forecasting, FastAPI, React, Docker, AWS EC2 and DuckDNS to provide an interactive election analytics and prediction system.
 Live Website

Live Demo:**  
http://electionprediction.duckdns.org

> The application is deployed on AWS EC2 using Docker.

---

 Project Overview

ElectionPulse AI analyzes historical election data to identify voting patterns and generate ML-based predictions.

The system provides:

- Lok Sabha election analysis
- Constituency-level prediction
- Party-wise prediction
- Vote forecasting
- Time-series analysis
- Interactive election dashboard
- REST APIs for predictions
- Historical election visualization

The goal is to demonstrate how machine learning and data analytics can be applied to historical electoral data to build an election forecasting system.

---

 Objectives

- Analyze historical Indian election datasets.
- Build an automated ML prediction pipeline.
- Predict likely winning parties at the constituency level.
- Forecast future election-related trends.
- Provide an interactive visualization dashboard.
- Deploy the complete application using Docker and AWS.

---

 Features

 Election Prediction

Users can enter constituency information and receive:

- Predicted winner
- Predicted party
- Winning probability
- Predicted votes

Election Analytics

The dashboard provides:

- Historical election trends
- Party-wise performance
- Total votes
- Constituency-level information
- Election statistics

 Time Series Forecasting

Historical election data is analyzed to identify trends and generate future projections.

The forecasting module is used for analytical trend estimation rather than guaranteeing actual future election outcomes.

 FastAPI Backend

The backend exposes REST APIs for:

- Election prediction
- Constituency prediction
- Model information
- Data processing
- Forecasting

Interactive API documentation is available through FastAPI Swagger UI.

```text
/docs
