from rest_framework import serializers

from book.models import BookStar, MyBook

__all__ = (
    'StarSerializer',
)


class StarSerializer(serializers.ModelSerializer):
    mybook = serializers.PrimaryKeyRelatedField(queryset=MyBook.objects.all())

    class Meta:
        model = BookStar
        fields = (
            'content',
            'created_date',
            'mybook',
        )
        read_only_fields = (
            'created_date',
        )

    def create(self, validated_data):
        instance = BookStar.objects.get_or_create(**validated_data)
        return instance
