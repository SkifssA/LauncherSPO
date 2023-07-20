import requests
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
        r = self.session.get('https://ssuz.vip.edu35.ru/auth/login-page')
        print(r)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        self.cookie = f'csrftoken={r.cookies["csrftoken"]}'



    def head(self):
        '''Создание заголовка'''
        head_ = {  # Заголовок запроса
            'Host': 'ssuz.vip.edu35.ru',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer':'https://ssuz.vip.edu35.ru/auth/login-page',
            'Sec-Ch-Ua': '"Not.A/Brand";v = "8", "Chromium";v = "114", "Microsoft Edge";v = "114"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        if self.cookie.find('ssuz_sessionid') != -1:
            head_['X-Csrftoken'] = self.cookie[self.cookie.rfind('=')+1:]
        return head_

    def date_patch(self, date_f):
        """Выставление правильного времени"""
        date_from = date_f
        if date_f == '':
            mon = int(datetime.today().strftime('%m'))
            if 13 > mon > 8:
                date_from = '01.09.' + datetime.today().strftime('%Y')
            else:
                date_from = '01.01.' + datetime.today().strftime('%Y')
        return date_from

    def set_cookie(self, cookie):
        '''Установка куки(Для тестов, а то банит XD)'''
        self.session.get('https://ssuz.vip.edu35.ru', cookies={'Cookie': cookie})
        self.cookie = cookie

    def login(self, login, password):
        '''Авторизация'''

        data = self.session.post('https://ssuz.vip.edu35.ru/auth/login', headers=self.head(),
                                 data={'csrfmiddlewaretoken': self.csrf,
                                       'login_login': login,
                                       'login_password': password})
        try:
            cook = requests.utils.dict_from_cookiejar(self.session.cookies)
            self.set_cookie(f'ssuz_sessionid={cook["ssuz_sessionid"]}; csrftoken={cook["csrftoken"]}')
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
            'period_id': '30',
            'date_from': date_from,
            'date_to': date_to,
            'month': '',
            'filter': ''
        }
        response = self.session.post(self.url[0], headers=self.head(), data=data).json()
        return response

    def disc_rows(self, id_group, prac='', date_from=''):
        '''Получение предметов группы'''
        date_from = self.date_patch(date_from)
        data = {
            'slave_mode': '1',
            'empty_item': '1',
            'practical': prac,
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
        s = f"'name': '{name} ', 'id_group': '{id_group}', 'subject_id': '{subject_id}','student_id': '{student_id}'"
        return '\t{' + s + '},\n'

    def create_disc_list(self, que):
        '''Создание списков для работы'''
        prac = 'Practice = [\n'
        theo = 'Theory = [\n'
        for group in self.group_rows(prac='1', date_from='01.09.2022')['rows']:
            name = group['name'][:group['name'].index(' ')]
            for disc in self.disc_rows(group['id'], prac='1', date_from='01.09.2022')['rows']:
                student = self.student_rows(group['id'], disc['id'], prac='1', date_from='01.09.2022')
                que.put(name)
                if student['total'] <= 5:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
                elif '(' in disc['name']:
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
                else:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'],
                                           student['rows'][0]['student_id'])
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
        return len(self.id_lesson_row(id_group, subject_id, prac=prac))

    def setting_turnout(self, id_group, subject_id, student_id, lesson, x, date_from='', prac=''):
        '''Выставление явки в журнал'''
        date_from = self.date_patch(date_from)
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

    def create_score_pole(self, id_group, subject_id, lesson, date_from='', prac=''):
        '''Создание поля для оценок'''
        date_from = self.date_patch(date_from)
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

    def show_score_pole(self, id_group, subject_id, lesson, date_from='', prac=''):
        '''Получение id поля для оценок'''
        date_from = self.date_patch(date_from)
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

    def expose_score(self, id_group, subject_id, lesson, wokr_id, score, student_id, date_from='', prac=''):
        '''Выставление оценок'''
        date_from = self.date_patch(date_from)
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

    def open_file_themes(self, disc, prac):
        themes = []
        prac = 't' if prac == '' else 'p'
        for file in os.listdir(os.getcwd() + '/Themes'):
            if disc['id_group'] in file and disc['name'][disc['name'].find('_') + 1:disc['name'].find(' ')] in file \
                    and prac in file[:-4]:
                print(file)
                with open('Themes/' + file, 'r') as f:
                    f.readline()
                    for line in f:
                        themes += [line[:line.rfind(' ')]] * int(line[line.rfind(' ') + 1:-1])
        return themes

    def save_themes(self, disc, prac=''):
        k = len(self.id_lesson_row(disc['id_group'], disc['subject_id'], date_from='01.09.2022', date_whis='31.12.2022',
                                   prac=prac))
        for less, theme in zip(self.id_lesson_row(disc['id_group'], disc['subject_id'], prac=prac),
                               self.open_file_themes(disc, prac)[k:]):
            self.uploading_topics(disc['id_group'], disc['subject_id'], less, theme, prac=prac)

    def uploading_topics(self, id_group, subject_id, lesson, theme, date_from='', prac=''):
        """Ввод темы в журнал"""
        date_from = self.date_patch(date_from)
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
        return self.session.post(self.url[9], headers=self.head(), data=data).json()

    # ДОПИЛИ БЛЯТЬ
    def uploader_sub_group_names(self, id_group, subject_id, date_from=''):
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'unit_id': '22',
            'period_id': '30',
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
        return self.session.post(self.url[10], headers=self.head(), data=data).json()['sub_group_names']

    def аssign_rating(self, id_group, subject_id, type_score, mark='', subperiod='', date_from=''):
        sub_g = self.uploader_sub_group_names(id_group, subject_id)
        if len(sub_g) == 0:
            sub_g = [0, 0]
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        data = {
            'group_id': id_group,
            'period_id': '30',
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
        self.session.post(self.url[11], headers=self.head(), data=data)

    def score_final(self, id_group, subject_id, student_id, score, type_score, subperiod='', date_from=''):
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        if type_score == 'annual_estimation':
            d = '{"lessons":{},"final_marks":{"' + f'{str(student_id)}_{type_score}' + '":{"mark":"' + str(
                score) + '","type":"' + type_score + '","student_id":' + str(student_id) + '}},"subperiod_marks":{}}'
        else:
            d = '{"lessons":{},"final_marks":{},"subperiod_marks":{"' + f'{str(student_id)}_subperiod_{id_group}_{subperiod}' + '":{' + f'"mark":"{score}","subperiod_id":"{subperiod}","student_id":{str(student_id)}' + '}}}'
        data = {
            'data': d,
            'unit_id': 22,
            'period_id': 30,
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
                          headers=self.head(), data=data)

    def today_list(self):
        e = self.group_rows(date_from=datetime.today().strftime('%d.%m.%Y'))['rows']
        mass = [[], []]
        for i in e:
            for j, x in enumerate(ListOfDisciplines.Theory):
                if i['id'] == int(x['id_group']):
                    if self.id_lesson_row(x['id_group'], x['subject_id'], date_from='03.03.2023',
                                          date_whis='03.03.2023'):
                        mass[0].append(ListOfDisciplines.Theory[j])
            for j, x in enumerate(ListOfDisciplines.Practice):
                if i['id'] == int(x['id_group']):
                    if self.id_lesson_row(x['id_group'], x['subject_id'], date_from='03.03.2023',
                                          date_whis='03.03.2023',
                                          prac='1'):
                        mass[1].append(ListOfDisciplines.Practice[j])
        return mass

    def ved_get(self):
        data = {
            'start': '0',
            'm3_window_id': 'cmp_2b72f74a',
            'grid_id': 'cmp_850ea220',
            'ssuz.exam_score.actions.PeriodSelectPack_id': '30',
            'ssuz.exam_score.actions.SubperiodSelectPack_id': '400',
            'filter': 'Копылов',
            'id': '-1',
        }
        return self.session.post('https://ssuz.vip.edu35.ru/actions/exam_score/objectrowsaction',
                                 headers=self.head(), data=data).json()['rows']

    def ved_score(self, exam_id, id_st, score):
        data = {
            'exam_sheet_id': exam_id,
            'm3_window_id': 'cmp_2fb9c023',
            'grid_id': 'cmp_83d63e96',
            'xaction': 'update',
            'rows': '{' + f'"student_id":{id_st},"score_23":"{score}"' + '}'
        }
        return self.session.post('https://ssuz.vip.edu35.ru/actions/exam_score/exam_score_rows',
                                 headers=self.head(), data=data)

    def ved_score_type(self, exam_id):
        data = {
            'exam_sheet_id': exam_id,
            'm3_window_id': 'cmp_eb198448',
            'grid_id': 'cmp_850ea220',
            'score_type_ids': '[23]',
        }
        return self.session.post('https://ssuz.vip.edu35.ru/actions/exam_score/re_score_type_save_action',
                                 headers=self.head(), data=data)


def sd(score):
    i = int(score) if score % 1 < 0.75 else int(score) + 1
    return i


def wwwww(disc):
    print(disc['name'])
    nums = re.findall(r'\d+', disc['subject_id'])
    s.аssign_rating(disc['id_group'], disc['subject_id'], 'Годовая', mark=0)
    s.аssign_rating(disc['id_group'], disc['subject_id'], 'Итоговая', mark=1)
    s.аssign_rating(disc['id_group'], disc['subject_id'], '2 семестр(22/23)', subperiod=400)
    for stud in s.student_rows(disc['id_group'], disc['subject_id'])['rows']:
        w = sd(float(z)) if (z := stud['aver_period']) != '' else z
        q = sd(float(x)) if (x := stud[f"aver_subper_{nums[0]}_400"]) != '' else x
        s.score_final(disc['id_group'], disc['subject_id'], stud['student_id'], w, 'annual_estimation')
        s.score_final(disc['id_group'], disc['subject_id'], stud['student_id'], q, '', 400)


def wwwww2(disc):
    print(disc['name'], '')
    e, x = 0, 0
    for stud in s.student_rows(disc['id_group'], disc['subject_id'])['rows']:
        w = sd(float(z)) if (z := stud['aver_period']) != '' else z
        if w == 2 or w == '':
            x += 1
        elif w > 3:
            e += 1
    print('5 и 4 в %', (e * 100) / s.student_rows(disc['id_group'], disc['subject_id'])['total'])
    print('2 и неотистованых', x)


def wwwww3(disc):
    print(disc['name'])
    for i in s.id_lesson_row(disc['id_group'], disc['subject_id'], date_from='01.09.2022'):
        if s.uploading_topics(disc['id_group'], disc['subject_id'], i, '', date_from='01.09.2022')[
            'message'] != 'Занятие закрыто!':
            print('ОТКРЫТО БЛЯЯЯЯТЬ')
    return len(s.id_lesson_row(disc['id_group'], disc['subject_id'], date_from='01.09.2022'))


if __name__ == '__main__':
    s = AvtoJ()
    s.set_cookie('ssuz_sessionid=ztoi20yh3xv911evywzzvsvihm1cvgmu')
    for exam in s.ved_get():
        s.ved_score_type(exam['id'])
        for disc in ListOfDisciplines.Theory:
            if disc['name'].find(exam['group_actual_name'][:exam['group_actual_name'].find(' ')]) != -1:
                print(disc['name'])
                for stud in s.student_rows(disc['id_group'], disc['subject_id'])['rows']:
                    s.ved_score(exam['id'], stud['student_id'], stud['final_grade'])
                break
