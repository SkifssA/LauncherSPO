import requests
import re
from datetime import datetime
try:
    import ListOfDisciplines
except ModuleNotFoundError:
    pass
from importlib import reload
import os




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
                                 data={'login_login': login,
                                       'login_password': password})
        try:
            cook = requests.utils.dict_from_cookiejar(self.session.cookies)
            self.set_cookie('ssuz_sessionid=' + cook['ssuz_sessionid'])
            return True
        except KeyError:
            return False

    def group_rows(self, date_from=''):
        '''Получение групп'''
        date_from = self.date_patch(date_from)
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

    def disc_rows(self, id_group, date_from=''):
        '''Получение предметов группы'''
        date_from = self.date_patch(date_from)
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
        s = f'"name": "{name} ", "id_group": "{id_group}", "subject_id":'+f"'{subject_id}'" + f',"student_id": {student_id}'
        return '\t{' + s + '},\n'

    def create_disc_list(self, que):
        '''Создание списков для работы'''
        prac = 'Practice = [\n'
        theo = 'Theory = [\n'
        for group in self.group_rows()['rows']:
            name = group['name'][:group['name'].index(' ')]
            for disc in self.disc_rows(group['id'])['rows']:
                student = self.student_rows(group['id'], disc['id'])
                que.put(name)
                if student['total'] <= 5:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'], student['rows'][0]['student_id'])
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'], student['rows'][0]['student_id'])
                elif student['total'] <= 15:
                    prac += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'], student['rows'][0]['student_id'])
                else:
                    theo += self.creat_str(name + '_' + disc['name'], group['id'], disc['id'], student['rows'][0]['student_id'])
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

    """
    Задачи:
    2. Понимание сколько было часов в 1 семестре(Считывание часов у группы с 1.09 - 31.12) +-
    """

    def open_file_themes(self, disc, prac):
        themes = []
        prac = 't' if prac == '' else 'p'
        for file in os.listdir(os.getcwd() + '/Themes'):
            if disc['id_group'] in file and disc['name'][disc['name'].find('_') + 1:disc['name'].find(' ')] in file\
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
        return self.session.post(self.url[9], headers=self.head(), data=data)


    #ДОПИЛИ БЛЯТЬ
    def uploader_sub_group_names(self, id_group, subject_id, date_from = ''):
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


    def аssign_rating(self, id_group, subject_id, type_score, mark = '', subperiod = '', date_from = ''):
        sub_g = self.uploader_sub_group_names(id_group, subject_id)
        if len(sub_g) == 0:
            sub_g = [0,0]
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


    def score_final(self, id_group, subject_id, student_id, score, type_score,subperiod = '', date_from = ''):
        date_from = self.date_patch(date_from)
        nums = re.findall(r'\d+', subject_id)
        if type_score == 'annual_estimation':
            d = '{"lessons":{},"final_marks":{"'+f'{str(student_id)}_{type_score}'+'":{"mark":"'+str(score)+'","type":"'+type_score+'","student_id":'+str(student_id)+'}},"subperiod_marks":{}}'
        else:
            d = '{"lessons":{},"final_marks":{},"subperiod_marks":{"'+f'{str(student_id)}_subperiod_{id_group}_{subperiod}'+'":{'+f'"mark":"{score}","subperiod_id":"{subperiod}","student_id":{str(student_id)}'+'}}}'
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
        self.session.post('https://ssuz.vip.edu35.ru/actions/register/lessons_tab/lessons_tab_save_rows', headers=self.head(), data=data)


def sd(score):
    i = int(score) if score % 1 < 0.75 else int(score)+1
    return i

def wwwww(disc):
    print(disc['name'])
    nums = re.findall(r'\d+', disc['subject_id'])
    s.аssign_rating(disc['id_group'], disc['subject_id'], 'Годовая', mark=0)
    s.аssign_rating(disc['id_group'], disc['subject_id'], 'Итоговая', mark=1)
    s.аssign_rating(disc['id_group'], disc['subject_id'], '2 семестр(22/23)', subperiod=400)
    for stud in s.student_rows(disc['id_group'], disc['subject_id'])['rows']:
        w = sd(float(z)) if (z:=stud['aver_period']) != '' else z
        q = sd(float(x)) if (x:=stud[f"aver_subper_{nums[0]}_400"]) != '' else x
        s.score_final(disc['id_group'], disc['subject_id'], stud['student_id'], w, 'annual_estimation')
        s.score_final(disc['id_group'], disc['subject_id'], stud['student_id'], q, '', 400)

if __name__ == '__main__':
    s = AvtoJ()
    s.set_cookie('ssuz_sessionid=4wf3yr029r27rnyf4xamkb3vlkao6igc')
    for disc in ListOfDisciplines.Theory:
        wwwww(disc)



