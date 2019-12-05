import re


def load_items(input_text):
    cheque = input_text[::-1]

    p = re.compile(r".\s(\d{2}[\.,]\d{1,})\s[^)]?(\d{2})?\s?(.{2}n\\)?(.+?)n")
    list_of_dicts = []
    res = p.findall(cheque)

    for tup in res:
        ll = list(tup)
        for i in ll:
            if i == "":
                ll.remove(i)
        tup = tuple(ll)
        list_of_dicts.append(
            {
                "price": tup[0][::-1],
                "item_name": tup[-1][::-1]
            }
        )

    return list_of_dicts
