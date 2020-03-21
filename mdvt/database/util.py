from mdvt import db


def db_insert_if_not_exist(entry, **kwargs):
    existing_entry = entry.query
    for key, value in kwargs.items():
        existing_entry.filter(key == value)
    existing_entry = existing_entry.first()

    if existing_entry is None:
        db.session.add(entry)
        db.session.commit()
        return entry
    else:
        return existing_entry
