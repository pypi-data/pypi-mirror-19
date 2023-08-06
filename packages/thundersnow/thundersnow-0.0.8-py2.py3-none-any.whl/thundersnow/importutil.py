import importlib


__all__ = (
    'import_object',
)


def import_object(obj_path):
    """Import an object by fully qualified import path"""
    module_path, obj_name = obj_path.rsplit('.', 1)
    mod = importlib.import_module(module_path)
    obj = getattr(mod, obj_name)
    return obj
