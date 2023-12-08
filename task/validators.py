def task_validators(data):
    data_sorted = sorted(data, key=lambda x: x["time to send"])
    task_id_can_done = []
    for task in data_sorted:
        pre_tasks = [x for x in task["pre-tasks"] if x not in task_id_can_done]
        if not pre_tasks:
            task_id_can_done.append(task["id"])
        else:
            return False
    return True
