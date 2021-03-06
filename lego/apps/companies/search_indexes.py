from lego.apps.search import register
from lego.apps.search.index import SearchIndex

from .models import Company
from .serializers import CompanySearchSerializer


class CompanyModelIndex(SearchIndex):

    queryset = Company.objects.all()
    serializer_class = CompanySearchSerializer
    result_fields = ("name", "description")
    autocomplete_result_fields = ("name",)

    def get_autocomplete(self, instance):
        return instance.name

    def autocomplete(self, query):
        return self.queryset.filter(name__istartswith=query)


register(CompanyModelIndex)
