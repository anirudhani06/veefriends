from django.shortcuts import redirect

# only un authenticated user.
def is_unauthenticated(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func