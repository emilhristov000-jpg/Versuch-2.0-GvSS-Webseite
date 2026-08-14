import redis
import subprocess


def redis_start():
    try:
        r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

        r.ping()
        print("Redis is already running.")
        return r

    except redis.exceptions.ConnectionError:
        print("Redis isn't running. Starting Docker container...")

        subprocess.run([
            "docker", "start", "redis"
        ], check=False)

        r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

        try:
            r.ping()
            print("Redis started successfully.")
            return r

        except redis.exceptions.ConnectionError:
            print("Could not start Redis.")
            return None