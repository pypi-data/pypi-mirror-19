import os
import sys
import json
from datetime import datetime
import codecs


template = '[日報] {today:%Y-%m-%d}({weekday}) ver.{version}: {message}'


def version(today):
    path = os.path.expanduser('~/.nippoh')
    with open(path, 'r') as fp:
        if not os.path.exists(path):
            db = {}
        else:
            db = json.loads(fp.read() or '{}')

        key = today.strftime('%Y-%m-%d')
        count = db.setdefault(key, 0)
        count += 1
        db[key] = count
    with open(path, 'w') as fp:
        fp.write(json.dumps(db))
    return count


def main():
    message = input('?> ')
    today = datetime.today()
    params = {
        'today': today,
        'message': message,
        'weekday': '月火水木金土日'[today.weekday()],
        'version': version(today),
    }
    text = template.format(**params)
    codecs.getwriter('utf-8')(sys.stdout).write(text)


if __name__ == '__main__':
    main()
