import os

def get_base_url ():

    env = os.environ.get("ENV","test")

    if env.lower() == "test":
        return "https://frontend-dev-36462279645.me-central2.run.app"
    elif env.lower() == "main":
        return "https://core.lameh.ai/"
    elif env.lower() == "uat":
        return "https://frontend-dev-36462279645.me-central2.app"
    else :
        raise Exception (f"Unkown environment: {env}")
