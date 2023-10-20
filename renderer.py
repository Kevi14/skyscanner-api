from json import JSONEncoder
from rest_framework.renderers import JSONRenderer
from math import ceil
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import APIException

from config import API_LIST_DEFAULT_PAGE_SIZE, API_LIST_MAX_PAGE_SIZE


class ResponseEnvelopeRenderer(JSONRenderer):
    """
    Renders response in envelope.
    """
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # OPTIONS method -> return raw description

        if renderer_context["request"].method == "OPTIONS":
            return JSONEncoder(indent=2).encode(data)

        # return error object
        if isinstance(data, dict) and data.get("error"):
            return JSONEncoder(indent=2).encode(data)

        final_response = {
            "pagination": {
                "page": None,
                "size": None,
                "totalPages": None,
                "totalElements": None,
            },
            "error": None,
            "data": None,
        }

        if isinstance(data, list):
            final_response["data"] = data

        if data is None:
            return JSONEncoder(indent=2).encode(final_response)

        if (isinstance(data, dict) and (
                data.get("results")
                or data.get("results") is not None
                and isinstance(data["results"], list
                               )
        )
        ):

            final_response["data"] = data["results"]

            try:
                final_response["pagination"]["page"] = int(
                    renderer_context["request"].GET["page"]
                )
            except MultiValueDictKeyError:
                final_response["pagination"]["page"] = 1
            try:
                final_response["pagination"]["size"] = int(
                    renderer_context["request"].GET["size"]
                )
            except MultiValueDictKeyError:
                final_response["pagination"]["size"] = API_LIST_DEFAULT_PAGE_SIZE
            except ValueError:
                raise APIException("Invalid pagination size")

            if final_response["pagination"]["size"] > API_LIST_MAX_PAGE_SIZE:
                final_response["pagination"]["size"] = API_LIST_MAX_PAGE_SIZE
            elif final_response["pagination"]["size"] <= 0:
                raise APIException("Pagination size out of range.")

            final_response["pagination"]["totalPages"] = ceil(
                data.get("count", len(data.get("results"))) / final_response["pagination"]["size"]
            )
            final_response["pagination"]["totalElements"] = data.get("count", len(data.get("results")))

        else:
            final_response["data"] = data

        return JSONEncoder(indent=2).encode(final_response)
