import requests
import re
from datetime import datetime
import ListOfDisciplines
from importlib import reload


class AvtoJ:
    def __init__(self):
        self.session = requests.session()
        self.url = [
            # Получение основного id и name группы
            'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_group_rows',
            # Получение id предмета и подгруппы
            'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_subject_rows',
            # Получение студентов группы
            'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_rows',
        ]
        self.load = ''
        self.cookie = ''

    '''Создание заголовка'''

    def head(self):
        head_ = {  # Заголовок запроса
            'Host': 'ssuz.vip.edu35.ru',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie
        }
        return head_

    '''Установка куки(Для тестов, а то банит XD)'''

    def set_cookie(self, cookie):
        self.session.get('https://ssuz.vip.edu35.ru', cookies={'Cookie': cookie})
        self.cookie = cookie

    '''Авторизация'''

    def login(self, login, password):
        data = self.session.post('https://ssuz.vip.edu35.ru/auth/login', headers=self.head(),
                                 data={'login_login': login,
                                       'login_password': password})
        try:
            cook = requests.utils.dict_from_cookiejar(self.session.cookies)
            self.set_cookie('ssuz_sessionid=' + cook['ssuz_sessionid'])
            return True
        except KeyError:
            return False

    '''Получение групп'''

    def group_rows(self, date_from='01.01.2023'):
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': '',
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'month': '',
            'filter': ''
        }
        response = self.session.post(self.url[0], headers=self.head(), data=data).json()
        return response

    '''Получение предметов группы'''

    def disc_rows(self, id_group, date_from='01.01.2023'):
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': '',
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'month': '',
            'filter': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': '',
        }
        response = self.session.post(self.url[1], headers=self.head(), data=data).json()
        return response

    '''Получение студентов группы'''

    def student_rows(self, id_group, subject_id, date_from='01.01.2023'):
        nums = re.findall(r'\d+', subject_id)
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': '',
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'month': '',
            'filter': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
        }
        response = self.session.post(self.url[2], headers=self.head(), data=data).json()
        return response

    '''Создание списка практических и теоретических журналов'''

    def creat_str(self, name, id_group, subject_id, student_id):
        s = f'"name": "{name}", "id_group": "{id_group}", "subject_id": '+f"'{subject_id}'"+f', "student_id": "{student_id}"'
        return '\t{' + s + '},\n'

    '''Создание списков для работы'''

    def create_disc_list(self):
        prac = 'Practice = [\n'
        theo = 'Theory = [\n'
        for group in self.group_rows()['rows']:
            name = group['name'][:group['name'].index(' ')]
            self.load = name
            for disc in self.disc_rows(group['id'])['rows']:
                student = self.student_rows(group['id'], disc['id'])
                if student['total'] <= 5:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
                elif student['total'] <= 15:
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
                else:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
        return [prac + ']\n', theo + ']']

    '''Запись в файл'''

    def save_file_disc(self):
        if not ListOfDisciplines.Theory and not ListOfDisciplines.Practice:
            with open('ListOfDisciplines.py', 'wb') as f:
                list_disc = self.create_disc_list()
                f.write(list_disc[0].encode('utf-8'))
                f.write(list_disc[1].encode('utf-8'))
            reload(ListOfDisciplines)