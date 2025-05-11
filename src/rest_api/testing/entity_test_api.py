
import json
from typing import Optional

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)


class EntityTestApi:
    entity = None

    def __init__(self, client, user=None):
        self.client = client
        self.user = user

        if self.user:
            self.client.force_authenticate(self.user)

    def get_entity(self, entity_id, expected_code=HTTP_200_OK):
        resp = self.client.get(
            path=reverse(f'{self.entity}-detail', kwargs={
                'pk': entity_id,
            }),
        )
        assert resp.status_code == expected_code, resp.content
        return json.loads(resp.content)

    def get_entities(self, filters=None, results=True, expected_code: int = HTTP_200_OK):
        if filters is None:
            filters = {}

        resp = self.client.get(
            path=reverse(f'{self.entity}-list'),
            data=filters,
        )
        assert resp.status_code == expected_code, resp.content

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('results', {})

        return resp_json

    def create_entity(self, entity_data, expected_code: Optional[int] = HTTP_201_CREATED, extra_data=None,
                      content_type='application/json'):
        if extra_data is not None:
            entity_data.update(**extra_data)

        resp = self.client.post(
            path=reverse(f'{self.entity}-list'),
            data=json.dumps(entity_data, cls=DjangoJSONEncoder) if content_type == 'application/json' else entity_data,
            content_type=content_type,
        )
        assert resp.status_code == expected_code, f'expected: {expected_code}, actual: {resp.status_code}. Content: {resp.content}'
        if expected_code == HTTP_204_NO_CONTENT:
            return

        assert resp.content

        return json.loads(resp.content)

    def update_entity(self, entity_id, entity_data, url_field: str = 'pk', partial=False, expected_code=HTTP_200_OK):
        client_method = self.client.put
        if partial:
            client_method = self.client.patch

        resp = client_method(
            path=reverse(f'{self.entity}-detail', kwargs={
                url_field: entity_id,
            }),
            data=json.dumps(entity_data, cls=DjangoJSONEncoder),
            content_type='application/json'
        )

        if expected_code == HTTP_204_NO_CONTENT:
            return

        assert resp.status_code == expected_code, resp.content
        return json.loads(resp.content)

    def delete_entity(self, entity_id, expected_code=HTTP_204_NO_CONTENT):
        resp = self.client.delete(
            path=reverse(f'{self.entity}-detail', kwargs={
                'pk': entity_id,
            }),
        )
        assert resp.status_code == expected_code, resp.content

    def list_get_action(self, action, results=False, expected_code=HTTP_200_OK, kwargs=None):
        url = reverse(f'{self.entity}-{action}', kwargs=kwargs)

        resp = self.client.get(path=url)
        assert resp.status_code == expected_code, resp.content

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('items', {})

        return resp_json

    def list_post_action(self, action, data, results=False, content_type='application/json', expected_code=HTTP_200_OK):
        path = reverse(f'{self.entity}-{action}')

        resp = self.client.post(
            path=path,
            data=json.dumps(data, cls=DjangoJSONEncoder) if content_type == 'application/json' else data,
            content_type=content_type,
        )
        assert resp.status_code == expected_code, resp.content

        if expected_code == HTTP_204_NO_CONTENT:
            return

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('items', {})

        return resp_json

    def list_patch_action(self, action, data, results=False, content_type='application/json',
                          expected_code=HTTP_200_OK):
        path = reverse(f'{self.entity}-{action}')
        resp = self.client.patch(
            path=path,
            data=json.dumps(data, cls=DjangoJSONEncoder) if content_type == 'application/json' else data,
            content_type=content_type,
        )

        assert resp.status_code == expected_code, resp.content

        if expected_code == HTTP_204_NO_CONTENT:
            return

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('items', {})

        return resp_json

    def list_put_action(self, action, data, results=False, content_type='application/json',
                          expected_code=HTTP_200_OK, url_kwargs=None):
        path = reverse(f'{self.entity}-{action}', kwargs=url_kwargs)
        resp = self.client.put(
            path=path,
            data=json.dumps(data, cls=DjangoJSONEncoder) if content_type == 'application/json' else data,
            content_type=content_type,
        )

        assert resp.status_code == expected_code, resp.content

        if expected_code == HTTP_204_NO_CONTENT:
            return

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('items', {})

        return resp_json

    def post_action(self, action, data, results=False, expected_code=HTTP_200_OK, **kwargs):
        url = reverse(f'{self.entity}-{action}')

        resp = self.client.post(path=url, data=data, **kwargs)

        assert resp.status_code == expected_code, f'expected: {expected_code}, actual: {resp.status_code}. Content: {resp.content}'

        if expected_code == HTTP_204_NO_CONTENT:
            return

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('results', {})

        return resp_json

    def detail_get_action(self, action, pk, query=None, results=False, expected_code=HTTP_200_OK):
        path = reverse(f'{self.entity}-{action}', kwargs={'pk': pk})

        query = query or {}

        resp = self.client.get(
            path=path,
            data=query,
        )
        assert resp.status_code == expected_code, resp.content

        if expected_code == HTTP_204_NO_CONTENT:
            return

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('results', {})

        return resp_json

    def detail_put_action(self, action, pk, data, results=False, expected_code=HTTP_200_OK):
        path = reverse(f'{self.entity}-{action}', kwargs={'pk': pk})
        resp = self.client.put(
            path=path,
            data=json.dumps(data, cls=DjangoJSONEncoder),
            content_type='application/json'
        )
        assert resp.status_code == expected_code, f'expected: {expected_code}, actual: {resp.status_code}. Content: {resp.content}'

        if resp.content:
            resp_json = json.loads(resp.content)
        else:
            resp_json = resp.content

        if results and resp.content:
            resp_json = resp_json.get('results', {})

        return resp_json

    def detail_put_action_custom_kwargs(self, action, custom_kwargs, data, results=False, expected_code=HTTP_200_OK):
        path = reverse(f'{self.entity}-{action}', kwargs=custom_kwargs)
        resp = self.client.put(
            path=path,
            data=data,
            media_type='multipart/form-data'
        )
        assert resp.status_code == expected_code, resp.content

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('results', {})

        return resp_json

    def detail_patch_action(self, action, pk, data, results=False, expected_code=HTTP_200_OK):
        path = reverse(f'{self.entity}-{action}', kwargs={'pk': pk})
        resp = self.client.patch(
            path=path,
            data=json.dumps(data, cls=DjangoJSONEncoder),
            content_type='application/json'
        )
        assert resp.status_code == expected_code, resp.content

        if expected_code == HTTP_204_NO_CONTENT:
            return

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('results', {})

        return resp_json

    def detail_post_action(self, action, pk, data, results=False, expected_code=HTTP_200_OK):
        path = reverse(f'{self.entity}-{action}', kwargs={'pk': pk})
        resp = self.client.post(
            path=path,
            data=json.dumps(data, cls=DjangoJSONEncoder),
            content_type='application/json'
        )

        if expected_code == HTTP_204_NO_CONTENT:
            return

        assert resp.status_code == expected_code, resp.content

        if expected_code == HTTP_204_NO_CONTENT:
            return

        resp_json = json.loads(resp.content)

        if results:
            resp_json = resp_json.get('results', {})

        return resp_json
