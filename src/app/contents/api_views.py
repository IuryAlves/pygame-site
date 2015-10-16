# coding: utf-8

import json
from flask import Blueprint, jsonify, request, make_response
import usecase

contents_api = Blueprint("contents_api", __name__, url_prefix="/api/contents")


@contents_api.route("/add", methods=["POST"])
def add():
    data = json.loads(request.data)
    usecase.add_content(**data)

    return jsonify(data={})


@contents_api.route("/get", methods=["GET"])
def get():
    contents = usecase.get_contents()

    data = [content.to_dict() for content in contents]
    return jsonify(data=data)


@contents_api.route("/delete", methods=["POST"])
def delete():
    type_ = json.loads(request.data)["type_"]

    usecase.delete_content(type_)
    return jsonify(data={})


@contents_api.route("/edit", methods=["POST"])
def edit():
    data = json.loads(request.data)
    type_ = data.pop("type_")
    edited_content = usecase.edit_content(type_, **data)

    if edited_content is None:
        response = make_response("content object does not exists")
        response.status_code = 500
        return response
    return jsonify(data=edited_content.to_dict())
