import time
import uuid
from typing import Any

import httpx
from getgauge.python import Messages, data_store, step

api_client = httpx.Client(base_url="http://localhost:8000/api/tasks", timeout=10.0)

def _last_resp() -> httpx.Response:
    return data_store.spec.get("lastresp")


def _set_last_resp(resp: httpx.Response):
    data_store.spec["lastresp"] = resp


def _set(key: str, value: Any):
    setattr(data_store.spec, key, value)


def _get(key: str):
    return getattr(data_store.spec, key)


@step("start-ctx")
def start_ctx():
    pass


@step("prev-ctx")
def prev_ctx():
    pass


@step("create task: name: <name>, desc: <desc>")
def create_task(name: str, desc: str) -> None:
    _set_last_resp(api_client.post("/", json={"name": name, "description": desc}))


@step("create invalid task")
def create_invalid_task():
    _set_last_resp(api_client.post("/", json={"description": "123"}))


@step("get: rmb task")
def get_rmb_task():
    _set_last_resp(api_client.get(f"/{_get('task_id')}"))


@step("update rmb task: name: <name>, status: <status>")
def update_task(name: str, status: str):
    _set_last_resp(api_client.patch(
        f"/{_get('task_id')}",
        json={"name": name, "status": status}
    ))


@step("get-list: page: <page>, page_size: <page_size>")
def list_tasks(page: str, page_size: str):
    _set_last_resp(api_client.get("/", params={"page": page, "page_size": page_size}))


@step("delete: rmb task")
def delete_task():
    _set_last_resp(api_client.delete(f"/{_get('task_id')}"))


@step("get task by random guid")
def fetch_rand_guid():
    _set_last_resp(api_client.get(f"/{uuid.uuid4()}"))


@step("perftest: get-list page: <page>, page_size: <page_size>")
def perftest_getlist(page: str, page_size: str):
    start = time.perf_counter()
    resp = api_client.get("/", params={"page": page, "page_size": page_size})
    _set("elapsed_ms", (time.perf_counter() - start) * 1000.0)
    _set_last_resp(resp)


@step("status: <code>")
def check_resp_status(code: str):
    resp = _last_resp()
    assert resp is not None, "no resp in data_store"
    assert resp.status_code == int(code), f"Expected {code}, got {resp.status_code}, body={resp.text}"


@step("check: id")
def check_id(): 
    pl = _last_resp().json()["payload"]
    assert "id" in pl and pl["id"] is not None, "Task id missing"


@step("check: name: <name>")
def check_name(name: str):
    assert _last_resp().json()["payload"]["name"] == name


@step("check: status: <status>")
def check_status(status: str):
    resp_json = _last_resp().json()
    assert resp_json["payload"]["status"] == status


@step("remember: id")
def remember_id():
    task_id = _last_resp().json()["payload"]["id"]
    _set("task_id", task_id)


@step("validate: payload ~ list of tasks")
def vld_list_tasks():
    resp_json = _last_resp().json()
    assert isinstance(resp_json["payload"], list)
    required = {"id", "name", "description", "status", "created_at", "updated_at"}
    for item in resp_json["payload"]:
        assert required.issubset(item.keys()), f"Task missing keys: {required - set(item.keys())}"


@step("check: payload ~ true")
def payload_is_true():
    resp_json = _last_resp().json()
    assert resp_json["payload"] is True


@step("err.code: <code>")
def error_code_is(code: str):
    resp_json = _last_resp().json()
    assert resp_json["error"]["error"] == code or resp_json["error"].get("error_code") == code


@step("perftest with threshold <threshold> ms")
def perftest_thr(threshold: str):
    elapsed_ms = _get("elapsed_ms")
    assert elapsed_ms is not None, "no perftest in data_store"
    assert elapsed_ms <= float(threshold), f"perftest: {elapsed_ms:.2f} ms > {threshold} ms"
    Messages.write_message(f"perftest: {elapsed_ms:.2f} ms <= {threshold} ms")
