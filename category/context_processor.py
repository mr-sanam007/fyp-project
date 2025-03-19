from .models import Category


#  this file contain the function that takes request as argument and return ditionary of data

def menu_links(request):
    links = Category.objects.all()
    return {'links': links}  # return a dictionary with the links