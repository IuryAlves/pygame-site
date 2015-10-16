# coding: utf-8

from models import Content


def delete_all_contents():
    for content in get_contents():
        delete_content(content.type_)


def get_contents():
    return Content.get_contents()


def delete_content(type_):
    return Content.delete_content(type_)


def add_content(data, type_):
    content = Content(data, type_)

    return Content.save_content(content)


def edit_content(type_, **kwargs):
    data = kwargs.get("data")

    content = Content.get_content_by_type(type_)

    if content is None:
        return None

    if data is not None:
        content.data = data

    Content.make_commit()
    return content
