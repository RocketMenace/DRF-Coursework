from rest_framework import serializers

from habits_tracker.users.serializers import (
    UserOutputSerializer,
)
from .models import RegularHabit, RelatedHabit
from .validators import (
    OneChosenFieldValidator,
    DurationTimeValidator,
    RelatedHabitValidator,
    EnjoyableHabitValidator,
    FrequencyValidator,
)


class RelatedHabitInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = RelatedHabit
        fields = "__all__"
        validators = [RelatedHabitValidator("is_enjoyable")]


class RelatedHabitOutputSerializer(serializers.ModelSerializer):

    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = RelatedHabit
        fields = "__all__"


class RegularHabitInputSerializer(serializers.ModelSerializer):

    related_habit = RelatedHabitInputSerializer(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    award = serializers.CharField(required=False)
    place = serializers.CharField()

    class Meta:
        model = RegularHabit
        fields = [
            "place",
            "action",
            "start_time",
            "end_time",
            "public",
            "is_enjoyable",
            "user",
            "related_habit",
            "frequency",
            "award",
        ]
        validators = [
            OneChosenFieldValidator("related_habit", "award"),
            DurationTimeValidator("start_time", "end_time"),
            EnjoyableHabitValidator("award", "related_habit", "is_enjoyable"),
            FrequencyValidator("start_time"),
        ]


class RegularHabitOutputSerializer(serializers.ModelSerializer):

    related_habit = RelatedHabitOutputSerializer(read_only=True)
    user = UserOutputSerializer(read_only=True)

    class Meta:
        model = RegularHabit
        fields = "__all__"
