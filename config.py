from environs import Env


env = Env()
env.read_env()


class Config:
    with env.prefixed("DATABASE_"):
        DB = dict(
            host=env.str("HOST"),
            port=env.int("PORT"),
            database=env.str("NAME"),
            user=env.str("USER"),
            password=env.str("PASSWORD"),
        )
    BASE_URL = env.str("BASE_URL")
