import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
import os
from . import log

proxy_root="/sparkui/ui"
logger = log.get_logger("sparkmonitorserver")


class SparkUIRouteHandler(APIHandler):
    """A custom tornado request handler to proxy Spark Web UI requests."""
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    
    @tornado.web.authenticated
    def get(self):
        """Handles get requests to the Spark UI
        Fetches the Spark Web UI from the configured ports
        """
        spark_ui_base_url = os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1")
        spark_ui_port = os.environ.get("SPARKMONITOR_UI_PORT", "4040")
        spark_ui_url = "http://{baseurl}:{port}".format(baseurl=spark_ui_base_url,port=spark_ui_port)

        logger.debug(self.request.uri)
        logger.debug(self.request.uri.index(proxy_root))
        request_path = self.request.uri[(self.request.uri.index(proxy_root) + len(proxy_root) + 1):]
        logger.debug(request_path)
        self.replace_path = self.request.uri[:self.request.uri.index(proxy_root) + len(proxy_root)]
        logger.debug('replace path- ' + self.replace_path)
        backendurl = url_path_join(spark_ui_url, request_path)
        logger.debug(backendurl)
        self.debug_url = spark_ui_url
        self.backendurl = backendurl

        logger.info("GET: \n Request uri:%s \n Port: %s \n Host: %s \n request_path: %s ", self.request.uri,
                    os.environ.get(
                        "SPARKMONITOR_UI_PORT", "4040"), os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1"),
                    request_path)

        self.finish(json.dumps({
            "data": "Test!"
        }))

def setup_handlers(web_app):
    # init_logger()
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern_sparkui = url_path_join(base_url, "sparkui", "ui")
    handlers = [(route_pattern_sparkui, SparkUIRouteHandler)]
    web_app.add_handlers(host_pattern, handlers)