# Миксины
class CommonContextMixin():
    """Мой миксин для добавления title"""
    title = None

    def get_context_data(self, **kwargs):
        context = super(CommonContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
