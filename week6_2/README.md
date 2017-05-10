# HackLX

Your task is to create a small system for offers.

Here are some mockups: https://app.moqups.com/meco/FYpHUL2OUu/view/page/ad64222d5

Keep in mind:
- You have handle the media file upload
- You have to optimize you calls using django-debug-toolbar
- You have to use Bootstrap to make the system look good.

Rewrite all views using class-based-views.

Add a new `DetailView` for every offer.


# Class-Based Views

* In CBV we use [LoginRequiredMixin](https://docs.djangoproject.com/en/1.10/topics/auth/default/#the-loginrequired-mixin) instead `login_required` decorator.
* [Intro of CBV](https://docs.djangoproject.com/en/1.10/topics/class-based-views/intro/)
* [Generic views - ListView and DetailView](https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-display/)
* Generic editing views -[CreateView, UpdateView, DeleteView](https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-editing/)
