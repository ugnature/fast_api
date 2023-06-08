# here we are going to set enviorment variable in the local machine in which this app will run
# an enviorment variable can be of secret key, database_username, database_password etc
# but before setting the envoirment varible we should use pydentic model -> base setting feature
# which help us in checking if we have assigned values to every environment variable or not

# benifit of creating this config.py file is that u can skip this file at the time of pushing everything to github

# now we will connect this file with .env file where we have given the secret values

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'


settings = Settings()
