import redis
import subprocess
import time

def redis_start():
    r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
    try:

        r.ping()
        print("Redis is already running.")
        return r

    except redis.exceptions.ConnectionError:
        print("Redis isn't running. Starting Docker container...")

        wow =subprocess.run([
            "docker", "start", "redis"
        ], capture_output=True, text=True)

        if wow.returncode != 0:
            print(f"Failed to start container: {wow.stderr.strip()}")
            return None

        for _ in range(5):
                time.sleep(1)
                try:
                    r.ping()
                    print("Redis started successfully.")
                    return r
                except redis.exceptions.ConnectionError:
                    continue

        print("Could not connect to Redis after container start.")
        return None

redis_start()