Nginx logs task 2
      - write code that parse the nginx access.log (under /home/logs/access.log) and print stats every interval
      - The stats we want to see are:
        1. The number of calls since last interval
        2. The number of uniqe calls by method+path
        Example output should look like:
        ```
        Total of 4 calls since last interval
        Uniqe calls:
        GET / : 1
        GET /redhat : 1
        POST /{{ student }} : 2
