from rest_framework import serializers
from account.models import Expend


class ExpendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expend
        fields = ('by_user', 'added_date', 'source_fund', 'source_amount', 'description', 'expend_in', 'expend_amount', 'verified')
        read_only_fields = ['by_user']
