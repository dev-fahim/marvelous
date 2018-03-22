from rest_framework import generics, mixins
from expend.models import Expend
from . serializers import ExpendSerializer
from django.db.models import Q


class ExpendApiView(generics.CreateAPIView):
    serializer_class = ExpendSerializer

    def perform_create(self, serializer):
        serializer.save(by_user=self.request.user.username)


class ExpendUpdateApiView(generics.UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = ExpendSerializer

    def perform_create(self, serializer):
        serializer.save(by_user=self.request.user.username)


class ExpendRudView(generics.ListAPIView):
    serializer_class = ExpendSerializer

    def get_queryset(self):
        return Expend.objects.all()


class ExpendSearchApiView(generics.ListAPIView):
    serializer_class = ExpendSerializer

    def get_queryset(self):
        qs = Expend.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(Q(source_fund__icontains=query) | Q(expend_in__icontains=query) | Q(verified__icontains=query)).distinct()
        return qs
