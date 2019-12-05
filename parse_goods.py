import re


def load_items(input_text):
    cheque = repr(input_text[::-1])
    print(input_text)
    p = re.compile(r".\s(\d{2}[\.,]\d{1,}).*?(\\n|\))(.*?)\\n")
    list_of_dicts = []
    res = p.findall(cheque)
    print(res)
    for tup in res:
        ll = list(tup)
        for i in ll:
            if i == "":
                ll.remove(i)
        tup = tuple(ll)
        if tup[1] == r"\\n":
            item_name = tup[2]
        else:
            item_name = tup[1] + tup[2]
        list_of_dicts.append(
            {
                "price": tup[0][::-1],
                "item_name": item_name[::-1]
            }
        )

    return list_of_dicts
