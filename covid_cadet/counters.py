def subdivision_get_employee_count_sum(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_count
    return count


def subdivision_get_employee_count_sum_adult(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_count_adult
    return count


def subdivision_get_covid_1_count_sum(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_covid_1_count
    return count


def subdivision_get_covid_1_count_sum_adult(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_covid_1_count_adult
    return count


def subdivision_get_covid_2_count_sum(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_covid_2_count
    return count


def subdivision_get_covid_2_count_sum_adult(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_covid_2_count_adult
    return count


def subdivision_get_willing_count_sum(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_willing_count
    return count


def subdivision_get_willing_count_sum_adult(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_willing_count_adult
    return count


def subdivision_get_covid_percent_sum(subdivisions_list):
    try:
        res = subdivision_get_covid_1_count_sum(subdivisions_list) / subdivision_get_employee_count_sum(subdivisions_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


def subdivision_get_covid_percent_sum_second(subdivisions_list):
    try:
        res = subdivision_get_covid_2_count_sum(subdivisions_list) / subdivision_get_employee_count_sum(subdivisions_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


def subdivision_get_covid_percent_sum_adult(subdivisions_list):
    try:
        res = subdivision_get_covid_1_count_sum_adult(subdivisions_list) / subdivision_get_employee_count_sum_adult(subdivisions_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


def subdivision_get_covid_percent_sum_adult_second(subdivisions_list):
    try:
        res = subdivision_get_covid_2_count_sum_adult(subdivisions_list) / subdivision_get_employee_count_sum_adult(subdivisions_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)



def get_employee_count_sum(employees_list):
    return employees_list.count()


def get_covid_1_count_sum(employees_list):
    return employees_list.filter(last_date1__isnull=False).count()


def get_covid_2_count_sum(employees_list):
    return employees_list.filter(last_date2__isnull=False).count()


def get_employee_covid_percent_sum_first(employees_list):
    try:
        res = get_covid_1_count_sum(employees_list) / get_employee_count_sum(
            employees_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


def get_employee_covid_percent_sum_second(employees_list):
    try:
        res = get_covid_2_count_sum(employees_list) / get_employee_count_sum(employees_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)



