class Config:
    SECRET_KEY = "b825c713da1c27fc72d8cb8d0875f7cc"
    SQLALCHEMY_DATABASE_URI = "sqlite:///seeker.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SECRET_KEY = "b825c713da1c27fc72d8cb8d0875f7cc"
    SQLALCHEMY_DATABASE_URI = "sqlite:///seekerTest.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False