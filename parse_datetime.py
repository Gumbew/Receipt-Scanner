from recognizers_date_time import recognize_datetime, Culture


def parse_datetime(datetime_string):
    results = recognize_datetime(datetime_string, Culture.English)
    if len(results) == 0:
        return None

    value = results[0].resolution['values'][0]
    if value['type'] == 'daterange':
        return None
    else:
        return value['timex']
