import dominate
from dominate.tags import *
from dominate.util import raw
from datetime import datetime, timedelta


def genHTML(data, urlRoot, date, entry=None):

    keys = sorted(data.keys())
    menus = sorted(data.values(), key=lambda x: x[0])

    if date.strftime('%Y-%m-%d') not in keys:
        for i in range(0, 5):
            date += timedelta(days=1)
            if date.strftime('%Y-%m-%d') in keys:
                break

    if entry == 'first':
        before, current, after = [], [menus[0]], menus[1:]
    elif entry == 'last':
        before, current, after = menus[:-1], [menus[-1]], []
    else:
        today = keys.index(date.strftime('%Y-%m-%d'))
        before, current, after = menus[:today], [menus[today]], menus[today + 1:]
    doc = dominate.document('Menu')

    menuLists = {'before': before, 'current': current, 'after': after}

    with doc.head:
        link(rel='stylesheet', href='{}static/style.css'.format(urlRoot), type='text/css')

    with doc:
        with body(onkeypress="keyPress(this, event);"):
            link(rel='stylesheet', href='{}static/style.css'.format(urlRoot), type='text/css')
            img(_class='arrow', id='left', onclick='change(false);', src='{}static/assets/left.svg'.format(urlRoot))
            img(_class='arrow', id='right', onclick='change(true);', src='{}static/assets/right.svg'.format(urlRoot))
            with div(id='main'):
                with div(_class='day before'):
                    h3('Go left to see previous weeks')
                iteration = 0
                for x in ['before', 'current', 'after']:
                    for i in menuLists[x]:
                        genDay(x, i, keys[iteration])
                        iteration += 1
                with div(_class='day after'):
                    h3('Go right to see future weeks')
            footer(raw(
                '<p>Arrows made by <a href="https://fontawesome.com">Font Awesome</a>. <a href="https://fontawesome.com/license/free">License</a>. No changes to images were made.' +
                '<br>Source code available at <a href="https://github.com/katzrkool/menu">Github</a>. <a href="https://github.com/katzrkool/menu/blob/master/LICENSE">Project License</a>'))
            script(type='text/javascript', src='{}static/main.js'.format(urlRoot))
    return doc.render()


def genDay(_class, data, date):
    day = div(_class='day {}'.format(_class))
    with day:
        h2(datetime.strptime(date, '%Y-%m-%d').strftime(
            '%A, %B %d, %Y'))
        with ul():
            for z in data:
                if z.startswith('\n'):
                    h3(z)
                else:
                    li(z)
    return day
