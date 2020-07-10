# NBA Combine Predictive Model

## Project Overview
* Created a system to predict first-year player efficiency (MAE ~ -0.08 FG%) statistics from player metrics recorded at the NBA Combine. 
* Scraped 5 years of NBA Combine and rookie-year player statistics using Python and BeautifulSoup.
* Engineered features from NBA Combine measurements and drills to determine their correlation with actual, in-game statistics.
* Compared accuracy of Linear and Random Forest regression models, using GridSearchCV to find the most optimal model.
* Built a client-facing API system using Flask.

## Resources Used
**Python Version:** 3.7 

**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle

**API Framework Requirements:** See [requirements.txt](https://github.com/carterwsmith/nbacombine/blob/master/FlaskAPI/requirements.txt) / use ```pip install -r requirements.txt```

**NBA Data API:** https://github.com/swar/nba_api

**Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## Scraping NBA Statistics
Utilized the NBA API to scrape NBA Combine and rookie-year statistics from the 2014-19 NBA seasons. I gathered the following data for each player:
* Player Details (Season, Name, Position)
* NBA Combine Measurables (Height w & w/o shoes, Weight, Wingspan, Vertical, etc.)
* NBA Combine Drill Results (Lane Agility, 3/4 Sprint, Bench Press, Shooting Performances, etc.)
* Rookie Year Statistics (GP, MIN, PPG, RPG, APG, FG%, etc.)

## Data Cleaning
I needed to clean the data to make it usable with a model. I made the following changes:
* Removed unnecessary or duplicated data, identifying players by their NBA API ID.
* Gathered relevant data for players who did not immediately play in NBA.
* Parsed Imperial measurements into readable decimals.
* Evaluated fractional shooting performances into raw percentages.

## Data Analysis
I explored the distribution of the data and the correlation between some measurements and statistics. Here are some relevant visuals: 

![alt text](https://github.com/carterwsmith/nbacombine/blob/master/defensive_correlation.png "Correlated Defense Figures")
![alt text](https://github.com/carterwsmith/nbacombine/blob/master/vertical_leap_plot.png "Vertical Leap Distribution")
![alt text](https://github.com/carterwsmith/nbacombine/blob/master/measurable_comparison.png "Related Measurable Comparison")

## Model Optimization
I began by splitting the data into training (20%) and testing (80%) sets, testing for Field Goal Percentage (FG%). I created two models and, given the density of the results, evaluated their accuracy by Mean Absolute Error. 

* **Linear Regression**: Standard model that accounts for the large number of recorded stats.
* **Random Forest**: Because the data is made up of widely varied measurements, this model could result in higher accuracy.

## Model Analysis
The optimized Random Forest model ended up giving the most accurate reponses to test data.
* **Random Forest**: -0.081 FG%
* **Linear Regression**: -0.099 FG%

## Productionization
I built a Flask API endpoint, hosted locally, for the user to provide the values of a Combine performance and for the API to request an estimated first-year NBA FG%.

## Conclusion
This project gave me insight to how the workouts and measurements of the NBA Combine factor into a player's success in their rookie year. 

This tool could be used in various ways:
* For NBA teams to analyze a player's Combine stats,
* To explore the correlation between physical characteristics and rookie-year success,
* Or to evaluate a player's transition from college-level performance to the NBA.

In the future, this tool could be built upon with additional draft classes to become more accurate. The model could also be trained to predict other factors, like 3PM or BPG, for teams to analyze a player's potential fit in a specific scheme or role.
