# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)


class Accessor(object):
    def __init__(self, resolver):
        self.resolver = resolver

    @property
    def dispatcher(self):
        return self.resolver.dispatcher

    def definitions(self, d):
        return d.get("definitions") or {}

    def properties(self, d):
        return d.get("properties") or {}

    def update_options_pre_properties(self, d, opts):
        for name in d.get("required") or []:
            opts[name]["required"] = True
        return opts

    def update_option_on_property(self, c, field, opts):
        if "description" in field:
            opts["description"] = field["description"]
        if self.resolver.has_many(field):
            logger.debug("    resolve: many=True")
            opts["many"] = True
        if "default" in field:
            logger.debug("    resolve: default=%r", field["default"])
            opts["missing"] = self.dispatcher.handle_default(c, field["default"], field)  # xxx
        if field.get("readOnly", False):
            logger.debug("    resolve: dump_only=True")
            opts["dump_only"] = True

        validators = self.resolver.resolve_validators_on_property(c, field)
        if validators:
            opts["validate"] = validators
        return opts
