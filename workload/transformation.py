def overall_transform(data):
    overall_hours = data.groupby(["billable"]).agg(
        hours=("hours", "sum")
    ).reset_index()
    return overall_hours


def member_transform(data):
    member_hours = data.groupby(["name", "billable"]).agg(
        hours=("hours", "sum")
    ).reset_index()
    return member_hours


def client_breakdown_transform(data):
    client_billable_hours = data.groupby(["client", "billable"]).agg(
        hours=("hours", "sum")
    ).reset_index()
    return client_billable_hours


def task_transform(data):
    task_hours = data.groupby(["client", "task", "billable"]).agg(
        hours=("hours", "sum")
    ).reset_index().sort_values(
        by=["billable", "hours"],
        ascending=[True, False]
    )
    return task_hours
