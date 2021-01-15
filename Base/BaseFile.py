import os


def write_data(f, method='w+', data=""):
    if not os.path.isfile(f):
        print('El archivo no existe, la escritura de datos falló')
    else:
        with open(f, method, encoding="utf-8") as fs:
            fs.write(data + "\n")


def mkdir_file(f, method='w+'):
    if not os.path.isfile(f):
        with open(f, method, encoding="utf-8") as fs:
            print("Archivo %s creado correctamente" % f)
            pass
    else:
        print("El archivo %s ya existe, la creación falló" % f)
        pass


def remove_file(f):
    if os.path.isfile(f):
        os.remove(f)
    else:
        print("El archivo %s no existe y no se puede eliminar" % f)
