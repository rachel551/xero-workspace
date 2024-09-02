#!/bin/sh

host="$1"
shift
port="$1"
shift
path="$1"
shift
# Default timeout set to 15 seconds, can be overridden with the WAIT_TIMEOUT environment variable
timeout="${WAIT_TIMEOUT:-15}"
cmd="$@"

url="http://$host:$port$path"

echo "Waiting for $url to be available..."

start_time=$(date +%s)

while true; do
  if curl --silent --fail "$url" > /dev/null; then
    echo "$url is up!"
    exec $cmd
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