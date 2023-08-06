import os

log_dir_base = 'D:/Projects/TensorBoard/'


def get_log_path(relative_path, del_exist=True):
    """
    获取实际的日志目录（统一管理所有TensorFlow项目的日志目录）
    可以选择删除已经存在的同名目录

    :param relative_path: 日志目录相对路径
    :param del_exist: 是否删除已经存在的同名目录
    :return: 实际的日志目录

    :since: 0.2.0
    """
    path = log_dir_base + relative_path + '/'
    if del_exist:
        try:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
        except:
            print('删除' + path + '失败！请确认是否被其他程序（如TensorBoard）占用')
            return get_log_path(relative_path + 'z')
        os.makedirs(path)
    else:
        if not os.path.exists(path):
            os.makedirs(path)

    return path

