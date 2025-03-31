def detectUser(user):
    if user == 1:
       redirectUrl ="vendorDashboard"
    elif user == 2:
        redirectUrl = "customerDashboard"
    elif user.role == None and user.is_superadmin:
        redirectUrl = "/admin"
        return redirectUrl