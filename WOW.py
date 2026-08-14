import subprocess

def contain(name):
        resultat = subprocess.run(
                ["docker","inspect","-f","{{.State.Status}}",name],
                capture_output=True,
                text=True
        )

        if resultat.returncode != 0:
                return "missing"
        return resultat.stdout.strip()
def start_redis(nam,prt):
        status = contain(nam)

        if status == "missing":
                print("container doesn't exist. Creating it...")
                subprocess.run([
                        "docker", "run",
                        "-d","--name"
                        , nam, "-p",f"{prt}:{prt}",
                        f"{nam}:latest"

                ])
        elif status == "exited":
                print("Container exist but is stopped. starting it ...")
                subprocess.run(["docker", "start", nam])

        elif status == "running":
                print("Redis is already running.")

ifn = input("wow: ")

if ifn =="stop" :
        start_redis(input("name bitte: "),input("port bitte: "))
elif ifn =="lösch" :
        subprocess.run(["docker", "rm", "-f", "redis"])


subprocess.run(["docker", "ps"])