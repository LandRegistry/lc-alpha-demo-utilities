import os


class Config(object):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    B2B_REGISTER_URL = "http://localhost:5001"
    B2B_SEARCH_REG_URL = "http://localhost:5004"
    B2B_SEARCH_WORK_URL = "http://localhost:5006"
    DB2_MIGRATOR_URL = "http://localhost:5009"
    DB2_LEGACY_URL = "http://localhost:5007"


class PreviewConfig(Config):
    B2B_REGISTER_URL = "http://localhost:5001"
    B2B_SEARCH_REG_URL = "http://localhost:5004"
    B2B_SEARCH_WORK_URL = "http://localhost:5006"
    DB2_MIGRATOR_URL = "http://localhost:5009"
    DB2_LEGACY_URL = "http://localhost:5007"