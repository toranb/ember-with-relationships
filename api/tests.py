import json
import uuid

from django.test import TestCase
from api.models import Speaker, Tag, Session

def add_sessions_speakers_and_tags():
    first_tag = Tag(pk=uuid.uuid4(), description="javascript")
    last_tag = Tag(pk=uuid.uuid4(), description="python")
    first_tag.save()
    last_tag.save()
    first_session = Session(pk=uuid.uuid4(), name="first")
    last_session = Session(pk=uuid.uuid4(), name="last")
    first_session.save()
    last_session.save()
    first_session.tags.add(first_tag)
    last_session.tags.add(last_tag)
    first_session.save()
    last_session.save()
    first_speaker = Speaker(pk=uuid.uuid4(), name="foo", session=first_session)
    last_speaker = Speaker(pk=uuid.uuid4(), name="bar", session=last_session)
    first_speaker.save()
    last_speaker.save()
    return first_session, last_session, first_speaker, last_speaker, first_tag, last_tag

class SessionTests(TestCase):

    def setUp(self):
        self.first_session, self.last_session, self.first_speaker, self.last_speaker, self.first_tag, self.last_tag = add_sessions_speakers_and_tags()

    def test_http_get_will_retrieve_list_of_sessions_and_return_200(self):
        response = self.client.get("/api/sessions/")
        sessions = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(sessions), 2)

    def test_http_get_will_return_session_json_with_all_the_attributes_on_the_model(self):
        response = self.client.get("/api/sessions/")
        sessions = json.loads(response.content)
        self.assertEqual(sessions[0]["name"], "first")
        self.assertEqual(sessions[1]["name"], "last")

    def test_http_get_will_return_list_of_session_json_including_speaker_ids(self):
        response = self.client.get("/api/sessions/")
        sessions = json.loads(response.content)
        self.assertEqual(len(sessions[0]["speakers"]), 1)
        self.assertEqual(sessions[0]["speakers"][0]["id"], str(self.first_speaker.pk))
        self.assertEqual(sessions[0]["speakers"][0]["name"], self.first_speaker.name)
        self.assertEqual(len(sessions[1]["speakers"]), 1)
        self.assertEqual(sessions[1]["speakers"][0]["id"], str(self.last_speaker.pk))
        self.assertEqual(sessions[1]["speakers"][0]["name"], self.last_speaker.name)

    def test_http_get_will_return_json_with_attrs_with_valid_pk(self):
        response = self.client.get("/api/sessions/{}/".format(self.first_session.pk))
        self.assertEqual(response.status_code, 200)
        session = json.loads(response.content)
        self.assertEqual(session["name"], self.first_session.name)
        self.assertEqual(len(session["speakers"]), 1)
        self.assertEqual(session["speakers"][0]["id"], str(self.first_speaker.pk))
        self.assertEqual(session["speakers"][0]["name"], self.first_speaker.name)

    def test_http_get_will_return_404_when_invalid_pk(self):
        response = self.client.get("/api/sessions/999999999999999999/")
        self.assertEqual(response.status_code, 404)

    def test_http_delete_will_remove_last_session_and_return_204(self):
        response = self.client.delete("/api/sessions/{}/".format(self.last_session.pk))
        self.assertEqual(response.status_code, 204)
        response = self.client.get("/api/sessions/{}/".format(self.last_session.pk))
        self.assertEqual(response.status_code, 404)

    def test_http_post_will_create_session_and_return_201(self):
        new_session_pk = str(uuid.uuid4())
        first_new_speaker_pk = str(uuid.uuid4())
        last_new_speaker_pk = str(uuid.uuid4())
        payload = {"id": new_session_pk, "name": "hello", "speakers": [{"id": first_new_speaker_pk, "name": "1"},{"id": last_new_speaker_pk, "name": "2"}]}
        response = self.client.post("/api/sessions/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        session = json.loads(response.content)
        self.assertEqual(session["id"], new_session_pk)
        self.assertEqual(session["name"], "hello")
        self.assertEqual(len(session["speakers"]), 2)
        expected_speaker_json = [{"id": first_new_speaker_pk, "name": "1"},{"id": last_new_speaker_pk, "name": "2"}]
        self.assertItemsEqual(session["speakers"], expected_speaker_json)

    def test_http_put_will_update_first_session_name_and_return_200(self):
        data = {"id": str(self.first_session.pk), "name": "updated name", "speakers": []}
        response = self.client.put("/api/sessions/{}/".format(self.first_session.pk), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        session = json.loads(response.content)
        self.assertEqual(session["name"], "updated name")

    def test_http_put_will_add_speaker_when_session_had_non_to_begin_with(self):
        new_session_pk = str(uuid.uuid4())
        payload = {"id": new_session_pk, "name": "put", "speakers": []}
        response = self.client.post("/api/sessions/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        first_new_speaker_pk = str(uuid.uuid4())
        last_new_speaker_pk = str(uuid.uuid4())
        data = {"id": new_session_pk, "name": "another one", "speakers": [{"id": first_new_speaker_pk, "name": "1"}, {"id": last_new_speaker_pk, "name": "2"}]}
        response = self.client.put("/api/sessions/{}/".format(new_session_pk), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        session = json.loads(response.content)
        self.assertEqual(session["name"], "another one")
        self.assertEqual(len(session["speakers"]), 2)
        expected_speaker_json = [{"id": first_new_speaker_pk, "name": "1"},{"id": last_new_speaker_pk, "name": "2"}]
        self.assertItemsEqual(session["speakers"], expected_speaker_json)
