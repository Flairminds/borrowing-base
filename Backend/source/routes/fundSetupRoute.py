from flask import Blueprint

from source.controllers import fundSetupController

fundSetup_blueprint = Blueprint("fundSetup_blueprint", __name__)


@fundSetup_blueprint.route("/get_concentration_tests", methods=["POST"])
def get_concentration_tests():
    return fundSetupController.get_concentration_tests()


@fundSetup_blueprint.route("/change_limit_percent", methods=["POST"])
def update_limit():
    return fundSetupController.update_limit()
