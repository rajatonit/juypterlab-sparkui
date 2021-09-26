import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
import os
from . import log
from . import helpers
from tornado import httpclient

proxy_root="/sparkui/ui"
logger = log.get_logger("sparkmonitorserver")


class SparkUIRouteHandler(APIHandler):
    """A custom tornado request handler to proxy Spark Web UI requests."""
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    
    @tornado.web.authenticated
    async def get(self):
        """Handles get requests to the Spark UI
        Fetches the Spark Web UI from the configured ports
        """
        http = httpclient.AsyncHTTPClient()

        spark_ui_base_url = os.environ.get("SPARKMONITOR_UI_HOST", "localhost")
        spark_ui_port = os.environ.get("SPARKMONITOR_UI_PORT", "8080")
        spark_ui_url = "http://{baseurl}:{port}".format(baseurl=spark_ui_base_url,port=spark_ui_port)

        request_path = self.request.uri[(self.request.uri.index(proxy_root) + len(proxy_root) + 1):]
        self.replace_path = self.request.uri[:self.request.uri.index(proxy_root) + len(proxy_root)]
        backendurl = helpers.url_path_join(spark_ui_url, request_path)
        self.debug_url = spark_ui_url
        self.backendurl = backendurl

        logger.info("GET: \n Request uri:%s \n Port: %s \n Host: %s \n request_path: %s ", self.request.uri,
                    os.environ.get(
                        "SPARKMONITOR_UI_PORT", "4040"), os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1"),
                    request_path)
        try:
            x = await http.fetch(backendurl)
            self.handle_response(x)
        except:
            self.handle_bad_response()

    def handle_bad_response(self):
        content_type = "text/html"

        try:
            with open(os.path.join(os.path.dirname(__file__), "spark_not_found.html"), 'r') as f:
                content = f.read()
                self.set_header("Content-Type", content_type)
                self.write(content)
            logger.info("SPARKMONITOR_SERVER: Spark UI not running")
        except FileNotFoundError:
            logger.info("default html file was not found")

    def handle_response(self, response):
        try:
            content_type = response.headers["Content-Type"]
            if "text/html" in content_type:
                content = helpers.replace(response.body, self.replace_path)
            elif "javascript" in content_type:
                body = "location.origin +'" + self.replace_path + "' "
                content = response.body.replace(b"location.origin", body.encode())
            else:
                # Probably binary response, send it directly.
                content = response.body
            self.set_header("Content-Type", content_type)
            self.write(content)
            self.finish()
        except Exception as e:
            logger.error(str(e))
            raise e

def setup_handlers(web_app):
    # init_logger()
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern_sparkui = url_path_join(base_url, "sparkui", "ui")
    handlers = [(route_pattern_sparkui, SparkUIRouteHandler)]
    web_app.add_handlers(host_pattern, handlers)