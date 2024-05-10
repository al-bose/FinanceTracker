## Overview
This web application allows users to track their expenditure and portfolio metrics.

The key technologies used are: Django, PostgreSQL, Python, JavaScript, HTML, Tailwind CSS (Standalone CLI without node.js), Alpha Vantage API (financial API), Chart.js (creating pie chart), Redis (used for low-level caching of the API calls to Alpha Vantage).

This project is deployed using Supabase, Redis Cloud and Vercel (CI/CD).

## Future Work To Be Done
- Implement changes to support cryptocurrencies (Alpha Vantage API uses different API endpoints for digital currencies)
- Refactor tailwind styling to use custom theme styles in the configuration
- Implement Forgot/Reset Password functionality
- Add unit tests and look to integrate them into the CI/CD pipeline

## Notes
- Utilized native django low-level redis caching API to cache the API calls to get stock data from Alpha Vantage. This is actually really important because there is a limit of 25 APi calls a day in the free tier. By caching the stock data we at least make sure we can support up to 25 unique stocks.
- I was able to use Tailwind Standalone CLI, which means there is no node dependency
- Utilized the native authentication functionality that Django provides with no customization done to the User model
- Project is deployed with Vercel and CI/CD is enabled (pushes to main branch)
- There is a memory cap of 30 MB in the free Redis plan that I am currently using

## References and Links:
- https://finance-tracker-three-xi.vercel.app/
- https://tailwindcss.com/docs/installation
- https://www.alphavantage.co/documentation/
- https://www.chartjs.org/
- https://redis.io/docs/latest/operate/rc/

## Running Locally:
You should be able to clone and run this repository locally by using the requirements.txt file and the commands that can be found in the build script. 

When running locally you will also have to create a .env file and specify:
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT (can be a local PostgreSQL database)
API_KEY (Alpha Vantage API key)
REDIS_URL (can either be a local instance of redis or redis cloud)
