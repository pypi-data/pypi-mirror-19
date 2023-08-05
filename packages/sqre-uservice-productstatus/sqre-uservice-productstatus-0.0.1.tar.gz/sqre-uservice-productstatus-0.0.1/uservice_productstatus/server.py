#!/usr/bin/env python
"""Retrieve QA metrics and report deviation"""
import json
# Python 2/3 compatibility
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError
from threading import Thread, Lock
import requests
from apikit import APIFlask as apf
from apikit import BackendError
from flask import jsonify


def server(run_standalone=False):
    """Create the app and then run it."""
    # Add "/productstatus" for mapping behind api.lsst.codes
    baseuri = "https://keeper.lsst.codes"
    app = apf(name="uservice-productstatus",
              version="0.0.1",
              repository="https://github.com/sqre-lsst/" +
              "sqre-uservice-productstatus",
              description="API wrapper for product status",
              route=["/", "/productstatus"],
              auth={"type": "none"})

    # Linter can't understand decorators.
    @app.errorhandler(BackendError)
    # pylint: disable=unused-variable
    def handle_invalid_usage(error):
        """Custom error handler."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Linter can't understand decorators.
    # pylint: disable=unused-variable
    @app.route("/")
    def healthcheck():
        """Default route to keep Ingress controller happy."""
        return "OK"

    @app.route("/productstatus")
    @app.route("/productstatus/")
    @app.route("/productstatus/<product>")
    def get_productstatus(product=None):
        """
        Iterate through products and editions to determine endpoint health.
        """
        if product is None:
            productlist = _get_product_list(baseuri)
        else:
            productlist = [baseuri + "/products/" + product]
        responses = _check_endpoints(productlist, baseuri)
        response = jsonify(responses)
        rsc = _get_max_status_code(responses)
        response.status_code = rsc
        return response

    if run_standalone:
        app.run(host='0.0.0.0', threaded=True)


def _get_max_status_code(responses):
    """Get the largest status code we encountered in the process."""
    stc = []
    for prod in responses:
        for edt in responses[prod]["editions"]:
            stc.append(responses[prod]["editions"][edt]["status_code"])
    return max(stc)


def _get_product_list(baseuri):
    """Get the available products."""
    url = baseuri + "/products"
    resp = requests.get(url)
    _check_response(resp)
    rdict = json.loads(resp.text)
    return rdict["products"]


def _check_response(resp):
    """Create an error if you don't get an HTTP 2xx back."""
    if resp.status_code < 200 or resp.status_code > 299:
        raise BackendError(reason=resp.reason,
                           status_code=resp.status_code,
                           content=resp.text)


def _check_endpoints(productlist, baseuri):
    """Get status for each endpoint and edition."""
    # In theory, the GIL makes the dictionary threadsafe already.
    #  In practice, let's make it explicit.
    mutex = Lock()
    mutex.acquire()
    try:
        responses = {}
    finally:
        mutex.release()
    productthreads = []
    for product in productlist:
        thd = Thread(target=_check_product,
                     args=(baseuri, product, mutex, responses))
        productthreads.append(thd)
        thd.start()
    for thd in productthreads:
        thd.join()
    return responses


def _check_product(baseuri, product, mutex, responses):
    """Check a given product and its editions."""
    # pylint: disable=too-many-locals
    prodname = ""
    resp = requests.get(product)
    try:
        _check_response(resp)
        # Only store successful URL fetches for the actual documents.
        #  Store failures for whatever failed.
        rdict = json.loads(resp.text)
        puburl = rdict["published_url"]
        prodname = rdict["slug"]
        mutex.acquire()
        try:
            responses[prodname] = {"url": puburl,
                                   "editions": {}}
        finally:
            mutex.release()
        edurl = baseuri + "/products/" + prodname + "/editions"
        resp = requests.get(edurl)
        _check_response(resp)
        edict = json.loads(resp.text)
        edition = edict["editions"]
        edthreads = []
        for edt in edition:
            thd = Thread(target=_check_edition,
                         args=(edt, prodname, puburl, mutex, responses))
            edthreads.append(thd)
            thd.start()
        for thd in edthreads:
            thd.join()
    except (BackendError, JSONDecodeError) as exc:
        if isinstance(exc, JSONDecodeError):
            resp.status_code = 500
            resp.reason = "JSON Decode Error"
            resp.text = "Could not decode: " + resp.text
        rurl = resp.url
        if prodname == "":
            prodname = rurl
        mutex.acquire()
        try:
            if prodname not in responses:
                responses[prodname] = {"url": None,
                                       "editions": {rurl: {}}}
        finally:
            mutex.release()
        badprod = {"url": rurl,
                   "status_code": resp.status_code}
        mutex.acquire()
        try:
            responses[prodname]["editions"][rurl] = badprod
        finally:
            mutex.release()


def _check_edition(edition, prodname, puburl, mutex, responses):
    """Check a given edition."""
    try:
        resp = requests.get(edition)
        _check_response(resp)
        edobj = json.loads(resp.text)
    except (BackendError, JSONDecodeError) as exc:
        if isinstance(exc, JSONDecodeError):
            resp.status_code = 500
            resp.reason = "JSON Decode Error"
            resp.text = "Could not decode: " + resp.text
        baded = {"url": resp.url,
                 "status_code": resp.status_code}
        # Fake edition name since we don't know it
        mutex.acquire()
        try:
            responses[prodname]["editions"][resp.url] = baded
        finally:
            mutex.release()
    edpuburl = edobj["published_url"]
    ver = edobj["slug"]
    if edobj["build_url"] is None:
        if edpuburl == puburl:
            mutex.acquire()
            try:
                # Never built master; remove top-level published_url
                responses[prodname]["url"] = None
            finally:
                mutex.release()
        return  # Do not check if never built.
    resp = requests.get(edpuburl)
    edres = {"url": resp.url,
             "status_code": resp.status_code}
    mutex.acquire()
    try:
        responses[prodname]["editions"][ver] = edres
    finally:
        mutex.release()


def standalone():
    """Entry point for running as its own executable."""
    server(run_standalone=True)

if __name__ == "__main__":
    standalone()
