from plone.distribution.api import distribution as dist_api
from plone.restapi.services.system.get import SystemGet as BaseService

import pkg_resources


plone_distribution_version = pkg_resources.require("plone.distribution")[0].version


class SystemGet(BaseService):
    def distribution_info(self) -> str:
        """Get distribution information if site was created with a distribution."""
        info = ""
        portal = self.context
        report = dist_api.get_creation_report(portal)
        if report:
            dist_name = report.name
            try:
                dist_title = dist_api.get(dist_name).title
            except ValueError:
                dist_title = "Uninstalled"
            info = f"{dist_title} ({dist_name})"
        return info

    def reply(self):
        response = super().reply()
        response["plone.distribution"] = plone_distribution_version
        distribution_info = self.distribution_info()
        if distribution_info:
            response["distribution"] = distribution_info
        return response
