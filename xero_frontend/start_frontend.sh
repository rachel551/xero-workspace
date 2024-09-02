#!/bin/sh

url='http://host.docker.internal:8000/api/balance-sheet'
timeout="${WAIT_TIMEOUT:-15}"
cmd="$@"

echo "Waiting for $url to be available..."

start_time=$(date +%s)

Function to fetch data
fetch_data() {
  DATA=$(curl -s "$url")
  if [ $? -ne 0 ]; then
    echo "Error fetching data from API."
    exit 1
  fi
  echo "$DATA" > /app/public/data.json
  echo "Data fetched and saved successfully."
}

while true; do
  if curl --silent --fail "$url" > /dev/null; then
    echo "$url is up!"
    echo "Fetching data..."
    fetch_data
    # Break the loop after successful data fetch
    break
  else
    echo "$url is not available. Retrying..."
  fi

  current_time=$(date +%s)
  elapsed_time=$((current_time - start_time))

  if [ "$elapsed_time" -ge "$timeout" ]; then
    echo "Timeout of $timeout seconds reached while waiting for $url"
    exit 1
  fi

  sleep 1
done

exec $cmd