import requests
import re
from datetime import datetime
import ListOfDisciplines
from importlib import reload
import os

"""
Придумать разгроничение по семестрам!!!!!
Соеденить выставление тем с основным приложением
"""


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
            # Закрытие занятия
            'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_close_lesson_action',
            # Открыть занятие
            'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_open_lesson_action',
            # Выставить явку
            'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/save_lesson_score',
            # Создание поля для оценок
            'https://ssuz.vip.edu35.ru/actions/lesson_work/objectsaveaction',
            # Получение id оценок
            'https://ssuz.vip.edu35.ru/actions/lesson_work/objectrowsaction',
            # Выставление оценок
            'https://ssuz.vip.edu35.ru/actions/register/lessons_tab/save_lesson_score',
            # Запись темы урока
            'https://ssuz.vip.edu35.ru/actions/register/lesson_register/lesson_register_save'
        ]
        self.load = ''
        self.cookie = ''

    def head(self):
        '''Создание заголовка'''
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

    def set_cookie(self, cookie):
        '''Установка куки(Для тестов, а то банит XD)'''
        self.session.get('https://ssuz.vip.edu35.ru', cookies={'Cookie': cookie})
        self.cookie = cookie

    def login(self, login, password):
        '''Авторизация'''
        data = self.session.post('https://ssuz.vip.edu35.ru/auth/login', headers=self.head(),
                                 data={'login_login': login,
                                       'login_password': password})
        try:
            cook = requests.utils.dict_from_cookiejar(self.session.cookies)
            self.set_cookie('ssuz_sessionid=' + cook['ssuz_sessionid'])
            return True
        except KeyError:
            return False

    def group_rows(self, date_from='01.01.2023'):
        '''Получение групп'''
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

    def disc_rows(self, id_group, date_from='01.01.2023'):
        '''Получение предметов группы'''
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

    def student_rows(self, id_group, subject_id, date_from='01.01.2023',
                     date_whis=datetime.today().strftime('%d.%m.%Y'), prac=''):
        '''Получение студентов группы'''
        nums = re.findall(r'\d+', subject_id)
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': prac,
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': date_whis,
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

    def creat_str(self, name, id_group, subject_id, student_id):
        '''Создание списка практических и теоретических журналов'''
        s = f'"name": "{name}", "id_group": "{id_group}", "subject_id": ' + f"'{subject_id}'" + f', "student_id": "{student_id}"'
        return '\t{' + s + '},\n'

    def create_disc_list(self):
        '''Создание списков для работы'''
        prac = 'Practice = [\n'
        theo = 'Theory = [\n'
        for group in self.group_rows()['rows']:
            name = group['name'][:group['name'].index(' ')]
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

    def save_file_disc(self):
        '''Запись в файл'''
        with open('ListOfDisciplines.py', 'wb') as f:
            list_disc = self.create_disc_list()
            f.write(list_disc[0].encode('utf-8'))
            f.write(list_disc[1].encode('utf-8'))
        reload(ListOfDisciplines)

    def id_lesson_row(self, id_group, subject_id, date_from='01.01.2023',
                      date_whis=datetime.today().strftime('%d.%m.%Y'), prac=''):
        '''Вывод всех занятий в журнале'''
        return tuple(x['id'] for x in self.student_rows(id_group, subject_id,
                                                        date_from, date_whis, prac=prac)['rows'][0]['lessons'])

    def close_open_lesson(self, id_group, subject_id, student_id, date_from='01.01.2023', prac='', open=False):
        '''Закрытие/открытие занятий'''
        url = 4 if open else 3
        nums = re.findall(r'\d+', subject_id)
        for lesson in self.id_lesson_row(id_group, subject_id, prac=prac):
            data = {
                'lesson_id': lesson,
                'student_id': student_id,
                'practical': prac,
                'unit_id': '22',
                'period_id': '30',
                'date_from': date_from,
                'date_to': datetime.today().strftime('%d.%m.%Y'),
                'slave_mode': '1',
                'month': '',
                'group_id': id_group,
                'subject': '0',
                'subject_gen_pr_id': '0',
                'exam_subject_id': '0',
                'subject_sub_group_obj': subject_id,
                'subject_id': nums[0],
                'view_lessons': 'false',
            }
            self.session.post(self.url[url], headers=self.head(), data=data)

    def setting_turnout(self, id_group, subject_id, student_id, lesson, x, date_from='01.01.2023', prac=''):
        '''Выставление явки в журнал'''
        nums = re.findall(r'\d+', subject_id)
        data = {
            'data': '{' + f'"lesson_id":{lesson},"attendance":"{x}","student_id":{student_id}' + '}',
            'practical': prac,
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'slave_mode': '1',
            'month': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
            'view_lessons': 'false',
        }
        self.session.post(self.url[5], headers=self.head(), data=data)

    def create_score_pole(self, id_group, subject_id, lesson, date_from='01.01.2023', prac=''):
        '''Создание поля для оценок'''
        nums = re.findall(r'\d+', subject_id)
        data = {
            'lesson_id': lesson,
            'practical': prac,
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'slave_mode': '1',
            'month': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
            'view_lessons': 'false',
            'type_id': '82',
            'description': '',
            'lesson_work_id': '0',
        }
        self.session.post(self.url[6], headers=self.head(), data=data)

    def show_score_pole(self, id_group, subject_id, lesson, date_from='01.01.2023', prac=''):
        '''Получение id поля для оценок'''
        nums = re.findall(r'\d+', subject_id)
        data = {
            'lesson_id': lesson,
            'practical': prac,
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'slave_mode': '1',
            'month': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
            'view_lessons': 'false',
            'type_id': '82',
            'description': '',
            'lesson_work_id': '0',
        }
        return self.session.post(self.url[7], headers=self.head(), data=data).json()

    def expose_score(self, id_group, subject_id, lesson, wokr_id, score, student_id, date_from='01.01.2023', prac=''):
        '''Выставление оценок'''
        nums = re.findall(r'\d+', subject_id)
        data = {
            'data': '{' + f'"lesson_id": {lesson}, "attendance": "", "work_id": "{wokr_id}", "score_type_id": "36", "score": "{score}", "student_id": {student_id}' + '}',
            'practical': prac,
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'slave_mode': '1',
            'month': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
            'view_lessons': 'false',
        }
        self.session.post(self.url[8], headers=self.head(), data=data)

    """
    Задачи:
    2. Понимание сколько было часов в 1 семестре(Считывание часов у группы с 1.09 - 31.12) +-
    """

    def open_file_themes(self, disc):
        themes = []
        for file in os.listdir(os.getcwd() + '/Themes'):
            if disc['id_group'] in file and disc['name'][disc['name'].find('_') + 1:disc['name'].find(' ')] in file:
                with open('Themes/' + file, 'r') as f:
                    for line in f:
                        themes += [line[:line.rfind(' ')]] * int(line[line.rfind(' ') + 1:-1])
        return themes

    def save_themes(self, disc, prac=''):
        k = len(self.id_lesson_row(disc['id_group'], disc['subject_id'], date_from='01.09.2022', date_whis='31.12.2022',
                                   prac=prac))
        for less, theme in zip(self.id_lesson_row(disc['id_group'], disc['subject_id'], prac=prac),
                               self.open_file_themes(disc)[k:]):
            self.uploading_topics(disc['id_group'], disc['subject_id'], less, theme, prac=prac)

    def uploading_topics(self, id_group, subject_id, lesson, theme, date_from='01.01.2023', prac=''):
        """Ввод темы в журнал"""
        nums = re.findall(r'\d+', subject_id)
        data = {
            'lesson_subject': theme,
            'lesson_id': lesson,
            'practical': prac,
            'unit_id': '22',
            'period_id': '30',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'slave_mode': '1',
            'month': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
            'view_lessons': 'false',
        }
        self.session.post(self.url[9], headers=self.head(), data=data)
