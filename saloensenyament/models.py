from persistent.mapping import PersistentMapping
from pyramid.security import Allow, Authenticated

class MyModel(PersistentMapping):
    __parent__ = __name__ = None
    __acl__ = [ (Allow, Authenticated, 'view'), ]    

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MyModel()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
