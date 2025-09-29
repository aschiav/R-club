# Install necessary packages
install.packages("httr")
install.packages("dplyr")
install.packages("jsonlite")
install.packages("ggplot2")

# Load necessary libraries
library(httr)
library(jsonlite)
library(dplyr)
library(ggplot2)

#documentation
"https://marketstack.com/documentation"

#other free APIs:
"https://github.com/public-apis/public-apis?tab=readme-ov-file"


# Set the stock symbol, your MarketStack API key, and the date range

symbol <- "AAPL"  # Example: Apple Inc.
api_key <- "f2dc5cde7b7ca3479b849cd8324349e2"
start_date <- "2024-02-01"  # Start date (YYYY-MM-DD)
end_date <- "2025-02-20"    # End date (YYYY-MM-DD)

# Construct the API endpoint URL with the date range
url <- paste0("http://api.marketstack.com/v1/eod?access_key=", api_key, "&symbols=", symbol, "&date_from=", start_date, "&date_to=", end_date)

# Make the GET request
response <- GET(url)

#check response code:
print(response$status_code)

#see JSON object
cat(content(response, "text"), "\n")

# Check the status of the response
if (status_code(response) == 200) {
  # Extract the content and parse the JSON
  stock_data <- content(response, "parsed")$data
  
  # Convert the data into a manageable data frame
  df <- data.frame(
    date = sapply(stock_data, function(x) x$date),
    open = sapply(stock_data, function(x) x$open),
    high = sapply(stock_data, function(x) x$high),
    low = sapply(stock_data, function(x) x$low),
    close = sapply(stock_data, function(x) x$close),
    volume = sapply(stock_data, function(x) x$volume),
    adj_close = sapply(stock_data, function(x) x$adj_close),
    dividend = sapply(stock_data, function(x) x$dividend),
    stringsAsFactors = FALSE
  )
  
  # Convert the 'date' column to Date format
  df$date <- as.Date(df$date, format = "%Y-%m-%d")
  
  # View the data frame
  print(df)
} else {
  cat("Error:", status_code(response), "Unable to fetch data\n")
}


#plot daily high
df %>%
  ggplot()+
  geom_line(aes(x=date, y=high), color="blue")+
  geom_line(aes(x=date, y=low), color="red")
