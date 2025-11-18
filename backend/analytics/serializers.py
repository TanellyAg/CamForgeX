from rest_framework import serializers

class MyStatsSerializer(serializers.Serializer):
    # Common
    role = serializers.ChoiceField(choices=['ARTIST', 'PROMOTER'])
    # Artist-only fields
    tracks = serializers.IntegerField(required=False)
    campaigns = serializers.IntegerField(required=False)
    total_plays = serializers.IntegerField(required=False)
    spent = serializers.CharField(required=False)  # using string to match your current response
    # Promoter-only fields
    my_plays = serializers.IntegerField(required=False)