from django.shortcuts import render
from parseltongue.parser_geneerator import JsonToGetText, Setting


def parser_post(request):
    return_text = {}
    if request.method == 'POST':
        html = request.POST['html']
        tags = request.POST['tags']
        tags_map = request.POST['map']
        table = request.POST['table']
        json = request.POST['json']
        if html is not '' and json is not '':
            get_html = JsonToGetText(html, json)
            return_text['tag'] = get_html.get_tag_text()
            return_text['table'] = get_html.get_table_text()
        elif html is not '':
            setting = Setting(html)
            if tags is not '':
                setting.set_tag(str(tags).split(','))
            if tags_map is not '':
                setting.set_tag_map(tags_map)
            if table is not '':
                setting.set_table(table)
            return_text['json'] = setting.to_json()
    return render(request, "post.html", return_text)