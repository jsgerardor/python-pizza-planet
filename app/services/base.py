from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request
from typing import Any, List, Optional, Sequence

from app.controllers.base import BaseController

class BaseService: 

    def create(controller: BaseController):
        blueprint, error = controller.create(request.json)
        response = blueprint if not error else {'error': error}  
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    def update(controller: BaseController):
        result, error = controller.update(request.json)
        response = result if not error else {'error': error}  
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    def get_by_id(controller: BaseController, _id: int):
        result, error = controller.get_by_id(_id)
        response = result if not error else {'error': error}  
        status_code = 200 if result else 404 if not error else 400
        return jsonify(response), status_code

    def get_all(controller: BaseController):
        result, error = controller.get_all()
        response = result if not error else {'error': error}  
        status_code = 200 if result else 404 if not error else 400
        return jsonify(response), status_code