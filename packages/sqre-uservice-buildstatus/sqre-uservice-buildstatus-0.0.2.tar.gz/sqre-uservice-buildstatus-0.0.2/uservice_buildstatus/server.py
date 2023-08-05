#!/usr/bin/env python
"""Retrieve build data from ci.lsst.codes"""
import requests
from apikit import APIFlask as apf
from apikit import BackendError
from flask import jsonify, request


def server(run_standalone=False):
    """Create the app and then run it."""
    # Add "/buildstatus" for mapping behind api.lsst.codes
    app = apf(name="uservice-buildstatus",
              version="0.0.1",
              repository="https://github.com/sqre-lsst/" +
              "sqre-uservice-buildstatus",
              description="API wrapper for build status",
              route=["/", "/buildstatus"],
              auth={"type": "basic",
                    "data": {"username": "",
                             "password": ""}})
    app.config["SESSION"] = None

    @app.route("/<buildname>")
    @app.route("/buildstatus/<buildname>")
    # pylint: disable=unused-variable
    def get_buildstatus(buildname):
        """
        Proxy for ci.lsst.codes.  We expect the incoming request to have
        Basic Authentication headers.
        """
        inboundauth = None
        if request.authorization is not None:
            inboundauth = request.authorization
            currentuser = app.config["AUTH"]["data"]["username"]
            currentpw = app.config["AUTH"]["data"]["password"]
            if currentuser != inboundauth.username or \
               currentpw != inboundauth.password:
                _reauth(app, inboundauth.username, inboundauth.password)
        else:
            raise BackendError(reason="Unauthorized", status_code=403,
                               content="No authorization provided.")
        session = app.config["SESSION"]
        url = "https://ci.lsst.codes/job/" + buildname + "/api/json"
        resp = session.get(url)
        if resp.status_code == 403:
            # Try to reauth
            _reauth(app, inboundauth.username, inboundauth.password)
            session = app.config["SESSION"]
            resp = session.get(url)
        if resp.status_code == 200:
            return resp.text
        else:
            raise BackendError(reason=resp.reason,
                               status_code=resp.status_code,
                               content=resp.text)

    @app.route("/")
    def root_route():
        """Needed for Ingress health check."""
        return "OK"

    @app.errorhandler(BackendError)
    # pylint: disable=unused-variable
    def handle_invalid_usage(error):
        """Custom error handler."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    if run_standalone:
        app.run(host='0.0.0.0', threaded=True)


def _reauth(app, username, password):
    """Get a session with authentication data"""
    session = requests.Session()
    session.auth = (username, password)
    app.config["SESSION"] = session


def standalone():
    """Entry point for running as its own executable."""
    server(run_standalone=True)

if __name__ == "__main__":
    standalone()
