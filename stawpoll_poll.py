import requests, json
import asyncio
import strawpoll


async def make_strawpoll(poll):
    api = strawpoll.API()
    data = strawpoll.Poll(poll[0],poll[1])
    await api.submit_poll(data)
    data = await api.submit_poll(data)
    return data
