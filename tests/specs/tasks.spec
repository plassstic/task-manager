# taskmgr-plassstic api testing

## Scenario: create task; status=200
* start-ctx
* create task: name: "test", desc: "desc"
* status: "200"
* check: id
* check: name: "test"
* remember: id

## Scenario: get task from mem; status=200
* prev-ctx
* get: rmb task
* status: "200"
* check: name: "test"

## Scenario: update task from mem; status=200
* prev-ctx
* update rmb task: name: "upd", status: "in_progress"
* status: "200"
* check: name: "upd"
* check: status: "in_progress"

## Scenario: get-list; status=200
* prev-ctx
* get-list: page: "1", page_size: "10"
* status: "200"
* validate: payload ~ list of tasks

## Scenario: delete task from mem; status=200
* prev-ctx
* delete: rmb task
* status: "200"
* check: payload ~ true

## Scenario: get by random guid; status=404
* prev-ctx
* get task by random guid
* status: "404"
* err.code: "not_found"

## Scenario: inv payload; status=422
* prev-ctx
* create invalid task
* status: "422"
* err.code: "validation_error"

## Scenario: perftest
* prev-ctx
* perftest: get-list page: "1", page_size: "10"
* perftest with threshold "250" ms
