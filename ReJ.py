import random

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import re
from datetime import datetime

try:
    import ListOfDisciplines
except ModuleNotFoundError:
    pass
from importlib import reload
import os
from bs4 import BeautifulSoup


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
            'https://ssuz.vip.edu35.ru/actions/register/lesson_register/lesson_register_save',
            # Получение название подгрупп
            'https://ssuz.vip.edu35.ru/actions/ssuz.register.actions.Pack/finalmarktypewindowaction',
            # Задать вид оценки
            'https://ssuz.vip.edu35.ru/actions/ssuz.register.actions.Pack/finalmarktypesaveaction',
        ]
        self.cookie = ''
        self.load = ''

        mon = int(datetime.today().strftime('%m'))
        if 13 > mon > 8:
            self.period_id = int(datetime.today().strftime('%y')) + 8 + (int(datetime.today().strftime('%y')) - 23)
        else:
            self.period_id = int(datetime.today().strftime('%y')) + 8 + (int(datetime.today().strftime('%y')) - 23) + 1
        print('rej 58',self.period_id)
        r = self.session.get('https://ssuz.vip.edu35.ru/auth/login-page', verify=False)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        self.cookie = f'csrftoken={r.cookies["csrftoken"]}'

    def head(self):
        '''Создание заголовка'''
        head_ = {  # Заголовок запроса
            'Host': 'ssuz.vip.edu35.ru',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://ssuz.vip.edu35.ru/auth/login-page',
            'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'Cache-Control':'max-age=0',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'cross-site',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Xsrftoken': self.cookie[self.cookie.find('csrftoken=') + len('csrftoken='):]
        }
        return head_

    def date_patch(self, date_f=''):
        """Выставление правильного времени"""
        date_from = date_f
        if date_f == '':
            mon = int(datetime.today().strftime('%m'))
            # date_from = '01.09.2023'# + datetime.today().strftime('%Y')
            if 13 > mon > 8:
                date_from = '01.09.' + datetime.today().strftime('%Y')
            else:
                date_from = '01.01.' + datetime.today().strftime('%Y')
        return date_from

    def set_cookie(self, cookie):
        '''Установка куки(Для тестов, а то банит XD)'''
        self.session.get('https://ssuz.vip.edu35.ru', cookies={'Cookie': cookie},verify=False)
        self.cookie = cookie

    def login(self, login, password):
        '''Авторизация'''

        # data = self.session.post('https://ssuz.vip.edu35.ru/auth/login', headers=self.head(),verify=False,
        #         data={'csrfmiddlewaretoken': self.csrf,'login_login': login,'login_password': password})
        # print(data.json())

        try:
            cook = requests.utils.dict_from_cookiejar(self.session.cookies)
            print("11111111111111111111111111111",cook)
            # self.set_cookie(f'csrf_token_header_name=X-XSRFTOKEN;ssuz_sessionid={cook["ssuz_sessionid"]};csrftoken={cook["csrftoken"]}')
            self.set_cookie(f'csrf_token_header_name=X-XSRFTOKEN;ssuz_sessionid={password};csrftoken={login}')
            return True
        except KeyError:
            return False

    def group_rows(self, prac='', date_from='', date_to=datetime.today().strftime('%d.%m.%Y')):
        '''Получение групп'''
        date_from = self.date_patch(date_from)
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
            'date_from': date_from,
            'date_to': date_to,
            'month': '',
            'filter': ''
        }
        # print('rej 139',self.session.post(self.url[0], headers=self.head(), data=data))
        response = self.session.post(self.url[0], headers=self.head(),verify=False, data=data).json()
        # print(141,response)
        return response

    def disc_rows(self, id_group, prac='', date_from=''):
        '''Получение предметов группы'''
        date_from = self.date_patch(date_from)
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
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
        response = self.session.post(self.url[1], headers=self.head(), data=data,verify=False).json()
        return response

    def student_rows(self, id_group, subject_id, date_from='',
                     date_whis=datetime.today().strftime('%d.%m.%Y'), prac=''):
        '''Получение студентов группы'''
        date_from = self.date_patch(date_from)

        nums = re.findall(r'\d+', subject_id)
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
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
        s = self.session.post(self.url[2], headers=self.head(), data=data,verify=False)
        response = s.json()
        # print('rej 189',response)
        return response

    def creat_str(self, name, id_group, subject_id, student_id, id_list):
        '''Создание списка практических и теоретических журналов'''
        s = f"'name': '{name} ', 'id_group': '{id_group}', 'subject_id': '{subject_id}','student_id': '{student_id}', 'id':{id_list}"
        return '\t{' + s + '},\n'

    def create_disc_list(self, que):
        '''Создание списков для работы'''
        prac = 'Practice = [\n'
        theo = 'Theory = [\n'
        p_id = 0
        t_id = 0
        for group in self.group_rows(prac='', date_from=self.date_patch())['rows']:
            name = group['name'][:group['name'].index(' ')]
            for disc in self.disc_rows(group['id'], prac='', date_from=self.date_patch())['rows']:
                student = self.student_rows(group['id'], disc['id'], prac='', date_from=self.date_patch())
                que.put(name)
                if student['total'] <= 5:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'], t_id)
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'], p_id)
                    p_id += 1
                    t_id += 1
                elif '(' in disc['name']:
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'], p_id)
                    p_id += 1
                else:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'], t_id)
                    t_id += 1
        return [prac + ']\n', theo + ']']

    def save_file_disc(self, que):
        '''Запись в файл'''
        with open('ListOfDisciplines.py', 'wb') as f:
            list_disc = self.create_disc_list(que)
            f.write(list_disc[0].encode('utf-8'))
            f.write(list_disc[1].encode('utf-8'))
        reload(ListOfDisciplines)

    def id_lesson_row(self, id_group, subject_id, date_from='',
                      date_whis=datetime.today().strftime('%d.%m.%Y'), prac=''):
        '''Вывод всех занятий в журнале'''
        date_from = self.date_patch(date_from)
        try:
            return tuple(x['id'] for x in self.student_rows(id_group, subject_id,
                                                            date_from, date_whis, prac=prac)['rows'][0]['lessons'])
        except IndexError:
            return []

    def close_open_lesson(self, id_group, subject_id, student_id, date_from='', prac='', open=False):
        '''Закрытие/открытие занятий'''
        date_from = self.date_patch(date_from)
        print('rej 247',date_from)
        url = 4 if open else 3
        nums = re.findall(r'\d+', subject_id)
        for lesson in self.id_lesson_row(id_group, subject_id, prac=prac):
            data = {
                'lesson_id': lesson,
                'student_id': student_id,
                'practical': prac,
                'unit_id': '22',
                'period_id': self.period_id,
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
            s = self.session.post(self.url[url], headers=self.head(), data=data,verify=False)
            print(269,data)
            print(270,s.json())
        return len(self.id_lesson_row(id_group, subject_id, prac=prac))

    def setting_turnout(self, id_group, subject_id, student_id, lesson, x, date_from='', prac=''):
        '''Выставление явки в журнал'''
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'data': '{' + f'"lesson_id":{lesson},"attendance":"{x}","student_id":{student_id}' + '}',
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
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
        }
        return self.session.post(self.url[5], headers=self.head(), data=data,verify=False)

    def create_score_pole(self, id_group, subject_id, lesson, date_from='', prac=''):
        '''Создание поля для оценок'''
        date_from = self.date_patch(date_from)
        print(date_from,'date_from 1')
        nums = re.findall(r'\d+', subject_id)
        data = {
            'lesson_id': lesson,
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
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
        self.session.post(self.url[6], headers=self.head(), data=data,verify=False)

    def show_score_pole(self, id_group, subject_id, lesson, date_from='', prac=''):
        '''Получение id поля для оценок'''
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'lesson_id': lesson,
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
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
        return self.session.post(self.url[7], headers=self.head(), data=data,verify=False).json()

    def expose_score(self, id_group, subject_id, lesson, wokr_id, score, student_id, date_from='', prac=''):
        '''Выставление оценок'''
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'data': '{' + f'"lesson_id": {lesson}, "attendance": "", "work_id": "{wokr_id}", "score_type_id": "36", "score": "{score}", "student_id": {student_id}' + '}',
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
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
        self.session.post(self.url[8], headers=self.head(), data=data,verify=False)

    def open_file_themes(self, disc, prac):
        themes = []
        prac = 't' if prac == '' else 'p'
        for file in os.listdir(os.getcwd() + '/Themes'):
            if disc['id_group'] in file and disc['name'][disc['name'].find('_') + 1:disc['name'].find(' ')] in file \
                    and prac in file[:-4]:
                print('rej 377',file)
                with open('Themes/' + file, 'r') as f:
                    f.readline()
                    for line in f:
                        themes += [line[:line.rfind(' ')]] * int(line[line.rfind(' ') + 1:-1])
        return themes

    def save_themes(self, disc, prac=''):
        
        k = len(self.id_lesson_row(disc['id_group'], disc['subject_id'], date_from='01.09.2023', date_whis=datetime.today().strftime('%d.%m.%Y'),prac=prac))
        # sss = zip(self.id_lesson_row(disc['id_group'], disc['subject_id'], prac=prac),self.open_file_themes(disc, prac)[k:])
        sss = zip(self.id_lesson_row(disc['id_group'], disc['subject_id'], prac=prac),self.open_file_themes(disc, prac))
        for less, theme in sss:
            s = self.uploading_topics(disc['id_group'], disc['subject_id'], less, theme, prac=prac)
            print('rej 391',less, theme)
            print(s,'rej 392')

    def uploading_topics(self, id_group, subject_id, lesson, theme, date_from='', prac=''):
        """Ввод темы в журнал"""
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'lesson_subject': theme,
            'lesson_id': lesson,
            'practical': prac,
            'unit_id': '22',
            'period_id': self.period_id,
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
        return self.session.post(self.url[9], headers=self.head(), data=data,verify=False).json()

    # ДОПИЛИ БЛЯТЬ
    def uploader_sub_group_names(self, id_group, subject_id, date_from=''):
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'unit_id': '22',
            'period_id': self.period_id,
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'practical': '',
            'slave_mode': '1',
            'month': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
            'subperiod': '',
            'mark': '0',
        }
        return self.session.post(self.url[10], headers=self.head(), data=data,verify=False).json()['sub_group_names']

    def аssign_rating(self, id_group, subject_id, type_score, mark='', subperiod='', date_from=''):
        sub_g = self.uploader_sub_group_names(id_group, subject_id)
        if len(sub_g) == 0:
            sub_g = [0, 0]
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'group_id': id_group,
            'period_id': self.period_id,
            'subject_sub_group_obj': subject_id,
            'mark': mark,
            'subperiod': subperiod,
            'unit_id': '22',
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'practical': '',
            'slave_mode': '1',
            'month': '',
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_id': nums[0],
            'sub_group_names': sub_g[0],
            'sub_group_names': sub_g[1],
            'mark_name': type_score,
            'mark_type_id': '23',
        }
        print('rej 468',self.session.post(self.url[11], headers=self.head(), data=data,verify=False))

    def score_final(self, id_group, subject_id, student_id, score, type_score='', subperiod='', date_from=''):
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        if type_score == 'annual_estimation':
            d = '{"lessons":{},"final_marks":{"' + f'{str(student_id)}_{type_score}' + '":{"mark":"' + \
                f'{str(score)}","type":"{type_score}","student_id":{str(student_id)}' + '}},"subperiod_marks":{}}'
        else:
            d = '{"lessons":{},"final_marks":{},"subperiod_marks":{"' + f'{str(student_id)}_subperiod_{id_group}_{subperiod}' + \
                '":{' + f'"mark":"{score}","subperiod_id":"{subperiod}","student_id":{str(student_id)}' + '}}}'
        data = {
            'data': d,
            'unit_id': 22,
            'period_id': self.period_id,
            'date_from': date_from,
            'date_to': datetime.today().strftime('%d.%m.%Y'),
            'practical': '',
            'slave_mode': '1',
            'month': '',
            'group_id': id_group,
            'subject': '0',
            'subject_gen_pr_id': '0',
            'exam_subject_id': '0',
            'subject_sub_group_obj': subject_id,
            'subject_id': nums[0],
        }
        self.session.post('https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_save_rows',
                          headers=self.head(), verify=False,data=data)

    def today_list(self):
        e = self.group_rows(date_from=datetime.today().strftime('%d.%m.%Y'))['rows']
        mass = [[], []]
        for i in e:
            for j, x in enumerate(ListOfDisciplines.Theory):
                if i['id'] == int(x['id_group']):
                    if self.id_lesson_row(x['id_group'], x['subject_id'],
                                          date_from=datetime.today().strftime('%d.%m.%Y'),
                                          date_whis=datetime.today().strftime('%d.%m.%Y')):
                        mass[0].append(ListOfDisciplines.Theory[j])
            for j, x in enumerate(ListOfDisciplines.Practice):
                if i['id'] == int(x['id_group']):
                    if self.id_lesson_row(x['id_group'], x['subject_id'],
                                          date_from=datetime.today().strftime('%d.%m.%Y'),
                                          date_whis=datetime.today().strftime('%d.%m.%Y'),
                                          prac='1'):
                        mass[1].append(ListOfDisciplines.Practice[j])
        return mass

    def ved_get(self, per, subper, family):
        data = {
            'start': '0',
            'm3_window_id': 'cmp_2b72f74a',
            'grid_id': 'cmp_850ea220',
            'ssuz.exam_score.actions.PeriodSelectPack_id': per,
            'ssuz.exam_score.actions.SubperiodSelectPack_id': subper,
            'filter': family,
            'id': '-1',
        }
        return self.session.post('https://ssuz.vip.edu35.ru/actions/exam_score/objectrowsaction',
                                 headers=self.head(),verify=False, data=data).json()['rows']

    def ved_score(self, exam_id, id_st, score):
        data = {
            'exam_sheet_id': exam_id,
            'm3_window_id': 'cmp_2fb9c023',
            'grid_id': 'cmp_83d63e96',
            'xaction': 'update',
            'rows': '{' + f'"student_id":{id_st},"score_23":"{score}"' + '}'
        }
        return self.session.post('https://ssuz.vip.edu35.ru/actions/exam_score/exam_score_rows',
                                 headers=self.head(),verify=False, data=data)

    def ved_score_type(self, exam_id):
        data = {
            'exam_sheet_id': exam_id,
            'm3_window_id': 'cmp_eb198448',
            'grid_id': 'cmp_850ea220',
            'score_type_ids': '[23]',
        }
        return self.session.post('https://ssuz.vip.edu35.ru/actions/exam_score/re_score_type_save_action',
                                 headers=self.head(),verify=False, data=data)


def sd(score):
    i = int(score) if score % 1 < 0.75 else int(score) + 1
    return i


def wwwww(disc):
    print('rej 558',disc['name'])
    nums = re.findall(r'\d+', disc['subject_id'])
    s.аssign_rating(disc['id_group'], disc['subject_id'], 'Годовая', mark=0)
    s.аssign_rating(disc['id_group'], disc['subject_id'], 'Итоговая', mark=1)
    s.аssign_rating(disc['id_group'], disc['subject_id'], '2 семестр(22/23)', subperiod=400)
    for stud in s.student_rows(disc['id_group'], disc['subject_id'])['rows']:
        w = sd(float(z)) if (z := stud['aver_period']) != '' else z
        q = sd(float(x)) if (x := stud[f"aver_subper_{nums[0]}_400"]) != '' else x
        s.score_final(disc['id_group'], disc['subject_id'], stud['student_id'], w, 'annual_estimation')
        s.score_final(disc['id_group'], disc['subject_id'], stud['student_id'], q, 400)


def wwwww2(disc):
    print('rej 571',disc['name'])
    e, x = 0, 0
    for stud in s.student_rows(disc['id_group'], disc['subject_id'])['rows']:
        w = sd(float(z)) if (z := stud['aver_period']) != '' else z
        if w == 2 or w == '':
            x += 1
        elif w > 3:
            e += 1
    print('5 и 4 в %', (e * 100) / s.student_rows(disc['id_group'], disc['subject_id'])['total'])
    print('2 и не отестованных', x)


def wwwww3(disc):
    print('rej 584',disc['name'])
    for i in s.id_lesson_row(disc['id_group'], disc['subject_id'], date_from='01.09.2022'):
        if s.uploading_topics(disc['id_group'], disc['subject_id'], i, '', date_from='01.09.2022')[
            'message'] != 'Занятие закрыто!':
            print('ОТКРЫТО БЛЯЯЯЯТЬ')
    return len(s.id_lesson_row(disc['id_group'], disc['subject_id'], date_from='01.09.2022'))


def random_list(n, list_d):
    s = []
    while not len(set(s)) == n:
        s.append(random.randint(0, len(list_d) - 1))
    st = []
    for i in set(s):
        st.append(list_d[i])
    return st


def wwwww4(disc, n):
    print('rej 603',disc['name'])
    date_lesson = set(
        [x['date'] for x in s.student_rows(disc['id_group'], disc['subject_id'])[
            'rows'][0]['lessons']])
    id_student = s.student_rows(disc['id_group'], disc['subject_id'])['rows']
    for d in date_lesson:
        print('rej 609',d)
        print('rej 610',datetime.strftime(datetime.strptime(d, '%d.%m.%Y'), '%a'))
        if not datetime.strftime(datetime.strptime(d, '%d.%m.%Y'), '%a') == 'Sat':
            st = random_list(n, id_student)
            for i in s.id_lesson_row(disc['id_group'], disc['subject_id'], date_from=d, date_whis=d):
                for j in st:
                    print('rej 615',s.setting_turnout(disc['id_group'], disc['subject_id'], j['student_id'], i, 'Н'))
                    pass

def kol_vo_ch(disc, prac=''):
    return len(s.id_lesson_row(disc['id_group'], disc['subject_id'], prac=prac))


def kol_vo():
    w = 0
    for i in (0, 2, 4, 6, 8, 10):
        w += kol_vo_ch(ListOfDisciplines.Theory[i])
        print(f'{ListOfDisciplines.Theory[i]["name"]} {kol_vo_ch(ListOfDisciplines.Theory[i])} ')
        print('rej 627')
    for i in (0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16):
        w += kol_vo_ch(ListOfDisciplines.Practice[i], prac='1')
        print(f'{ListOfDisciplines.Practice[i]["name"]} {kol_vo_ch(ListOfDisciplines.Practice[i], prac="1")}')
    print(w)



if __name__ == '__main__':
    s = AvtoJ()
    print(s.login('1051110511_t0087', '0knvK1a6'))
    kol_vo()


