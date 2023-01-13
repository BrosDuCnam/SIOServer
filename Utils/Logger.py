import Dataclasses.Webhooks as Webhooks
import pandas as pd
import Dataclasses.Webhooks as Webhooks

from discordwebhook import Discord

from pygit2 import Repository, Commit

discord = Discord(
    url="https://discord.com/api/webhooks/1063555763047501845/PXyAjsTyDs4DKlWApJq6-374z3HyX-xsjfulEGCN65f8GOyNP0Tn3gN1iJ-_G3XbBrWf")


def get_commit_data() -> dict[str, str | int]:
    repo = Repository(".")
    head = repo.head

    git_branch = head.shorthand
    commit = repo[head.target]
    commit_id = commit.hex
    commit_short_id = commit.hex[:7]
    commit_name = commit.message.splitlines()[0]
    commit_description = commit.message.splitlines()[0]

    # iso 8601 format string (YYYY-MM-DDTHH:MM:SSZ)
    timestamp = pd.to_datetime(commit.commit_time, unit="s").isoformat()

    return {
        "branch": git_branch,
        "commit_id": commit_id,
        "commit_short_id": commit_short_id,
        "commit_name": commit_name,
        "commit_description": commit_description,
        "timestamp": timestamp
    }


def log(*message):
    if len(message) == 0:
        return

    data: dict[str, str | int] = get_commit_data()

    if isinstance(message[0], str):
        if message[0].lower() in Webhooks.webhooks:
            discord.post(embeds=Webhooks.webhook_format(message[0].lower(), data))
            return

    data["log"] = '_'.join(str(i) for i in message)

    discord.post(embeds=Webhooks.webhook_format("log", data))
