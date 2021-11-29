from saleapp import admin, db
from saleapp.models import Category, Product, Tag, User
from flask_admin.contrib.sqla import ModelView

# Custom Views Config 
class ProductView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_model = True
    details_modal = True
    column_filters = ['name', 'price']
    column_searchable_list = ['name']

admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tag, db.session))
