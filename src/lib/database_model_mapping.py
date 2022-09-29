from sqlalchemy import Column, String, Integer, Text, Table, ForeignKey, Boolean, text, Float
from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm.collections import InstrumentedList
from models.client import Client
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage

def register_sqlalchemy_models():
    mapper_registry = registry()

    metadata = mapper_registry.metadata

    t_clients = Table(
        'clients', metadata,
        Column('id', Integer, primary_key=True),
        Column('title', Text, nullable=False),
        Column('type', Text, nullable=False),
        Column('proxy_port', Integer, nullable=False),
        Column('browser_port', Integer),
        Column('open', Boolean, nullable=False, server_default=text("0")),
        Column('created_at', Integer, nullable=False),
        Column('launched_at', Integer)
    )

    t_http_flows = Table(
        'http_flows', metadata,
        Column('id', Integer, primary_key=True),
        Column('uuid', Text, index=True),
        Column('client_id', ForeignKey('clients.id')),
        Column('type', Text, nullable=False, index=True),
        Column('title', Text),
        Column('request_id', ForeignKey('http_requests.id')),
        Column('original_request_id', ForeignKey('http_requests.id')),
        Column('response_id', ForeignKey('http_responses.id')),
        Column('original_response_id', ForeignKey('http_responses.id')),
        Column('http_flow_id', Integer),
        Column('created_at', Integer, nullable=False)
    )

    # t_editor_items = Table(
    #     'editor_items', metadata,
    #     Column('id', Integer, primary_key=True),
    #     Column('parent_id', ForeignKey('editor_items.id'), index=True),
    #     Column('name', Text, nullable=False),
    #     Column('item_type', Text, nullable=False),
    #     Column('item_id', Integer),
    #     Column('created_at', Integer, nullable=False)
    # )

    t_http_requests = Table(
        'http_requests', metadata,
        Column('id', Integer, primary_key=True),
        Column('http_version', Text, nullable=False),
        Column('headers', Text),
        Column('content', Text),
        Column('trailers', Text),
        Column('timestamp_start', Float),
        Column('timestamp_end', Float),
        Column('host', Text, nullable=False, index=True),
        Column('port', Integer),
        Column('method', Text, nullable=False),
        Column('scheme', Text, nullable=False),
        Column('authority', Text),
        Column('path', Text, nullable=False),
        Column('form_data', Text, nullable=False),
        Column('created_at', Integer, nullable=False)
    )

    t_http_responses = Table(
        'http_responses', metadata,
        Column('id', Integer, primary_key=True),
        Column('http_version', Text, nullable=False),
        Column('headers', Text, nullable=False),
        Column('content', Text),
        Column('timestamp_start', Float),
        Column('timestamp_end', Float),
        Column('status_code', Integer, nullable=False),
        Column('reason', Text),
        Column('created_at', Integer, nullable=False)
    )

    # t_settings = Table(
    #     'settings', metadata,
    #     Column('id', Integer, primary_key=True),
    #     Column('json', Text, nullable=False)
    # )


    # t_variables = Table(
    #     'variables', metadata,
    #     Column('id', Integer, primary_key=True),
    #     Column('key', Text, nullable=False, index=True),
    #     Column('value', Text, nullable=False),
    #     Column('description', Text),
    #     Column('source_type', Text, nullable=False),
    #     Column('source_id', Integer),
    #     Column('created_at', Integer, nullable=False)
    # )

    t_websocket_messages = Table(
        'websocket_messages', metadata,
        Column('id', Integer, primary_key=True),
        Column('http_flow_id', ForeignKey('http_flows.id')),
        Column('direction', Text, nullable=False),
        Column('content', Text, nullable=False),
        Column('content_original', Text),
        Column('created_at', Integer, nullable=False)
    )

    mapper_registry.map_imperatively(Client, t_clients)

    mapper_registry.map_imperatively(HttpFlow, t_http_flows, properties={
        'client' : relationship(Client, backref='flow'),
        'request' : relationship(HttpRequest, foreign_keys='HttpFlow.request_id'),
        'original_request' : relationship(HttpRequest, foreign_keys='HttpFlow.original_request_id'),
        'response' : relationship(HttpResponse, foreign_keys='HttpFlow.response_id'),
        'original_response' : relationship(HttpResponse, foreign_keys='HttpFlow.original_response_id'),
        'websocket_messages': relationship(WebsocketMessage, foreign_keys='WebsocketMessage.http_flow_id', uselist=True),
    })

    mapper_registry.map_imperatively(HttpRequest, t_http_requests)

    mapper_registry.map_imperatively(HttpResponse, t_http_responses)

    mapper_registry.map_imperatively(WebsocketMessage, t_websocket_messages)

