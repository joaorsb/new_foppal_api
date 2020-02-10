import urllib.parse
import os

import motor.motor_asyncio
from models.app_link_model import AppLinkModel


class DBConnection:

    @classmethod
    def create_client(cls):
        password = os.environ.get('MONGO_ATLAS')
        env_mongo_uri = os.environ.get('MONGO_DB_URI')
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(env_mongo_uri)
        return mongo_client

    @staticmethod
    def create_main_connection(app_link: str):
        mongo_client = DBConnection.create_client()
        mongo_db = mongo_client.news_links
        if app_link == AppLinkModel.brazil:
            collection = mongo_db.brazil_links_teamnews
        elif app_link == AppLinkModel.deutschland:
            collection = mongo_db.deutschland_links_teamnews
        elif app_link == AppLinkModel.espana:
            collection = mongo_db.espana_links_teamnews
        elif app_link == AppLinkModel.nederland:
            collection = mongo_db.netherlands_links_teamnews
        elif app_link == AppLinkModel.sverige:
            collection = mongo_db.sverige_links_teamnews
        else:
            collection = mongo_db.norge_links_teamnews

        return collection

    @staticmethod
    def create_teams_connection(app_link: str):
        mongo_client = DBConnection.create_client()
        mongo_db = mongo_client.news_links

        if app_link == AppLinkModel.brazil:
            collection = mongo_db.brazil_links_footballteam
        elif app_link == AppLinkModel.deutschland:
            collection = mongo_db.deutschland_links_footballteam
        elif app_link == AppLinkModel.espana:
            collection = mongo_db.espana_links_footballteam
        elif app_link == AppLinkModel.nederland:
            collection = mongo_db.netherlands_links_footballteam
        elif app_link == AppLinkModel.sverige:
            collection = mongo_db.sverige_links_footballteam
        else:
            collection = mongo_db.norge_links_footballteam

        return collection

    @staticmethod
    def create_events_connection(app_link: str):
        mongo_client = DBConnection.create_client()
        mongo_db = mongo_client.news_links

        if app_link == AppLinkModel.brazil:
            collection = mongo_db.brazil_links_event
        elif app_link == AppLinkModel.deutschland:
            collection = mongo_db.deutschland_links_event
        elif app_link == AppLinkModel.espana:
            collection = mongo_db.espana_links_event
        elif app_link == AppLinkModel.nederland:
            collection = mongo_db.netherlands_links_event
        elif app_link == AppLinkModel.sverige:
            collection = mongo_db.sverige_links_event
        else:
            collection = mongo_db.norge_links_event

        return collection
