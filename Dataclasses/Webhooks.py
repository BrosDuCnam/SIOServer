import datetime

webhooks: dict[str, list: object] = {
    "starting":
        [
            {
                "title": "Starting",
                "color": 16776960,
                "fields": [
                    {"name": "commit : {commit_short_id}", "value": "{commit_name}"},
                    {"name": "branch :", "value": "{branch}"}
                ],
                "footer": {"text": "{commit_id}"},
            },
        ],
    "started":
        [
            {
                "title": "Started",
                "color": 5763719,
                "fields": [
                    {"name": "commit : {commit_short_id}", "value": "{commit_name}"},
                    {"name": "branch :", "value": "{branch}"}
                ],
                "footer": {"text": "{commit_id}"},
            },
        ],
    "stopped":
        [
            {
                "title": "Stopped",
                "color": 15548997,
                "fields": [
                    {"name": "commit : {commit_short_id}", "value": "{commit_name}"},
                    {"name": "branch :", "value": "{branch}"}
                ],
                "footer": {"text": "{commit_id}"},
            },
        ],
    "log":
        [
            {
                "title": "Log",
                "description": "{log}",
                "color": 16776960,
                "fields": [
                    {"name": "commit : {commit_short_id}", "value": "{commit_name}"},
                    {"name": "branch :", "value": "{branch}"}
                ],
                "footer": {"text": "{commit_id}"},
            },
        ]
}


def webhook_format(webhook_name: str, data: dict[str, str]) -> list[dict[str, str]]:
    """Format a webhook with data

    :param webhook_name: name of the webhook
    :param data: data to format the webhook
    :return: formatted webhook.
    """

    webhook = webhooks[webhook_name]

    for index, embed in enumerate(webhook):
        for field in embed["fields"]:
            field["name"] = field["name"].format(**data)
            field["value"] = field["value"].format(**data)

        embed["footer"]["text"] = embed["footer"]["text"].format(**data)
        embed["title"] = embed["title"].format(**data)
        embed["timestamp"] = data["timestamp"]

        if "description" in embed:
            embed["description"] = embed["description"].format(**data)

    return webhook
