from django.shortcuts import redirect


class NoLoginRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
