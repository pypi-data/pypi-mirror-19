from rest_framework import status
from rest_framework.response import Response


class CrudSerializersMixin:
    """
    Allows you set a specific serializer for each ViewSet method.
    """

    retrieve_serializer = None
    list_serializer = None
    update_serializer = None
    create_serializer = None
    destroy_serializer = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.retrieve_serializer:
            return self.retrieve_serializer
        elif self.action == 'list' and self.list_serializer:
            return self.list_serializer
        elif self.action == 'update' and self.update_serializer:
            return self.update_serializer
        elif self.action == 'partial_update' and self.update_serializer:
            return self.update_serializer
        elif self.action == 'create' and self.create_serializer:
            return self.create_serializer
        elif self.action == 'destroy' and self.destroy_serializer:
            return self.destroy_serializer

        return self.serializer_class


class BulkCreateMixin:
    """
    Allows you to pass an array of objects to the create method. Serializers with many=true
    apparently use all or nothing validation, validated_data will be empty even if only a single
    record has an error. If we want partial saves we can write our own logic. For now we will
    stick with all or nothing.

    If using this mixin with other mixins that override the create method be sure this
    mixin comes after all other mixins that override create in the inheritance chain.
    """

    def bulk_create(self, request, *args, **kwargs):
        preview = True if self.request.query_params.get(r'preview', 'false') == 'true' else False

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        return_status = status.HTTP_200_OK

        if preview is False:
            self.perform_create(serializer)
            return_status = status.HTTP_201_CREATED

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=return_status, headers=headers)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            return self.bulk_create(request, *args, **kwargs)

        return super(BulkCreateMixin, self).create(request, *args, **kwargs)
