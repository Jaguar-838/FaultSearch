import sys
import files_tools as fTool
import logger
import tg_webApi as tg

def start():
    lg_stat = logger.Logger('', 'statistic.txt')
    lg_fails = logger.Logger('', 'fails.txt')
    lg_stat.open()
    lg_fails.open()
    #@reboot /usr/bin/python3 /home/pcuser/Tests_mac_print/FaultSearch/bot.py
    path = '/home/pcuser/Desktop/reports'

    _all, _deleted = fTool.delete_small_len_files(path)
    lg_stat.log(f'Всего файлов было: {_all}')
    lg_stat.log(f'\nБыло удалено недописаных файлов: {_deleted}')
    lg_stat.log('\n-')
    _all, _deleted = fTool.delete_earlier_files(path)
    lg_stat.log(f'\nВсего было файлов: {_all}')
    lg_stat.log(f'\nБыло удалено ранних копий файлов: {_deleted}')
    lg_stat.log('\n-')
    _all, _fails = fTool.search_fails_report_count(path)
    prc = round(((_fails/_all)*100), 3)
    lg_stat.log(f'\nСудя по отчетам, всего роутеров протестировано: {_all}')
    lg_stat.log(f'\nИз них не прошли быстрый тест: {_fails}')
    lg_stat.log(f'\nА это в процентах: {prc}%')
    lg_stat.log('\n-')
    lg_stat.log('\nИ вот какая статистика: ')
    fTool.search_statistic_in_files(path, lg_stat)
    lg_stat.close()
    fTool.write_fails(path, lg_fails)
    lg_fails.close()
    tg.send_document(document_path='statistic.txt')
    tg.send_document(document_path='fails.txt')

if __name__ == '__main__':
    start()


