from flask_admin import AdminIndexView
from flask_admin.base import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login.utils import logout_user
from werkzeug.utils import redirect

from saleapp import app, db, utils
from saleapp.models import Category, Product, Receipt, ReceiptDetail, Tag, User, UserRole


class AdminHomeView(AdminIndexView):
    @expose('/')
    def home(self):
        cate_stats = utils.cate_stats2()
        return self.render('admin/pages/home.html', cate_stats=cate_stats)

# Custom Views Config 
class ProductView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_model = True
    details_modal = True
    column_filters = ['name', 'price']
    column_searchable_list = ['name']
    

class UserView(ModelView):
    edit_model = True

class AdminAutheticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, name='ĐiệnMáyXanhLè Admin', template_mode='bootstrap4', index_view=AdminHomeView())

admin.add_view(AdminAutheticatedView(Category, db.session))
admin.add_view(AdminAutheticatedView(Receipt, db.session))
admin.add_view(AdminAutheticatedView(ReceiptDetail, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(AdminAutheticatedView(Tag, db.session))
admin.add_view(LogoutView(name="Log out"))
